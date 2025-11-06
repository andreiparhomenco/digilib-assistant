# Changelog

## [0.4.1] - 2025-11-06

### Added
- ✅ Yandex GPT API integration fully tested and working
- ✅ Creative Mode now generates real AI-powered project ideas
- ✅ Rate limiting implemented (10 requests/hour, 50/day per user)
- ✅ Full Russian localization

### Changed
- ⬆️ Updated python-telegram-bot to 22.5 (from 20.7)
- ⬆️ Updated aiohttp to 3.13+ for Python 3.13 compatibility
- 🔧 Fixed compatibility issues with latest dependencies

### Fixed
- 🐛 Resolved `Updater` attribute error in python-telegram-bot
- 🐛 Fixed aiohttp installation on Windows with Python 3.13
- 🐛 Fixed module import issues

### Technical Details
- **Python:** 3.13.0
- **python-telegram-bot:** 22.5
- **aiohttp:** 3.13.2+
- **Telegram Bot:** Working ✅
- **Yandex GPT:** Configured ✅

## [0.4.0] - 2025-11-06

### Added
- 🎉 Initial release
- 📚 Educational Mode with 6 topics (Cursor, GitHub, Git, Integration, Push, Railway)
- 💡 Creative Mode structure (Yandex GPT placeholder)
- 🎯 Hierarchical menu navigation (3 levels)
- ⚡ ConversationHandler state machine
- 🎨 Analogy-First content format
- 📝 Comprehensive documentation

### Features
- ✅ 6 educational topics with beginner-friendly content
- ✅ Button-based navigation
- ✅ Command support (/start, /help, /cancel)
- ✅ Error handling and logging
- ✅ .env configuration support

