"""Обёртка над ccxt: свечи, цены, балансы, ордера.

Единственное место в коде, которое знает о конкретной бирже.
Смена биржи = смена exchange в config.yaml (любая спотовая биржа ccxt).
"""
import logging
import time

import ccxt
import pandas as pd

log = logging.getLogger("exchange")

RETRIES = 3
RETRY_PAUSE_SEC = 2


class Exchange:
    def __init__(self, cfg):
        self.cfg = cfg
        klass = getattr(ccxt, cfg["exchange"])
        params = {"enableRateLimit": True}
        if cfg.mode in ("testnet", "live"):
            params["apiKey"] = cfg.api_key
            params["secret"] = cfg.api_secret
        self.client = klass(params)
        if cfg.mode == "testnet":
            self.client.set_sandbox_mode(True)
        self.client.load_markets()

    def _retry(self, fn, *args, **kwargs):
        last_exc = None
        for attempt in range(1, RETRIES + 1):
            try:
                return fn(*args, **kwargs)
            except (ccxt.NetworkError, ccxt.ExchangeNotAvailable) as e:
                last_exc = e
                log.warning("Сетевая ошибка (%s/%s): %s", attempt, RETRIES, e)
                time.sleep(RETRY_PAUSE_SEC * attempt)
        raise last_exc

    def fetch_ohlcv(self, symbol: str, timeframe: str, limit: int) -> pd.DataFrame:
        """Закрытые свечи (последняя, недоформированная, отброшена)."""
        raw = self._retry(self.client.fetch_ohlcv, symbol, timeframe, limit=limit)
        df = pd.DataFrame(raw, columns=["ts", "open", "high", "low", "close", "volume"])
        df["ts"] = pd.to_datetime(df["ts"], unit="ms", utc=True)
        return df.iloc[:-1].reset_index(drop=True)

    def last_price(self, symbol: str) -> float:
        return float(self._retry(self.client.fetch_ticker, symbol)["last"])

    def quote_balance(self, quote: str = "USDT") -> float:
        bal = self._retry(self.client.fetch_balance)
        return float(bal.get(quote, {}).get("free", 0.0))

    def amount_to_precision(self, symbol: str, amount: float) -> float:
        return float(self.client.amount_to_precision(symbol, amount))

    def market_buy(self, symbol: str, amount: float) -> dict:
        amount = self.amount_to_precision(symbol, amount)
        order = self._retry(self.client.create_market_buy_order, symbol, amount)
        log.info("BUY %s %s -> id=%s", symbol, amount, order.get("id"))
        return order

    def market_sell(self, symbol: str, amount: float) -> dict:
        amount = self.amount_to_precision(symbol, amount)
        order = self._retry(self.client.create_market_sell_order, symbol, amount)
        log.info("SELL %s %s -> id=%s", symbol, amount, order.get("id"))
        return order
