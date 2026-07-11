"""Мониторинг funding-ставок перпетуальных фьючерсов Binance.

Запуск:  python -m monitor.funding [config.yaml]

Когда рынок перегрет лонгами, лонги платят шортам funding каждые 8 часов.
Стратегия «кэрри» (лонг спот + шорт перп той же суммы) в такие периоды
даёт почти дельта-нейтральный доход. Этот монитор НЕ торгует — только
оповещает, когда годовая ставка превышает порог, чтобы вы видели моменты,
когда кэрри-этап (см. docs/ALT_STRATEGIES.md §2) становится привлекательным.
Ключи API не нужны: данные публичные.
"""
import logging
import sys
import time

import ccxt

from bot.config import load_config
from bot.notifier import Notifier

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
log = logging.getLogger("funding")

FUNDINGS_PER_YEAR = 3 * 365  # выплата каждые 8 часов


class FundingMonitor:
    def __init__(self, cfg, client=None, notifier=None):
        self.fm = cfg["funding_monitor"]
        self.notifier = notifier or Notifier(cfg)
        self.client = client or ccxt.binance(
            {"enableRateLimit": True, "options": {"defaultType": "swap"}}
        )
        self.above: set[str] = set()  # символы уже выше порога (не спамим)

    def check_once(self) -> list[dict]:
        """Возвращает новые возможности (символ пересёк порог снизу вверх)."""
        opportunities = []
        for symbol in self.fm["symbols"]:
            try:
                rate = float(self.client.fetch_funding_rate(symbol)["fundingRate"])
            except Exception as e:  # noqa: BLE001 — один символ не срывает опрос
                log.warning("Не смог получить funding %s: %s", symbol, e)
                continue
            annual_pct = rate * FUNDINGS_PER_YEAR * 100
            log.info("%s: funding %.4f%% за 8ч (~%.1f%% годовых)",
                     symbol, rate * 100, annual_pct)
            if annual_pct >= self.fm["min_annualized_pct"]:
                if symbol not in self.above:
                    self.above.add(symbol)
                    opportunities.append({"symbol": symbol, "annual_pct": annual_pct})
            else:
                self.above.discard(symbol)
        return opportunities

    def run(self):
        log.info("Мониторю funding: %s, порог %.0f%% годовых",
                 self.fm["symbols"], self.fm["min_annualized_pct"])
        while True:
            try:
                for opp in self.check_once():
                    self.notifier.send(
                        f"💰 Funding {opp['symbol']}: ~{opp['annual_pct']:.1f}% годовых. "
                        f"Кэрри (лонг спот + шорт перп) сейчас привлекателен."
                    )
            except KeyboardInterrupt:
                break
            except Exception as e:  # noqa: BLE001
                log.exception("Ошибка тика: %s", e)
            time.sleep(self.fm["poll_interval_min"] * 60)


if __name__ == "__main__":
    cfg = load_config(sys.argv[1] if len(sys.argv) > 1 else "config.yaml")
    FundingMonitor(cfg).run()
