"""Бэктест той же стратегии на истории Binance.

Запуск:  python -m backtest.backtest --symbol BTC/USDT --days 365
Использует те же generate_signal / stop_and_take / position_size, что и живой бот.
"""
import argparse
import logging

import ccxt
import pandas as pd

from bot.config import load_config
from bot.indicators import add_indicators
from bot.strategy import entry_decision, exit_decision, stop_and_take

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger("backtest")

WARMUP = 50  # свечей на разогрев индикаторов


def fetch_history(exchange_id: str, symbol: str, timeframe: str, days: int) -> pd.DataFrame:
    client = getattr(ccxt, exchange_id)({"enableRateLimit": True})
    ms_per_candle = client.parse_timeframe(timeframe) * 1000
    since = client.milliseconds() - days * 86_400_000
    rows = []
    while since < client.milliseconds():
        batch = client.fetch_ohlcv(symbol, timeframe, since=since, limit=1000)
        if not batch:
            break
        rows.extend(batch)
        since = batch[-1][0] + ms_per_candle
    df = pd.DataFrame(rows, columns=["ts", "open", "high", "low", "close", "volume"])
    df["ts"] = pd.to_datetime(df["ts"], unit="ms", utc=True)
    return df.drop_duplicates("ts").reset_index(drop=True)


def run_backtest(df: pd.DataFrame, cfg, starting_balance: float) -> dict:
    fee = cfg.paper["fee_pct"] / 100
    risk = cfg.risk
    cash, pos = starting_balance, None
    trades, equity_curve = [], []

    df = add_indicators(df, cfg.strategy)
    for i in range(WARMUP, len(df)):
        window = df.iloc[: i + 1]
        candle = df.iloc[i]

        if pos:
            exit_price, reason = None, None
            if candle["low"] <= pos["stop"]:
                exit_price, reason = pos["stop"], "stop_loss"
            elif candle["high"] >= pos["take"]:
                exit_price, reason = pos["take"], "take_profit"
            elif exit_decision(window, cfg.strategy, pos["strategy"]):
                exit_price, reason = candle["close"], "exit_signal"
            if exit_price is not None:
                cash += pos["qty"] * exit_price * (1 - fee)
                trades.append(
                    {"pnl": pos["qty"] * (exit_price - pos["entry"]),
                     "reason": reason, "strategy": pos["strategy"]}
                )
                pos = None
        else:
            should_enter, strategy_name = entry_decision(window, cfg.strategy)
            if should_enter:
                price, atr_value = candle["close"], candle["atr"]
                risk_usd = cash * risk["risk_per_trade_pct"] / 100
                stop_dist = risk["stop_atr_mult"] * atr_value
                qty = min(risk_usd / stop_dist, cash / price) if stop_dist > 0 else 0
                if qty * price >= risk["min_order_usdt"]:
                    cash -= qty * price * (1 + fee)
                    stop, take = stop_and_take(price, atr_value, risk)
                    pos = {"qty": qty, "entry": price, "stop": stop,
                           "take": take, "strategy": strategy_name}

        equity_curve.append(cash + (pos["qty"] * candle["close"] if pos else 0))

    if pos:  # закрываем хвост по последней цене
        cash += pos["qty"] * df["close"].iloc[-1] * (1 - fee)
        trades.append({"pnl": pos["qty"] * (df["close"].iloc[-1] - pos["entry"]),
                       "reason": "end_of_data", "strategy": pos["strategy"]})

    eq = pd.Series(equity_curve)
    wins = [t for t in trades if t["pnl"] > 0]
    losses = [t for t in trades if t["pnl"] <= 0]
    gross_win = sum(t["pnl"] for t in wins)
    gross_loss = abs(sum(t["pnl"] for t in losses))
    buy_hold = starting_balance * df["close"].iloc[-1] / df["close"].iloc[WARMUP]
    return {
        "final_equity": cash,
        "return_pct": (cash / starting_balance - 1) * 100,
        "buy_hold_pct": (buy_hold / starting_balance - 1) * 100,
        "max_drawdown_pct": ((eq / eq.cummax() - 1).min()) * 100,
        "trades": len(trades),
        "winrate_pct": 100 * len(wins) / len(trades) if trades else 0,
        "profit_factor": gross_win / gross_loss if gross_loss else float("inf"),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--symbol", default="BTC/USDT")
    ap.add_argument("--days", type=int, default=365)
    ap.add_argument("--config", default="config.yaml")
    args = ap.parse_args()

    cfg = load_config(args.config)
    balance = cfg.paper["starting_balance_usdt"]
    log.info("Загружаю %s дней %s (%s)...", args.days, args.symbol, cfg.timeframe)
    df = fetch_history(cfg["exchange"], args.symbol, cfg.timeframe, args.days)
    log.info("Свечей: %s (%s — %s)", len(df), df["ts"].iloc[0], df["ts"].iloc[-1])

    r = run_backtest(df, cfg, balance)
    log.info("")
    log.info("=== Результаты: %s, %s дней, старт %.0f USDT ===", args.symbol, args.days, balance)
    log.info("Итоговый капитал:   %10.2f USDT", r["final_equity"])
    log.info("Доходность:         %+9.2f %%", r["return_pct"])
    log.info("Buy & hold:         %+9.2f %%", r["buy_hold_pct"])
    log.info("Макс. просадка:     %9.2f %%", r["max_drawdown_pct"])
    log.info("Сделок:             %10d", r["trades"])
    log.info("Winrate:            %9.1f %%", r["winrate_pct"])
    log.info("Profit factor:      %10.2f", r["profit_factor"])


if __name__ == "__main__":
    main()
