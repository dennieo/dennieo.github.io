# Trading Bot — автоматический спотовый бот для Binance

Автономный торговый бот: сам получает данные, анализирует (EMA-кроссовер + RSI + ATR-стопы),
принимает решения, исполняет сделки и ведёт учёт. Три режима — `paper` (симуляция),
`testnet` (тестнет Binance), `live` (реальные деньги) — с одним и тем же кодом стратегии.

**Полное описание архитектуры, алгоритма и плана внедрения:** [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)

> ⚠️ Ничто здесь не является финансовым советом. Торгуйте только суммой,
> потерю которой готовы принять полностью. Начинайте с `paper` и бэктеста.

## Быстрый старт

```bash
cd trading-bot
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

### 1. Бэктест (первым делом)

```bash
python -m backtest.backtest --symbol BTC/USDT --days 365
```

Покажет доходность против buy&hold, просадку, winrate, profit factor.
Параметры стратегии — в `config.yaml`.

### 2. Paper trading (без денег и без ключей)

В `config.yaml` уже стоит `mode: paper`:

```bash
python -m bot.main
```

Бот торгует виртуальными $500 на реальных ценах. Состояние — в `data/bot.db`.

### 3. Testnet

Зарегистрируйтесь на https://testnet.binance.vision, получите ключи,
скопируйте `.env.example` → `.env`, заполните ключи, поставьте `mode: testnet`.

### 4. Live (только после этапов 1–3)

Ключи с **только** «Reading» + «Spot Trading» (без вывода средств!), IP-whitelist,
небольшой баланс ($100–300), `mode: live`.

## Управление

- **Остановить новые входы:** создать файл `STOP` в папке бота (`touch STOP`).
- **Уведомления в Telegram:** `telegram.enabled: true` + токен/чат в `.env`.
- **Docker:** `docker build -t trading-bot . && docker run -d --restart unless-stopped --env-file .env -v $(pwd)/data:/app/data trading-bot`

## Структура

```
bot/            главный цикл, биржа, стратегия, риск, исполнение, состояние
backtest/       бэктестер на тех же функциях стратегии
docs/           ARCHITECTURE.md — paper с полным описанием
config.yaml     все параметры (режим, символы, стратегия, риск)
```

## Вынос в отдельный репозиторий

Проект самодостаточен внутри `trading-bot/`. Чтобы вынести:

```bash
mkdir ../trading-bot-repo && cp -r trading-bot/* trading-bot/.gitignore ../trading-bot-repo
cd ../trading-bot-repo && git init && git add -A && git commit -m "Initial commit"
# создайте ПРИВАТНЫЙ репозиторий на GitHub и запушьте
```

Репозиторий с торговым ботом лучше держать **приватным**.
