"""Риск-менеджмент: размер позиции и защитные лимиты."""
import logging
from pathlib import Path

log = logging.getLogger("risk")


class RiskManager:
    def __init__(self, cfg, state):
        self.p = cfg.risk
        self.stop_file = Path(cfg["paths"]["stop_file"])
        self.state = state

    def position_size(self, equity: float, price: float, atr_value: float,
                      available_quote: float, risk_mult: float = 1.0) -> float:
        """Кол-во базовой валюты: рискуем risk_per_trade_pct капитала до стопа.

        risk_mult — адаптивный множитель стратегии (bot/adaptive.py).
        """
        risk_usd = equity * self.p["risk_per_trade_pct"] / 100 * risk_mult
        stop_distance = self.p["stop_atr_mult"] * atr_value
        if stop_distance <= 0:
            return 0.0
        qty = risk_usd / stop_distance
        qty = min(qty, available_quote / price)  # не больше свободного баланса
        if qty * price < self.p["min_order_usdt"]:
            return 0.0
        return qty

    def entry_allowed(self, equity: float) -> tuple[bool, str]:
        if self.stop_file.exists():
            return False, f"найден файл {self.stop_file} (kill switch)"
        if self.state.open_positions_count() >= self.p["max_open_positions"]:
            return False, "достигнут лимит открытых позиций"
        daily_pnl = self.state.pnl_today()
        max_loss = equity * self.p["max_daily_loss_pct"] / 100
        if daily_pnl < -max_loss:
            return False, f"дневной убыток {daily_pnl:.2f} превысил лимит {max_loss:.2f}"
        return True, ""
