"""Индикаторы — чистые функции над pandas. Общие для бота и бэктестера."""
import pandas as pd


def ema(close: pd.Series, period: int) -> pd.Series:
    return close.ewm(span=period, adjust=False).mean()


def rsi(close: pd.Series, period: int = 14) -> pd.Series:
    delta = close.diff()
    gain = delta.clip(lower=0).ewm(alpha=1 / period, adjust=False).mean()
    loss = (-delta.clip(upper=0)).ewm(alpha=1 / period, adjust=False).mean()
    rs = gain / loss.replace(0, 1e-12)
    return 100 - 100 / (1 + rs)


def atr(df: pd.DataFrame, period: int = 14) -> pd.Series:
    """df: колонки high, low, close."""
    prev_close = df["close"].shift(1)
    tr = pd.concat(
        [
            df["high"] - df["low"],
            (df["high"] - prev_close).abs(),
            (df["low"] - prev_close).abs(),
        ],
        axis=1,
    ).max(axis=1)
    return tr.ewm(alpha=1 / period, adjust=False).mean()


def adx(df: pd.DataFrame, period: int = 14) -> pd.Series:
    """ADX (Wilder) — сила тренда: >25 тренд, <20 боковик."""
    up = df["high"].diff()
    down = -df["low"].diff()
    plus_dm = ((up > down) & (up > 0)) * up
    minus_dm = ((down > up) & (down > 0)) * down

    prev_close = df["close"].shift(1)
    tr = pd.concat(
        [
            df["high"] - df["low"],
            (df["high"] - prev_close).abs(),
            (df["low"] - prev_close).abs(),
        ],
        axis=1,
    ).max(axis=1)

    alpha = 1 / period
    atr_w = tr.ewm(alpha=alpha, adjust=False).mean().replace(0, 1e-12)
    plus_di = 100 * plus_dm.ewm(alpha=alpha, adjust=False).mean() / atr_w
    minus_di = 100 * minus_dm.ewm(alpha=alpha, adjust=False).mean() / atr_w
    dx = 100 * (plus_di - minus_di).abs() / (plus_di + minus_di).replace(0, 1e-12)
    return dx.ewm(alpha=alpha, adjust=False).mean()


def add_indicators(df: pd.DataFrame, params: dict) -> pd.DataFrame:
    """Добавляет колонки ema_fast, ema_slow, rsi, atr, adx к OHLCV-датафрейму."""
    out = df.copy()
    out["ema_fast"] = ema(out["close"], params["ema_fast"])
    out["ema_slow"] = ema(out["close"], params["ema_slow"])
    out["rsi"] = rsi(out["close"], params["rsi_period"])
    out["atr"] = atr(out, params["atr_period"])
    out["adx"] = adx(out, params["adx_period"])
    return out
