"""Common handlers for bot commands."""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle /start command - Main menu with mode selection."""
    user = update.effective_user
    
    # Welcome message following Style Guide
    message = f"""👋 Привет, {user.first_name}!

Я DigiLib Assistant - твой проводник в мир создания цифровых решений. 🚀

**Чем займемся сегодня?**
• Изучим основы работы с современными инструментами
• Придумаем идею для твоего проекта

Просто нажми на кнопку ниже!"""

    # Hierarchical menu - Level 1: Mode Selection
    keyboard = [
        [InlineKeyboardButton("📚 Изучить основы", callback_data="mode_educational")],
        [InlineKeyboardButton("💡 Придумать проект", callback_data="mode_creative")],
        [InlineKeyboardButton("❓ Помощь", callback_data="help")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(message, reply_markup=reply_markup, parse_mode='Markdown')
    
    # Return state for ConversationHandler
    return 1  # MODE_SELECTION state


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /help command."""
    help_text = """📚 **Справка по DigiLib Assistant**

**Основные команды:**
/start - Начать работу с ботом
/help - Показать эту справку
/cancel - Отменить текущее действие

**Режимы работы:**
📚 **Изучить основы** - Пошаговые гиды по 6 темам:
  • Cursor (редактор кода с AI)
  • GitHub (платформа для кода)
  • Git (контроль версий)
  • Связка Cursor + GitHub
  • Push кода на GitHub
  • Деплой на Railway

💡 **Придумать проект** - AI поможет:
  • Сгенерировать идеи проектов
  • Подобрать технологии
  • Составить план действий

**Нужна помощь?**
Просто напиши свой вопрос, и я постараюсь помочь!"""

    # Check if called from callback query or direct command
    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.message.reply_text(help_text, parse_mode='Markdown')
    else:
        await update.message.reply_text(help_text, parse_mode='Markdown')


async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle /cancel command - Return to main menu."""
    message = """❌ Действие отменено.

Возвращаю тебя в главное меню."""

    keyboard = [
        [InlineKeyboardButton("📚 Изучить основы", callback_data="mode_educational")],
        [InlineKeyboardButton("💡 Придумать проект", callback_data="mode_creative")],
        [InlineKeyboardButton("❓ Помощь", callback_data="help")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(message, reply_markup=reply_markup)
    
    return 1  # Return to MODE_SELECTION state
