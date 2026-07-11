"""Трекер позиций умных кошельков и консенсус-сигналы.

Сигнал BUY по монете — когда лонг держат >= consensus_min кошельков из топа
(переход через порог снизу вверх). SELL — когда консенсус распался
(переход сверху вниз). Копируем только лонги: исполнение на споте.
"""
import logging
from dataclasses import dataclass

log = logging.getLogger("tracker")


@dataclass
class ConsensusSignal:
    coin: str
    action: str      # BUY | SELL
    longs: int       # сколько кошельков сейчас в лонге
    total: int       # сколько кошельков отслеживаем


class SmartMoneyTracker:
    def __init__(self, client, wallets: list[str], coins: list[str], consensus_min: int):
        self.client = client
        self.wallets = wallets
        self.coins = set(coins)
        self.consensus_min = consensus_min
        self.prev_longs: dict[str, int] = {}   # coin -> число лонгов на прошлом опросе
        self.first_poll = True

    def poll_positions(self) -> dict[str, dict[str, float]]:
        """{wallet: {coin: szi}} по всем отслеживаемым кошелькам."""
        out = {}
        for w in self.wallets:
            try:
                out[w] = self.client.positions(w)
            except Exception as e:  # noqa: BLE001 — один кошелёк не срывает опрос
                log.warning("Не смог получить позиции %s: %s", w, e)
        return out

    def consensus(self, positions: dict[str, dict[str, float]]) -> dict[str, int]:
        """coin -> число отслеживаемых кошельков в лонге по этой монете."""
        longs: dict[str, int] = {c: 0 for c in self.coins}
        for pos in positions.values():
            for coin, szi in pos.items():
                if coin in self.coins and szi > 0:
                    longs[coin] += 1
        return longs

    def tick(self) -> list[ConsensusSignal]:
        """Один опрос: возвращает сигналы на переходах через порог консенсуса."""
        positions = self.poll_positions()
        if not positions:
            return []
        longs = self.consensus(positions)
        signals = []
        for coin, n in longs.items():
            prev = self.prev_longs.get(coin, 0)
            crossed_up = prev < self.consensus_min <= n
            crossed_down = n < self.consensus_min <= prev
            # на первом опросе не сигналим: не знаем, свежий это консенсус или старый
            if not self.first_poll:
                if crossed_up:
                    signals.append(ConsensusSignal(coin, "BUY", n, len(positions)))
                elif crossed_down:
                    signals.append(ConsensusSignal(coin, "SELL", n, len(positions)))
        self.prev_longs = longs
        self.first_poll = False
        return signals
