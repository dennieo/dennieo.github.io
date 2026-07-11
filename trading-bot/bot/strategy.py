"""Стратегии и выбор по режиму рынка.

- trend:          EMA-кроссовер + RSI-фильтр — зарабатывает на трендах;
- mean_reversion: разворот RSI из перепроданности — зарабатывает на боковике;
- auto:           определяем режим рынка по ADX и включаем подходящую.

Чистые функции: свечи с индикаторами -> решение. Ничего не знают про
деньги и биржу — одинаково работают в бэктесте, оптимизаторе и вживую.
"""
from enum import Enum

import pandas as pd


class Signal(str, Enum):
    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"


def detect_regime(df: pd.DataFrame, params: dict) -> str:
    """'trend' или 'range' по силе тренда (ADX)."""
    if df.empty:
        return "range"
    return "trend" if float(df["adx"].iloc[-1]) >= params["adx_trend_min"] else "range"


def signal_trend(df: pd.DataFrame, params: dict) -> Signal:
    """Кроссовер EMA на последней закрытой свече + RSI-фильтр перегретости."""
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


def signal_mean_reversion(df: pd.DataFrame, params: dict) -> Signal:
    """Покупка разворота из перепроданности, выход при возврате RSI к середине."""
    if len(df) < 2:
        return Signal.HOLD
    prev, last = df.iloc[-2], df.iloc[-1]
    if prev["rsi"] < params["mr_rsi_entry"] <= last["rsi"]:
        return Signal.BUY
    if last["rsi"] >= params["mr_rsi_exit"]:
        return Signal.SELL
    return Signal.HOLD


def entry_decision(df: pd.DataFrame, params: dict) -> tuple[bool, str]:
    """(входить?, имя стратегии). mode: trend | mean_reversion | auto."""
    mode = params.get("mode", "trend")
    regime = detect_regime(df, params)
    if mode == "trend" or (mode == "auto" and regime == "trend"):
        if signal_trend(df, params) == Signal.BUY:
            return True, "trend"
    if mode == "mean_reversion" or (mode == "auto" and regime == "range"):
        if signal_mean_reversion(df, params) == Signal.BUY:
            return True, "mean_reversion"
    return False, ""


def exit_decision(df: pd.DataFrame, params: dict, strategy_name: str) -> bool:
    """Выходить ли из позиции по сигналу той стратегии, что её открыла."""
    if strategy_name == "mean_reversion":
        return signal_mean_reversion(df, params) == Signal.SELL
    return signal_trend(df, params) == Signal.SELL


# обратная совместимость: сигнал трендовой стратегии
generate_signal = signal_trend


def stop_and_take(entry_price: float, atr_value: float, risk_params: dict) -> tuple[float, float]:
    """Возвращает (stop_loss, take_profit) от цены входа и ATR."""
    stop = entry_price - risk_params["stop_atr_mult"] * atr_value
    take = entry_price + risk_params["take_profit_atr_mult"] * atr_value
    return stop, take
