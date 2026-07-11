"""Адаптивное распределение риска: система учится на собственных сделках.

Стратегия, зарабатывающая в последних N сделках, получает множитель риска
до cap_mult; сливающая — до floor_mult. Никогда не ноль: стратегия
продолжает торговать малым размером и может «реабилитироваться», когда
рынок снова станет её. Мало данных (< min_trades) — нейтральный 1.0.
"""
import logging

log = logging.getLogger("adaptive")

PF_CAP = 3.0  # выше — не делаем различий: и так отлично


def _interp(x: float, x0: float, x1: float, y0: float, y1: float) -> float:
    return y0 + (y1 - y0) * (x - x0) / (x1 - x0)


def risk_multiplier(state, strategy: str, params: dict) -> float:
    """Множитель риска стратегии по её недавнему profit factor."""
    if not params.get("enabled"):
        return 1.0
    pnls = state.recent_pnls(strategy, params["window_trades"])
    if len(pnls) < params["min_trades"]:
        return 1.0
    gross_win = sum(p for p in pnls if p > 0)
    gross_loss = abs(sum(p for p in pnls if p <= 0))
    pf = min(gross_win / gross_loss if gross_loss else PF_CAP, PF_CAP)

    floor, cap = params["floor_mult"], params["cap_mult"]
    if pf <= 0.6:
        mult = floor
    elif pf < 1.0:
        mult = _interp(pf, 0.6, 1.0, floor, 1.0)
    elif pf < 1.6:
        mult = _interp(pf, 1.0, 1.6, 1.0, cap)
    else:
        mult = cap
    if mult != 1.0:
        log.info("[%s] pf=%.2f за %d сделок -> множитель риска %.2f",
                 strategy, pf, len(pnls), mult)
    return mult
