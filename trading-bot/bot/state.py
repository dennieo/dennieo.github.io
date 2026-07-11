"""Состояние бота в SQLite: позиции, сделки, кривая капитала.

Переживает перезапуски: после старта бот читает открытые позиции из БД.
"""
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

SCHEMA = """
CREATE TABLE IF NOT EXISTS positions (
    symbol TEXT PRIMARY KEY,
    qty REAL NOT NULL,
    entry_price REAL NOT NULL,
    stop_loss REAL NOT NULL,
    take_profit REAL NOT NULL,
    opened_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS trades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT NOT NULL,
    qty REAL NOT NULL,
    entry_price REAL NOT NULL,
    exit_price REAL NOT NULL,
    pnl REAL NOT NULL,
    reason TEXT NOT NULL,
    opened_at TEXT NOT NULL,
    closed_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS equity (
    ts TEXT PRIMARY KEY,
    equity REAL NOT NULL
);
CREATE TABLE IF NOT EXISTS kv (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
"""


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


class State:
    def __init__(self, db_path: str):
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(db_path)
        self.db.row_factory = sqlite3.Row
        self.db.executescript(SCHEMA)

    # --- позиции ---
    def get_position(self, symbol: str) -> dict | None:
        row = self.db.execute(
            "SELECT * FROM positions WHERE symbol = ?", (symbol,)
        ).fetchone()
        return dict(row) if row else None

    def open_positions_count(self) -> int:
        return self.db.execute("SELECT COUNT(*) FROM positions").fetchone()[0]

    def save_position(self, symbol, qty, entry_price, stop_loss, take_profit):
        self.db.execute(
            "INSERT OR REPLACE INTO positions VALUES (?,?,?,?,?,?)",
            (symbol, qty, entry_price, stop_loss, take_profit, _now()),
        )
        self.db.commit()

    def close_position(self, symbol: str, exit_price: float, reason: str) -> dict:
        pos = self.get_position(symbol)
        pnl = (exit_price - pos["entry_price"]) * pos["qty"]
        self.db.execute(
            "INSERT INTO trades (symbol, qty, entry_price, exit_price, pnl, reason,"
            " opened_at, closed_at) VALUES (?,?,?,?,?,?,?,?)",
            (symbol, pos["qty"], pos["entry_price"], exit_price, pnl, reason,
             pos["opened_at"], _now()),
        )
        self.db.execute("DELETE FROM positions WHERE symbol = ?", (symbol,))
        self.db.commit()
        return {**pos, "exit_price": exit_price, "pnl": pnl, "reason": reason}

    def invested_usdt(self) -> float:
        """Сколько USDT сейчас вложено в открытые позиции (по ценам входа)."""
        row = self.db.execute(
            "SELECT COALESCE(SUM(qty * entry_price), 0) FROM positions"
        ).fetchone()
        return float(row[0])

    # --- капитал ---
    def snapshot_equity(self, equity: float):
        self.db.execute(
            "INSERT OR REPLACE INTO equity VALUES (?, ?)", (_now(), equity)
        )
        self.db.commit()

    def pnl_today(self) -> float:
        today = datetime.now(timezone.utc).date().isoformat()
        row = self.db.execute(
            "SELECT COALESCE(SUM(pnl), 0) FROM trades WHERE closed_at >= ?", (today,)
        ).fetchone()
        return float(row[0])

    # --- kv (баланс paper-режима и пр.) ---
    def kv_get(self, key: str, default: str | None = None) -> str | None:
        row = self.db.execute("SELECT value FROM kv WHERE key = ?", (key,)).fetchone()
        return row[0] if row else default

    def kv_set(self, key: str, value: str):
        self.db.execute("INSERT OR REPLACE INTO kv VALUES (?, ?)", (key, value))
        self.db.commit()
