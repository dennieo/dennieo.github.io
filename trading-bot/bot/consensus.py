"""Обмен анализом между ботами через общий файл консенсуса (data/consensus.json).

Smart-money бот каждый тик записывает сюда свой анализ: сколько умных
кошельков в лонге по каждой монете. Трендовый бот (v1) может использовать
это как фильтр входа — покупать только при поддержке умных денег.
Файл на общем томе data/ — работает и между Docker-контейнерами.
"""
import json
import logging
import time
from pathlib import Path

log = logging.getLogger("consensus")


def write_consensus(path: str, longs: dict[str, int], total_wallets: int):
    """Атомарная запись снапшота консенсуса (tmp + rename)."""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(".tmp")
    tmp.write_text(json.dumps(
        {"ts": time.time(), "longs": longs, "total_wallets": total_wallets}
    ))
    tmp.replace(p)


def read_consensus(path: str, max_age_sec: float) -> dict | None:
    """Снапшот консенсуса или None, если файла нет / устарел / битый."""
    try:
        data = json.loads(Path(path).read_text())
        if time.time() - float(data["ts"]) > max_age_sec:
            return None
        return data
    except (OSError, ValueError, KeyError):
        return None


def entry_allowed_by_smartmoney(flt: dict, symbol: str) -> tuple[bool, str]:
    """Фильтр входа для трендового бота.

    flt — секция smartmoney_filter конфига. Fail-open: если фильтр выключен
    или данные консенсуса недоступны/устарели (smart-money бот не запущен),
    вход разрешается с предупреждением — трендовый бот остаётся автономным.
    """
    if not flt.get("enabled"):
        return True, ""
    coin = symbol.split("/")[0]
    data = read_consensus(flt["consensus_file"], flt["max_age_min"] * 60)
    if data is None:
        log.warning("Консенсус умных денег недоступен/устарел — вход без фильтра")
        return True, ""
    longs = int(data["longs"].get(coin, 0))
    need = int(flt["min_longs"])
    if longs < need:
        return False, f"smart-money фильтр: в лонге {longs} кошельков, нужно >= {need}"
    return True, f"smart-money за: {longs}/{data['total_wallets']} кошельков в лонге"
