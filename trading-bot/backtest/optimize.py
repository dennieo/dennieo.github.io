"""Walk-forward подбор параметров стратегии.

Запуск:  python -m backtest.optimize --symbol BTC/USDT --days 540

Защита от переподгонки: параметры подбираются на первых 70% истории
(in-sample), а оцениваются на последних 30% (out-of-sample), которые
оптимизатор «не видел». Доверять стоит только OOS-цифрам: если лучший
in-sample вариант провалился на OOS — стратегия подогнана под шум.
"""
import argparse
import copy
import itertools
import logging

from bot.config import Config, load_config
from backtest.backtest import fetch_history, run_backtest

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger("optimize")

# сетка параметров: намеренно небольшая — гигантские сетки находят шум
GRID = {
    ("strategy", "ema_fast"): [8, 12, 16],
    ("strategy", "ema_slow"): [21, 26, 34],
    ("risk", "stop_atr_mult"): [1.5, 2.0, 2.5],
    ("risk", "take_profit_atr_mult"): [2.0, 3.0, 4.5],
}
MIN_TRADES = 5      # in-sample вариант с < N сделок = случайность, отсекаем
TOP_N = 5           # сколько лучших вариантов проверяем на out-of-sample
IS_SHARE = 0.7      # доля истории под in-sample


def apply_params(cfg: Config, combo: dict) -> Config:
    raw = copy.deepcopy(cfg.raw)
    for (section, key), value in combo.items():
        raw[section][key] = value
    return Config(raw=raw)


def fmt(combo: dict) -> str:
    return ", ".join(f"{k[1]}={v}" for k, v in combo.items())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--symbol", default="BTC/USDT")
    ap.add_argument("--days", type=int, default=540)
    ap.add_argument("--config", default="config.yaml")
    args = ap.parse_args()

    cfg = load_config(args.config)
    balance = cfg.paper["starting_balance_usdt"]
    log.info("Загружаю %s дней %s (%s)...", args.days, args.symbol, cfg.timeframe)
    df = fetch_history(cfg["exchange"], args.symbol, cfg.timeframe, args.days)
    split = int(len(df) * IS_SHARE)
    df_is, df_oos = df.iloc[:split].reset_index(drop=True), df.iloc[split:].reset_index(drop=True)
    log.info("In-sample: %d свечей, out-of-sample: %d свечей", len(df_is), len(df_oos))

    keys = list(GRID)
    combos = [dict(zip(keys, values)) for values in itertools.product(*GRID.values())]
    combos = [c for c in combos
              if c[("strategy", "ema_fast")] < c[("strategy", "ema_slow")]]
    log.info("Вариантов параметров: %d\n", len(combos))

    results = []
    for combo in combos:
        r = run_backtest(df_is, apply_params(cfg, combo), balance)
        if r["trades"] >= MIN_TRADES:
            results.append((combo, r))
    results.sort(key=lambda cr: cr[1]["return_pct"], reverse=True)

    log.info("=== Топ-%d по in-sample -> проверка на out-of-sample ===", TOP_N)
    log.info("%-55s %10s %10s %8s", "параметры", "IS ret%", "OOS ret%", "OOS dd%")
    best = None
    for combo, r_is in results[:TOP_N]:
        r_oos = run_backtest(df_oos, apply_params(cfg, combo), balance)
        log.info("%-55s %+9.1f%% %+9.1f%% %7.1f%%", fmt(combo),
                 r_is["return_pct"], r_oos["return_pct"], r_oos["max_drawdown_pct"])
        if best is None or r_oos["return_pct"] > best[1]["return_pct"]:
            best = (combo, r_oos)

    if best:
        log.info("\nЛучший по OOS: %s", fmt(best[0]))
        log.info("Перенесите эти значения в config.yaml. Если все OOS-результаты")
        log.info("сильно хуже in-sample — не доверяйте подбору: это переподгонка.")


if __name__ == "__main__":
    main()
