"""Отчёт о результатах всех ботов: консоль + Telegram.

Запуск:  python -m bot.report [config.yaml]
Читает базы обоих ботов (trend и smart-money) и собирает сводку:
капитал, PnL за 7/30 дней, статистика сделок по стратегиям.
"""
import logging
import sqlite3
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

from bot.config import load_config
from bot.notifier import Notifier

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger("report")


def equity_stats(db: sqlite3.Connection) -> dict:
    row = db.execute("SELECT ts, equity FROM equity ORDER BY ts DESC LIMIT 1").fetchone()
    if not row:
        return {}
    now_eq = row[1]
    out = {"equity": now_eq}
    for label, days in (("7d", 7), ("30d", 30)):
        cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()
        past = db.execute(
            "SELECT equity FROM equity WHERE ts <= ? ORDER BY ts DESC LIMIT 1", (cutoff,)
        ).fetchone()
        if past and past[0]:
            out[label] = (now_eq / past[0] - 1) * 100
    return out


def trade_stats(db: sqlite3.Connection) -> list[dict]:
    rows = db.execute(
        """SELECT strategy, COUNT(*), SUM(pnl),
                  SUM(CASE WHEN pnl > 0 THEN 1 ELSE 0 END)
           FROM trades GROUP BY strategy"""
    ).fetchall()
    return [
        {"strategy": r[0], "trades": r[1], "pnl": r[2] or 0.0,
         "winrate": 100 * r[3] / r[1] if r[1] else 0}
        for r in rows
    ]


def build_report(cfg) -> str:
    lines = [f"📊 Отчёт ({datetime.now(timezone.utc):%Y-%m-%d %H:%M} UTC)"]
    dbs = {"trend-бот": cfg["paths"]["db"], "smart-money": cfg["smartmoney"]["db"]}
    for name, path in dbs.items():
        if not Path(path).exists():
            lines.append(f"\n{name}: базы ещё нет (бот не запускался)")
            continue
        db = sqlite3.connect(path)
        lines.append(f"\n— {name} —")
        eq = equity_stats(db)
        if eq:
            s = f"Капитал: {eq['equity']:.2f} USDT"
            for label in ("7d", "30d"):
                if label in eq:
                    s += f" | {label}: {eq[label]:+.2f}%"
            lines.append(s)
        stats = trade_stats(db)
        if not stats:
            lines.append("Закрытых сделок пока нет")
        for st in stats:
            lines.append(
                f"[{st['strategy']}] сделок {st['trades']}, "
                f"PnL {st['pnl']:+.2f} USDT, winrate {st['winrate']:.0f}%"
            )
        open_pos = db.execute("SELECT symbol, strategy FROM positions").fetchall()
        if open_pos:
            lines.append("Открыто: " + ", ".join(f"{s} [{st}]" for s, st in open_pos))
        db.close()
    return "\n".join(lines)


if __name__ == "__main__":
    cfg = load_config(sys.argv[1] if len(sys.argv) > 1 else "config.yaml")
    report = build_report(cfg)
    log.info("%s", report)
    Notifier(cfg).send(report)
