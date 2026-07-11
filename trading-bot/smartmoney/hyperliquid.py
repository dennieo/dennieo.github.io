"""Клиент публичного API Hyperliquid (без ключей, только чтение).

Docs: https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint
"""
import logging
import time

import requests

log = logging.getLogger("hyperliquid")

RETRIES = 3
RETRY_PAUSE_SEC = 2


class HyperliquidClient:
    def __init__(self, api_url: str, timeout: int = 15):
        self.api_url = api_url
        self.timeout = timeout
        self.session = requests.Session()

    def _post(self, payload: dict):
        last_exc = None
        for attempt in range(1, RETRIES + 1):
            try:
                resp = self.session.post(self.api_url, json=payload, timeout=self.timeout)
                resp.raise_for_status()
                return resp.json()
            except requests.RequestException as e:
                last_exc = e
                log.warning("API-ошибка (%s/%s): %s", attempt, RETRIES, e)
                time.sleep(RETRY_PAUSE_SEC * attempt)
        raise last_exc

    def user_fills(self, wallet: str) -> list[dict]:
        """История сделок кошелька (до ~2000 последних fills).

        Каждый fill: coin, side ('B'/'A'), px, sz, time (ms), closedPnl, fee.
        """
        return self._post({"type": "userFills", "user": wallet}) or []

    def positions(self, wallet: str) -> dict[str, float]:
        """Открытые позиции кошелька: {coin: подписанный размер (>0 лонг, <0 шорт)}."""
        state = self._post({"type": "clearinghouseState", "user": wallet}) or {}
        out = {}
        for ap in state.get("assetPositions", []):
            pos = ap.get("position", {})
            szi = float(pos.get("szi", 0) or 0)
            if szi != 0:
                out[pos["coin"]] = szi
        return out
