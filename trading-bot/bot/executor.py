"""Исполнение сделок.

paper   — симуляция: виртуальный кэш в SQLite, исполнение по последней цене
          с учётом комиссии;
testnet / live — рыночные ордера через API биржи.
"""
import logging

log = logging.getLogger("executor")

CASH_KEY = "paper_cash_usdt"


class Executor:
    def __init__(self, cfg, exchange, state):
        self.cfg = cfg
        self.ex = exchange
        self.state = state
        self.paper = cfg.mode == "paper"
        self.fee = cfg.paper["fee_pct"] / 100
        if self.paper and self.state.kv_get(CASH_KEY) is None:
            self.state.kv_set(CASH_KEY, str(cfg.paper["starting_balance_usdt"]))

    def cash(self) -> float:
        """Свободный кэш в котируемой валюте (USDT)."""
        if self.paper:
            return float(self.state.kv_get(CASH_KEY))
        return self.ex.quote_balance("USDT")

    def open_long(self, symbol: str, qty: float, price: float) -> float:
        """Покупка. Возвращает фактическую цену исполнения."""
        if self.paper:
            cost = qty * price * (1 + self.fee)
            self.state.kv_set(CASH_KEY, str(self.cash() - cost))
            log.info("[paper] BUY %s qty=%.8f по %.2f (cost %.2f)", symbol, qty, price, cost)
            return price
        order = self.ex.market_buy(symbol, qty)
        return float(order.get("average") or order.get("price") or price)

    def close_long(self, symbol: str, qty: float, price: float) -> float:
        """Продажа всей позиции. Возвращает фактическую цену исполнения."""
        if self.paper:
            proceeds = qty * price * (1 - self.fee)
            self.state.kv_set(CASH_KEY, str(self.cash() + proceeds))
            log.info("[paper] SELL %s qty=%.8f по %.2f (proceeds %.2f)", symbol, qty, price, proceeds)
            return price
        order = self.ex.market_sell(symbol, qty)
        return float(order.get("average") or order.get("price") or price)
