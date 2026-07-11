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

## Smart-money трекер (альтернативная стратегия)

Следование за кошельками успешных трейдеров Hyperliquid: скоринг по публичной
истории сделок, сигнал при консенсусе ≥3 умных кошельков в лонге.
Подробности и другие нестандартные подходы: [docs/ALT_STRATEGIES.md](docs/ALT_STRATEGIES.md).

```bash
python -m smartmoney.main    # режим наблюдения: только сигналы в лог/Telegram
```

Кошельки берутся из лидерборда автоматически или задаются в `config.yaml`
(`smartmoney.wallets`). Автоисполнение сигналов на споте Binance —
`smartmoney.auto_trade: true` (начинайте с `mode: paper`).

## Совместный автономный запуск обоих ботов

```bash
docker compose up -d --build     # trend-bot + smartmoney-bot, авторестарт 24/7
```

Боты независимы (отдельные SQLite-базы), но живут на общей инфраструктуре:

- **Общий kill switch:** `touch data/STOP` — оба бота прекращают новые входы.
- **Бюджеты на общем счёте (live):** `risk.budget_usdt` и `smartmoney.budget_usdt`
  делят реальный баланс между ботами (например 200 + 100 USDT) — ни один
  не заберёт весь счёт. `0` = без лимита (если бот работает один).
- В `paper`-режиме у каждого свой виртуальный баланс — конфликтов нет.
- **Связка анализаторов:** smart-money бот каждую минуту публикует свой анализ
  (сколько умных кошельков в лонге) в `data/consensus.json`, а трендовый бот при
  `smartmoney_filter.enabled: true` покупает **только когда согласны оба**:
  и индикаторы, и умные деньги. Если smart-money бот выключен или данные
  устарели, фильтр мягко отключается — трендовый бот остаётся автономным.

## Управление

- **Остановить новые входы:** `touch data/STOP` (действует на всех ботов).
- **Уведомления в Telegram:** `telegram.enabled: true` + токен/чат в `.env`.
- **Один бот в Docker:** `docker build -t trading-bot . && docker run -d --restart unless-stopped --env-file .env -v $(pwd)/data:/app/data trading-bot`

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
