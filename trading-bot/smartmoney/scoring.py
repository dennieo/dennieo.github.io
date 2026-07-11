"""Скоринг кошельков по их истории сделок (fills Hyperliquid).

Смотрим только на закрывающие fills (closedPnl != 0) — по ним посчитан
реализованный PnL. Кошельки с малой историей или убытком отсекаются.
"""
from dataclasses import dataclass

PF_CAP = 5.0  # ограничение profit factor, чтобы пара удачных сделок не давала топ-скор


@dataclass
class WalletStats:
    wallet: str
    n_trades: int
    pnl_total: float
    winrate: float          # 0..1 по закрывающим fills
    profit_factor: float
    score: float


def score_wallet(wallet: str, fills: list[dict], min_trades: int) -> WalletStats | None:
    """None — кошелёк не прошёл фильтры (мало сделок / убыточен)."""
    closes = [f for f in fills if float(f.get("closedPnl", 0) or 0) != 0]
    if len(closes) < min_trades:
        return None

    pnls = [float(f["closedPnl"]) for f in closes]
    fees = sum(float(f.get("fee", 0) or 0) for f in fills)
    pnl_total = sum(pnls) - fees
    if pnl_total <= 0:
        return None

    wins = [p for p in pnls if p > 0]
    losses = [p for p in pnls if p <= 0]
    gross_win = sum(wins)
    gross_loss = abs(sum(losses))
    profit_factor = min(gross_win / gross_loss if gross_loss else PF_CAP, PF_CAP)
    winrate = len(wins) / len(closes)

    # стабильность важнее величины: PF * winrate, с мягким бонусом за объём истории
    score = profit_factor * winrate * min(len(closes) / (min_trades * 2), 1.5)
    return WalletStats(wallet, len(closes), pnl_total, winrate, profit_factor, score)


def rank_wallets(client, candidates: list[str], min_trades: int, top_n: int) -> list[WalletStats]:
    """Скачивает fills кандидатов, скорит, возвращает топ-N по score."""
    stats = []
    for w in candidates:
        s = score_wallet(w, client.user_fills(w), min_trades)
        if s:
            stats.append(s)
    return sorted(stats, key=lambda s: s.score, reverse=True)[:top_n]
