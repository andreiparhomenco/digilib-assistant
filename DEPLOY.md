# 🚂 Деплой на Railway

## Быстрый старт

### Вариант 1: Deploy через GitHub (рекомендуется)

1. **Перейди на Railway:**
   - https://railway.app
   - Нажми "Start a New Project"

2. **Подключи GitHub:**
   - Выбери "Deploy from GitHub repo"
   - Авторизуй Railway в GitHub
   - Выбери репозиторий `andreiparhomenco/digilib-assistant`

3. **Railway автоматически:**
   - ✅ Обнаружит Dockerfile
   - ✅ Построит Docker образ
   - ✅ Запустит контейнер

4. **Добавь Environment Variables:**
   ```
   TELEGRAM_BOT_TOKEN=твой_токен
   YANDEX_GPT_API_KEY=твой_ключ
   YANDEX_FOLDER_ID=твой_folder_id
   DEBUG=False
   LOG_LEVEL=INFO
   ```

5. **Deploy завершен!** 🎉

---

## Вариант 2: Deploy через Railway CLI

### Установка Railway CLI

```bash
# Windows (PowerShell)
iwr https://railway.app/install.ps1 | iex

# macOS/Linux
sh <(curl -sSL https://railway.app/install.sh)
```

### Деплой

```bash
# 1. Войди в аккаунт
railway login

# 2. Создай новый проект
railway init

# 3. Добавь переменные окружения
railway variables set TELEGRAM_BOT_TOKEN="твой_токен"
railway variables set YANDEX_GPT_API_KEY="твой_ключ"
railway variables set YANDEX_FOLDER_ID="твой_folder_id"
railway variables set DEBUG="False"
railway variables set LOG_LEVEL="INFO"

# 4. Deploy
railway up
```

---

## 🔧 Настройка переменных окружения

В Railway Dashboard → Variables → RAW Editor:

```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
YANDEX_GPT_API_KEY=your_yandex_gpt_api_key_here
YANDEX_FOLDER_ID=your_folder_id_here
DEBUG=False
LOG_LEVEL=INFO
GPT_REQUESTS_PER_HOUR=10
GPT_REQUESTS_PER_DAY=50
```

---

## 📊 Мониторинг

### Логи

```bash
# Через CLI
railway logs

# Через Dashboard
railway.app → твой проект → Logs
```

### Статус

```bash
# Проверить статус
railway status

# Информация о проекте
railway info
```

---

## 🔄 Обновление

### Автоматическое (через GitHub)

1. Сделай изменения в коде
2. Закоммить и запушь в GitHub
3. Railway автоматически пересоберет и задеплоит

### Ручное (через CLI)

```bash
railway up
```

---

## 💰 Стоимость

**Free Plan (хватит для старта):**
- $5 бесплатных кредитов в месяц
- 500 часов выполнения
- 512 MB RAM
- 1 GB диск

**Hobby Plan ($5/месяц):**
- $5 кредитов + $5/месяц
- Unlimited часов
- 8 GB RAM
- 100 GB диск

---

## 🐛 Troubleshooting

### Бот не отвечает

1. Проверь логи: `railway logs`
2. Проверь переменные: `railway variables`
3. Перезапусти: `railway restart`

### Build fails

1. Проверь Dockerfile
2. Убедись что все зависимости в requirements-minimal.txt
3. Проверь логи сборки

### Memory issues

1. Увеличь лимит в Railway Dashboard
2. Или перейди на Hobby Plan

---

## 🔗 Полезные ссылки

- 📖 Railway Docs: https://docs.railway.app
- 💬 Railway Discord: https://discord.gg/railway
- 🐛 GitHub Issues: https://github.com/andreiparhomenco/digilib-assistant/issues

---

## ✅ Checklist перед деплоем

- [ ] Все environment variables настроены
- [ ] Telegram Bot Token валиден
- [ ] Yandex GPT credentials правильные
- [ ] DEBUG=False для продакшена
- [ ] .env файл НЕ в Git (проверь .gitignore)
- [ ] Railway project создан
- [ ] GitHub репозиторий подключен

---

**После деплоя бот будет работать 24/7 на серверах Railway! 🚀**

