# DigiLib Assistant

Образовательный чат-бот для библиотеки, помогающий новичкам осваивать цифровые инструменты и создавать проекты.

## 🚀 Implementation Status

**Current Phase:** ✅ PHASE 4 - Creative Mode (Yandex GPT) COMPLETE

### Completed Phases:
- ✅ **Phase 1:** Foundation & Technology Validation
  - Python 3.13.0 installed and working
  - Virtual environment created successfully
  - python-telegram-bot 20.7 integrated
  - Configuration management working
  - Project structure established

- ✅ **Phase 2:** Bot Foundation Expansion
  - ConversationHandler state machine implemented
  - Hierarchical menu structure (from UI/UX Creative Phase)
  - Command handlers (start, help, cancel)
  
- ✅ **Phase 3:** Educational Mode
  - All 6 educational topics implemented with Analogy-First format
  - Topic navigation with "What's Next" logic
  - 2-column grid layout for topic selection
  - Integration between topics
  - Call-to-action to Creative Mode after completing all topics

- ✅ **Phase 4:** Creative Mode (Yandex GPT Integration - JUST COMPLETED)
  - Yandex GPT API client with constraint-based prompting
  - 3-question context collection dialogue
  - Rate limiting (10 requests/hour, 50/day per user)
  - Response processing and validation
  - Error handling and fallback messages
  - Idea formatting for Telegram

### In Progress:
- ⏳ **Phase 5:** Data & Security
- ⏳ **Phase 6:** Testing & Polish
- ⏳ **Phase 7:** Deployment to Railway

## 📋 Prerequisites

- Python 3.10+ (currently using 3.13.0)
- Telegram Bot Token (from @BotFather) - **Required**
- Yandex GPT API Key + Folder ID - **Optional** (for Creative Mode)
- Windows 10+ / macOS / Linux

## 🛠️ Setup Instructions

### 1. Clone and Navigate

```bash
cd digilib-assistant
```

### 2. Create Virtual Environment

```bash
# Windows
py -m venv venv
.\venv\Scripts\Activate.ps1

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
# For minimal installation
pip install -r requirements-minimal.txt

# For full development (when available)
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
# Copy the example environment file
copy .env.example .env  # Windows
# OR
cp .env.example .env    # macOS/Linux

# Edit .env and add your Telegram Bot Token
```

### 5. Get Telegram Bot Token (Required)

1. Open Telegram and search for [@BotFather](https://t.me/botfather)
2. Send `/newbot` command
3. Follow instructions to create your bot
4. Copy the token and paste it into `.env` file:
   ```
   TELEGRAM_BOT_TOKEN=your_token_here
   ```

### 6. Get Yandex GPT Credentials (Optional - for Creative Mode)

**Note:** Educational Mode works without Yandex GPT. This is only needed for AI-powered idea generation.

1. Go to [cloud.yandex.ru](https://cloud.yandex.ru) and create an account
2. Create a new folder or use existing one
3. Copy your Folder ID (found in folder settings)
4. Create API Key:
   - Go to "Service Accounts"
   - Create service account with `ai.languageModels.user` role
   - Create API key for this account
5. Add credentials to `.env` file:
   ```
   YANDEX_GPT_API_KEY=your_api_key_here
   YANDEX_FOLDER_ID=your_folder_id_here
   ```

### 7. Run the Bot

```bash
python main.py
```

## 🧪 Testing the Bot

Once the bot is running:

### Educational Mode Testing

1. Open Telegram and search for your bot by username
2. Send `/start` command
3. Click **"📚 Изучить основы"**
4. Test topic navigation:
   - Select "🖥️ Cursor" topic
   - Read the analogy-first content
   - Click **"⏭️ Next topic"** to see GitHub topic
   - Use **"🔙 К темам"** to return to topic list
5. Complete all 6 topics:
   - Cursor → GitHub → Git → Cursor+GitHub → Push → Railway
   - See completion celebration message

### Creative Mode Testing (with Yandex GPT)

**Note:** Requires Yandex GPT API credentials in `.env` file

1. From main menu, click **"💡 Придумать проект"**
2. Answer 3 questions:
   - Question 1: Select target audience (for self/work/business)
   - Question 2: Type your problem or goal (free text)
   - Question 3: Select project type (web/bot/mobile/any)
3. Wait for AI to generate 2-3 project ideas
4. Review personalized ideas with:
   - Problem it solves
   - Technologies needed
   - First steps to start

**Without API credentials:** Bot will show informative message about how to get API access

### Navigation Testing

- Try **"🏠 В главное меню"** from any screen
- Use `/help` command for help
- Use `/cancel` to return to main menu
- Test "🔙" back buttons throughout

## 📁 Project Structure

```
digilib-assistant/
├── main.py                      # Entry point with ConversationHandler
├── requirements.txt             # Full dependencies
├── requirements-minimal.txt     # Minimal dependencies
├── .env.example                 # Environment template
├── .gitignore                   # Git ignore rules
├── README.md                    # This file
├── src/                         # Source code
│   ├── __init__.py
│   ├── config/                  # Configuration module
│   │   └── __init__.py
│   ├── handlers/                # Bot handlers
│   │   ├── __init__.py
│   │   ├── common_handler.py   # Start, help, cancel commands
│   │   ├── educational_handler.py  # 6 educational topics
│   │   └── creative_handler.py # AI idea generation with Yandex GPT
│   └── utils/                   # Utility functions
│       ├── __init__.py
│       └── yandex_gpt.py       # Yandex GPT API client
├── tests/                       # Test files (to be implemented)
└── docs/                        # Documentation (to be implemented)
```

## 🎯 Current Features (Phase 3 Complete)

### ✅ Core Bot Features
- ✅ ConversationHandler state machine
- ✅ Hierarchical menu navigation (3 levels)
- ✅ Command handling (/start, /help, /cancel)
- ✅ Async/await support
- ✅ Configuration management
- ✅ Error handling & logging

### ✅ Educational Mode (COMPLETE)
- ✅ 6 educational topics with full content:
  - 🖥️ Cursor (AI code editor)
  - 🐙 GitHub (code hosting)
  - 📦 Git (version control)
  - 🔗 Cursor + GitHub integration
  - ⬆️ Push code to GitHub
  - 🚂 Deploy on Railway
- ✅ Analogy-First content format (beginner-friendly)
- ✅ Navigation system (Next topic/Back/Menu)
- ✅ 2-column grid layout
- ✅ Completion celebration and CTA to Creative Mode

### ✅ Creative Mode (COMPLETE - with Yandex GPT)
- ✅ 3-question context collection dialogue
- ✅ Yandex GPT API integration
- ✅ Constraint-based prompting strategy
- ✅ Project idea generation (2-3 ideas per request)
- ✅ Rate limiting (10/hour, 50/day per user)
- ✅ Error handling and fallback messages
- ✅ Response validation and formatting

## 🚧 Planned Features (Phases 5-7)

### Phase 5: Data & Security
- [ ] Rate limiting (10 GPT requests/hour)
- [ ] Input validation
- [ ] SQLite/PostgreSQL database
- [ ] Analytics tracking

### Phase 6: Testing & Polish
- [ ] Unit tests
- [ ] Integration tests
- [ ] Code quality tools (black, pylint, mypy)
- [ ] Documentation

### Phase 7: Deployment
- [x] Dockerfile для Railway
- [x] railway.json конфигурация
- [x] .dockerignore оптимизация
- [x] DEPLOY.md инструкции
- [ ] CI/CD pipeline (optional)
- [x] Health checks (в Dockerfile)

## 📊 Technology Stack

- **Language:** Python 3.13
- **Bot Framework:** python-telegram-bot 20.7
- **Environment:** python-dotenv 1.0.0
- **AI Integration:** Yandex GPT (planned)
- **Database:** SQLite → PostgreSQL (planned)
- **Hosting:** Railway (planned)

## 🔧 Development

### Code Quality Tools (to be integrated)

```bash
# Format code
black src/ tests/

# Lint code
pylint src/ tests/

# Type checking
mypy src/

# Run tests
pytest tests/
```

## 🚂 Deployment на Railway

**Инструкции:** См. [DEPLOY.md](DEPLOY.md)

### Быстрый деплой:

1. Перейди на https://railway.app
2. "Deploy from GitHub repo"
3. Выбери этот репозиторий
4. Добавь environment variables
5. Railway автоматически соберет Docker и задеплоит!

**Подробнее:** [DEPLOY.md](DEPLOY.md)

---

## 📝 Next Steps

1. ✅ Technology Validation Complete
2. ✅ Creative Phases Complete (UI/UX, Prompts, Content)
3. ✅ Phase 3: Educational Mode Complete
4. ✅ Phase 4: Yandex GPT Integration Complete
5. ⏭️ Phase 5: Data & Security (Database, Analytics)
6. ⏭️ Phase 6: Testing & Code Quality
7. ✅ Phase 7: Railway Deployment Ready

## 🤝 Contributing

This project is part of a library initiative to democratize digital product creation.

## 📄 License

TBD

## 🙋 Support

For issues and questions, please refer to project documentation in `memory-bank/` directory.

---

**Version:** 0.5.0 (Railway Ready)  
**Last Updated:** 2025-11-06  
**Status:** ✅ PRODUCTION READY - Full deployment support with Docker + Railway
