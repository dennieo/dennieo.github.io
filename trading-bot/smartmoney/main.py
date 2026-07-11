"""Smart-money бот: следование за лучшими кошельками Hyperliquid.

Запуск:  python -m smartmoney.main [путь_к_config.yaml]

По умолчанию auto_trade выключен — бот только шлёт сигналы (лог/Telegram).
С auto_trade: true сигналы исполняются на споте Binance через ту же
инфраструктуру, что и v1 (paper/testnet/live, риск 1%, стопы по ATR).
"""
import logging
import sys
import time

from bot.config import load_config
from bot.consensus import write_consensus
from bot.notifier import Notifier
from smartmoney.hyperliquid import HyperliquidClient
from smartmoney.scoring import rank_wallets
from smartmoney.tracker import SmartMoneyTracker

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
log = logging.getLogger("smartmoney")


def fetch_leaderboard_wallets(url: str, limit: int) -> list[str]:
    """Кандидаты из публичного лидерборда (best effort — формат неофициальный)."""
    import requests
    try:
        rows = requests.get(url, timeout=20).json().get("leaderboardRows", [])
        return [r["ethAddress"] for r in rows[:limit] if r.get("ethAddress")]
    except Exception as e:  # noqa: BLE001
        log.warning("Лидерборд недоступен (%s) — используйте wallets в конфиге", e)
        return []


class SmartMoneyBot:
    def __init__(self, config_path: str = "config.yaml"):
        self.cfg = load_config(config_path)
        self.sm = self.cfg["smartmoney"]
        self.notifier = Notifier(self.cfg)
        self.client = HyperliquidClient(self.sm["api_url"])
        self.trade = None
        if self.sm.get("auto_trade"):
            from bot.exchange import Exchange
            from bot.executor import Executor
            from bot.risk import RiskManager
            from bot.state import State
            state = State(self.sm["db"])
            exchange = Exchange(self.cfg)
            self.trade = {
                "state": state,
                "exchange": exchange,
                "executor": Executor(
                    self.cfg, exchange, state, self.sm.get("budget_usdt")
                ),
                "risk": RiskManager(self.cfg, state),
            }

    # --- подготовка: скоринг и выбор кошельков ---
    def select_wallets(self) -> list[str]:
        candidates = list(self.sm.get("wallets") or [])
        if not candidates:
            candidates = fetch_leaderboard_wallets(
                self.sm["leaderboard_url"], self.sm["leaderboard_candidates"]
            )
        if not candidates:
            raise SystemExit("Нет кандидатов: заполните smartmoney.wallets в config.yaml")
        log.info("Скоринг %d кошельков-кандидатов...", len(candidates))
        ranked = rank_wallets(self.client, candidates, self.sm["min_trades"], self.sm["top_n"])
        if not ranked:
            raise SystemExit("Ни один кошелёк не прошёл фильтры (min_trades / PnL > 0)")
        for s in ranked:
            log.info(
                "  %s  score=%.2f  pnl=%+.0f$  winrate=%.0f%%  pf=%.2f  сделок=%d",
                s.wallet, s.score, s.pnl_total, s.winrate * 100, s.profit_factor, s.n_trades,
            )
        return [s.wallet for s in ranked]

    # --- исполнение сигналов (auto_trade) ---
    def execute(self, signal):
        symbol = self.sm["map_to_spot"].get(signal.coin)
        if not self.trade or not symbol:
            return
        t = self.trade
        pos = t["state"].get_position(symbol)
        if signal.action == "SELL" and pos:
            price = t["exchange"].last_price(symbol)
            fill = t["executor"].close_long(symbol, pos["qty"], price)
            trade = t["state"].close_position(symbol, fill, "smart_money_exit")
            self.notifier.send(f"❌ SM: закрыл {symbol} по {fill:.2f}, PnL {trade['pnl']:+.2f}")
        elif signal.action == "BUY" and not pos:
            from bot.indicators import add_indicators
            from bot.strategy import stop_and_take
            equity = t["executor"].cash()
            allowed, why = t["risk"].entry_allowed(equity)
            if not allowed:
                log.info("SM %s: вход запрещён — %s", symbol, why)
                return
            df = add_indicators(
                t["exchange"].fetch_ohlcv(symbol, self.cfg.timeframe, 100), self.cfg.strategy
            )
            price = t["exchange"].last_price(symbol)
            atr_value = float(df["atr"].iloc[-1])
            qty = t["risk"].position_size(equity, price, atr_value, t["executor"].cash())
            if qty <= 0:
                return
            fill = t["executor"].open_long(symbol, qty, price)
            stop, take = stop_and_take(fill, atr_value, self.cfg.risk)
            t["state"].save_position(symbol, qty, fill, stop, take, "smart_money")
            self.notifier.send(f"✅ SM: купил {symbol} qty={qty:.8f} по {fill:.2f}, SL {stop:.2f}")

    def manage_positions(self):
        """Стопы/тейки открытых smart-money позиций (auto_trade)."""
        if not self.trade:
            return
        t = self.trade
        for symbol in self.sm["map_to_spot"].values():
            pos = t["state"].get_position(symbol)
            if not pos:
                continue
            price = t["exchange"].last_price(symbol)
            reason = None
            if price <= pos["stop_loss"]:
                reason = "stop_loss"
            elif price >= pos["take_profit"]:
                reason = "take_profit"
            if reason:
                fill = t["executor"].close_long(symbol, pos["qty"], price)
                trade = t["state"].close_position(symbol, fill, reason)
                self.notifier.send(
                    f"❌ SM: закрыл {symbol} по {fill:.2f} ({reason}), PnL {trade['pnl']:+.2f}"
                )

    # --- цикл ---
    def run(self):
        wallets = self.select_wallets()
        tracker = SmartMoneyTracker(
            self.client, wallets, self.sm["coins"], self.sm["consensus_min"]
        )
        mode = "auto_trade" if self.trade else "только сигналы"
        log.info("Слежу за %d кошельками, монеты %s, консенсус >=%d (%s)",
                 len(wallets), self.sm["coins"], self.sm["consensus_min"], mode)
        self.notifier.send(f"🧠 Smart-money бот запущен ({mode}): {len(wallets)} кошельков")
        while True:
            try:
                for sig in tracker.tick():
                    msg = (f"{'🟢' if sig.action == 'BUY' else '🔴'} SM-сигнал: {sig.action} "
                           f"{sig.coin} — в лонге {sig.longs}/{sig.total} умных кошельков")
                    log.info(msg)
                    self.notifier.send(msg)
                    self.execute(sig)
                # публикуем анализ для трендового бота (smartmoney_filter)
                if not tracker.first_poll:
                    write_consensus(
                        self.sm["consensus_file"], tracker.prev_longs, len(wallets)
                    )
                self.manage_positions()
            except KeyboardInterrupt:
                break
            except Exception as e:  # noqa: BLE001
                log.exception("Ошибка тика: %s", e)
            time.sleep(self.sm["poll_interval_sec"])


if __name__ == "__main__":
    SmartMoneyBot(sys.argv[1] if len(sys.argv) > 1 else "config.yaml").run()
