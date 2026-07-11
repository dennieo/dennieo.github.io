"""Загрузка конфигурации: config.yaml + секреты из .env."""
import os
from dataclasses import dataclass, field
from pathlib import Path

import yaml
from dotenv import load_dotenv


@dataclass
class Config:
    raw: dict = field(default_factory=dict)

    @property
    def mode(self) -> str:
        return self.raw["mode"]

    @property
    def symbols(self) -> list[str]:
        return self.raw["symbols"]

    @property
    def timeframe(self) -> str:
        return self.raw["timeframe"]

    @property
    def strategy(self) -> dict:
        return self.raw["strategy"]

    @property
    def risk(self) -> dict:
        return self.raw["risk"]

    @property
    def paper(self) -> dict:
        return self.raw["paper"]

    def __getitem__(self, key):
        return self.raw[key]

    @property
    def api_key(self) -> str:
        return os.environ.get("BINANCE_API_KEY", "")

    @property
    def api_secret(self) -> str:
        return os.environ.get("BINANCE_API_SECRET", "")


def load_config(path: str | Path = "config.yaml") -> Config:
    load_dotenv()
    with open(path) as f:
        raw = yaml.safe_load(f)
    cfg = Config(raw=raw)
    if cfg.mode not in ("paper", "testnet", "live"):
        raise ValueError(f"Неизвестный режим: {cfg.mode}")
    if cfg.mode in ("testnet", "live") and not (cfg.api_key and cfg.api_secret):
        raise ValueError(
            f"Режим {cfg.mode} требует BINANCE_API_KEY и BINANCE_API_SECRET в .env"
        )
    return cfg
