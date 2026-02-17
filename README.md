# Telegram profit bot (MVP)

Минимальный MVP бота для учёта дохода и комиссии в рамках сессии в супергруппе Telegram.

Запуск в контейнере:

```bash
cp .env.example .env
# заполните BOT_TOKEN и WEBHOOK_URL
docker compose up --build
```

Файлы:

- `app/` — исходники
- `Dockerfile`, `docker-compose.yml`, `.env.example`, `requirements.txt`
