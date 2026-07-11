"""Автоперенастройка: параметры улучшаются со временем без участия человека.

Запуск:  python -m backtest.retune                # разовая рекомендация (dry-run)
         python -m backtest.retune --apply        # применить, если лучше текущих
         python -m backtest.retune --apply --loop # автономный цикл раз в interval_days

Логика: walk-forward подбор на свежей истории (70% in-sample, 30%
out-of-sample). Новые параметры ПРИМЕНЯЮТСЯ только если на out-of-sample
они лучше текущих минимум на min_improvement_pct и просадка не хуже
текущей более чем на max_dd_worsening_pct. Иначе — остаёмся на старых.
Применение = запись data/params_override.json; работающие боты подхватывают
его на лету (без рестарта). История решений — в data/retune_log.jsonl.
"""
import argparse
import itertools
import json
import logging
import time
from datetime import datetime, timezone
from pathlib import Path

from bot.config import load_config
from bot.notifier import Notifier
from backtest.backtest import fetch_history, run_backtest
from backtest.optimize import GRID, MIN_TRADES, TOP_N, IS_SHARE, apply_params, fmt

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")
log = logging.getLogger("retune")


def recommend(df, cfg) -> dict | None:
    """Ищет параметры лучше текущих. None — оставаться на текущих."""
    rt = cfg["retune"]
    balance = cfg.paper["starting_balance_usdt"]
    split = int(len(df) * IS_SHARE)
    df_is = df.iloc[:split].reset_index(drop=True)
    df_oos = df.iloc[split:].reset_index(drop=True)

    current = run_backtest(df_oos, cfg, balance)
    log.info("Текущие параметры на OOS: %+.2f%% (dd %.1f%%, %d сделок)",
             current["return_pct"], current["max_drawdown_pct"], current["trades"])

    keys = list(GRID)
    combos = [dict(zip(keys, v)) for v in itertools.product(*GRID.values())]
    combos = [c for c in combos
              if c[("strategy", "ema_fast")] < c[("strategy", "ema_slow")]]
    scored = []
    for combo in combos:
        r = run_backtest(df_is, apply_params(cfg, combo), balance)
        if r["trades"] >= MIN_TRADES:
            scored.append((combo, r))
    scored.sort(key=lambda cr: cr[1]["return_pct"], reverse=True)

    best = None
    for combo, _ in scored[:TOP_N]:
        r_oos = run_backtest(df_oos, apply_params(cfg, combo), balance)
        if best is None or r_oos["return_pct"] > best[1]["return_pct"]:
            best = (combo, r_oos)
    if best is None:
        log.info("Ни один вариант не набрал %d сделок in-sample — без изменений", MIN_TRADES)
        return None

    combo, r_oos = best
    improvement = r_oos["return_pct"] - current["return_pct"]
    dd_worsening = current["max_drawdown_pct"] - r_oos["max_drawdown_pct"]  # dd отрицательный
    log.info("Лучший кандидат: %s -> OOS %+.2f%% (dd %.1f%%, %d сделок), прирост %+.2f п.п.",
             fmt(combo), r_oos["return_pct"], r_oos["max_drawdown_pct"],
             r_oos["trades"], improvement)

    if r_oos["trades"] < rt["min_oos_trades"]:
        log.info("Отклонено: мало OOS-сделок (%d < %d)", r_oos["trades"], rt["min_oos_trades"])
        return None
    if improvement < rt["min_improvement_pct"]:
        log.info("Отклонено: прирост %.2f п.п. < порога %.2f — остаёмся на текущих",
                 improvement, rt["min_improvement_pct"])
        return None
    if dd_worsening > rt["max_dd_worsening_pct"]:
        log.info("Отклонено: просадка хуже на %.1f п.п. (> %.1f)",
                 dd_worsening, rt["max_dd_worsening_pct"])
        return None
    return {"combo": combo, "current": current, "candidate": r_oos,
            "improvement": improvement}


def apply_override(cfg, rec: dict):
    """Пишет подобранные параметры в override-файл + журнал решений."""
    rt = cfg["retune"]
    override = {"strategy": {}, "risk": {},
                "updated_at": datetime.now(timezone.utc).isoformat()}
    for (section, key), value in rec["combo"].items():
        override[section][key] = value
    path = Path(rt["override_file"])
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(override, indent=2))
    tmp.replace(path)

    with open(rt["log_file"], "a") as f:
        f.write(json.dumps({
            "ts": override["updated_at"],
            "params": {f"{s}.{k}": v for (s, k), v in rec["combo"].items()},
            "oos_return_pct": rec["candidate"]["return_pct"],
            "prev_oos_return_pct": rec["current"]["return_pct"],
        }) + "\n")
    log.info("Записан %s — боты подхватят на лету", path)


def run_once(args) -> bool:
    cfg = load_config(args.config)  # уже с текущим override
    rt = cfg["retune"]
    symbol = args.symbol or cfg.symbols[0]
    log.info("Перенастройка на %s, %d дней %s", symbol, rt["days_history"], cfg.timeframe)
    df = fetch_history(cfg["exchange"], symbol, cfg.timeframe, rt["days_history"])
    rec = recommend(df, cfg)
    if not rec:
        return False
    if args.apply:
        apply_override(cfg, rec)
        Notifier(cfg).send(
            f"🔧 Автоперенастройка: новые параметры дают {rec['improvement']:+.1f} п.п. "
            f"на out-of-sample — применены"
        )
    else:
        log.info("Dry-run: добавьте --apply для применения")
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--symbol", default=None, help="по умолчанию первый из config")
    ap.add_argument("--config", default="config.yaml")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--loop", action="store_true", help="повторять раз в interval_days")
    args = ap.parse_args()

    while True:
        try:
            run_once(args)
        except Exception as e:  # noqa: BLE001 — в цикле сбой не фатален
            log.exception("Ошибка перенастройки: %s", e)
            if not args.loop:
                raise
        if not args.loop:
            break
        interval_days = load_config(args.config)["retune"]["interval_days"]
        log.info("Следующая перенастройка через %d дн.", interval_days)
        time.sleep(interval_days * 86400)


if __name__ == "__main__":
    main()
