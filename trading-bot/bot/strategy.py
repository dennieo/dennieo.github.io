"""Стратегия v1: EMA-кроссовер + RSI-фильтр.

Чистая функция: свечи с индикаторами -> сигнал. Ничего не знает про
деньги, позиции и биржу — поэтому одинаково работает в бэктесте и вживую.
"""
from enum import Enum

import pandas as pd


class Signal(str, Enum):
    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"


def generate_signal(df: pd.DataFrame, params: dict) -> Signal:
    """df — закрытые свечи с колонками ema_fast, ema_slow, rsi.
    Смотрим на две последние закрытые свечи: кроссовер = смена знака разницы EMA.
    """
    if len(df) < 2:
        return Signal.HOLD
    prev, last = df.iloc[-2], df.iloc[-1]

    crossed_up = prev["ema_fast"] <= prev["ema_slow"] and last["ema_fast"] > last["ema_slow"]
    crossed_down = prev["ema_fast"] >= prev["ema_slow"] and last["ema_fast"] < last["ema_slow"]

    if crossed_up and last["rsi"] < params["rsi_overbought"]:
        return Signal.BUY
    if crossed_down:
        return Signal.SELL
    return Signal.HOLD


def stop_and_take(entry_price: float, atr_value: float, risk_params: dict) -> tuple[float, float]:
    """Возвращает (stop_loss, take_profit) от цены входа и ATR."""
    stop = entry_price - risk_params["stop_atr_mult"] * atr_value
    take = entry_price + risk_params["take_profit_atr_mult"] * atr_value
    return stop, take
