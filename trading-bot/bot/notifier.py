"""Уведомления в Telegram (опционально). Ошибки уведомлений не роняют бота."""
import logging
import os

import requests

log = logging.getLogger("notifier")


class Notifier:
    def __init__(self, cfg):
        tg = cfg["telegram"]
        self.enabled = bool(tg.get("enabled"))
        self.token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
        self.chat_id = os.environ.get("TELEGRAM_CHAT_ID", "")
        if self.enabled and not (self.token and self.chat_id):
            log.warning("Telegram включён, но нет TELEGRAM_BOT_TOKEN/CHAT_ID — выключаю")
            self.enabled = False

    def send(self, text: str):
        log.info("NOTIFY: %s", text)
        if not self.enabled:
            return
        try:
            requests.post(
                f"https://api.telegram.org/bot{self.token}/sendMessage",
                json={"chat_id": self.chat_id, "text": text},
                timeout=10,
            )
        except Exception as e:  # noqa: BLE001 — уведомление не должно ронять бота
            log.warning("Не удалось отправить в Telegram: %s", e)
