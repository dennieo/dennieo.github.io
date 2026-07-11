"""Главный цикл бота: данные -> анализ -> решение -> исполнение -> учёт.

Запуск:  python -m bot.main [путь_к_config.yaml]
"""
import logging
import sys
import time

from bot.config import load_config
from bot.exchange import Exchange
from bot.executor import Executor
from bot.indicators import add_indicators
from bot.notifier import Notifier
from bot.risk import RiskManager
from bot.state import State
from bot.strategy import Signal, generate_signal, stop_and_take

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
log = logging.getLogger("main")


class Bot:
    def __init__(self, config_path: str = "config.yaml"):
        self.cfg = load_config(config_path)
        self.state = State(self.cfg["paths"]["db"])
        self.ex = Exchange(self.cfg)
        self.executor = Executor(self.cfg, self.ex, self.state)
        self.risk = RiskManager(self.cfg, self.state)
        self.notifier = Notifier(self.cfg)
        self.last_candle_ts: dict[str, object] = {}

    # --- helpers ---
    def equity(self) -> float:
        """Кэш + текущая стоимость открытых позиций."""
        total = self.executor.cash()
        for symbol in self.cfg.symbols:
            pos = self.state.get_position(symbol)
            if pos:
                total += pos["qty"] * self.ex.last_price(symbol)
        return total

    # --- логика одного символа ---
    def manage_open_position(self, symbol: str, pos: dict, signal: Signal):
        price = self.ex.last_price(symbol)
        reason = None
        if price <= pos["stop_loss"]:
            reason = "stop_loss"
        elif price >= pos["take_profit"]:
            reason = "take_profit"
        elif signal == Signal.SELL:
            reason = "exit_signal"
        if not reason:
            return
        fill = self.executor.close_long(symbol, pos["qty"], price)
        trade = self.state.close_position(symbol, fill, reason)
        self.notifier.send(
            f"❌ Закрыл {symbol} по {fill:.2f} ({reason}), "
            f"PnL {trade['pnl']:+.2f} USDT"
        )

    def try_enter(self, symbol: str, df):
        equity = self.equity()
        allowed, why = self.risk.entry_allowed(equity)
        if not allowed:
            log.info("%s: вход запрещён — %s", symbol, why)
            return
        price = self.ex.last_price(symbol)
        atr_value = float(df["atr"].iloc[-1])
        qty = self.risk.position_size(equity, price, atr_value, self.executor.cash())
        if qty <= 0:
            log.info("%s: размер позиции нулевой (мало баланса/мин. ордер)", symbol)
            return
        if self.cfg.mode != "paper":
            qty = self.ex.amount_to_precision(symbol, qty)
            if qty <= 0:
                return
        fill = self.executor.open_long(symbol, qty, price)
        stop, take = stop_and_take(fill, atr_value, self.cfg.risk)
        self.state.save_position(symbol, qty, fill, stop, take)
        self.notifier.send(
            f"✅ Купил {symbol}: qty={qty:.8f} по {fill:.2f}, "
            f"SL {stop:.2f} / TP {take:.2f}"
        )

    def process_symbol(self, symbol: str):
        df = self.ex.fetch_ohlcv(
            symbol, self.cfg.timeframe, self.cfg["candles_history"]
        )
        if df.empty:
            return
        new_candle = self.last_candle_ts.get(symbol) != df["ts"].iloc[-1]
        df = add_indicators(df, self.cfg.strategy)
        signal = generate_signal(df, self.cfg.strategy) if new_candle else Signal.HOLD
        if new_candle:
            self.last_candle_ts[symbol] = df["ts"].iloc[-1]
            log.info("%s: новая свеча %s, сигнал %s", symbol, df["ts"].iloc[-1], signal)

        pos = self.state.get_position(symbol)
        if pos:
            # стопы/тейки проверяем каждым тиком, не только на новой свече
            self.manage_open_position(symbol, pos, signal)
        elif signal == Signal.BUY:
            self.try_enter(symbol, df)

    # --- цикл ---
    def run(self):
        log.info(
            "Старт бота: mode=%s, symbols=%s, tf=%s, equity=%.2f USDT",
            self.cfg.mode, self.cfg.symbols, self.cfg.timeframe, self.equity(),
        )
        self.notifier.send(f"🤖 Бот запущен ({self.cfg.mode}), equity {self.equity():.2f} USDT")
        while True:
            try:
                for symbol in self.cfg.symbols:
                    self.process_symbol(symbol)
                self.state.snapshot_equity(self.equity())
            except KeyboardInterrupt:
                log.info("Остановка по Ctrl+C")
                break
            except Exception as e:  # noqa: BLE001 — один сбой не роняет процесс
                log.exception("Ошибка тика: %s", e)
                self.notifier.send(f"⚠️ Ошибка тика: {e}")
            time.sleep(self.cfg["poll_interval_sec"])


if __name__ == "__main__":
    Bot(sys.argv[1] if len(sys.argv) > 1 else "config.yaml").run()
