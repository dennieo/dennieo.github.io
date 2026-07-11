FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY bot/ bot/
COPY backtest/ backtest/
COPY smartmoney/ smartmoney/
COPY config.yaml .

# состояние (SQLite) живёт на томе: -v $(pwd)/data:/app/data
VOLUME /app/data

CMD ["python", "-m", "bot.main"]
