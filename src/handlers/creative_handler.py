"""Creative mode handler - AI-powered idea generation with Yandex GPT."""

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from src.config import YANDEX_GPT_API_KEY, YANDEX_FOLDER_ID
from src.utils import YandexGPTClient

logger = logging.getLogger(__name__)

# Global GPT client instance (initialized once)
gpt_client = None


def get_gpt_client() -> YandexGPTClient:
    """Get or create GPT client instance."""
    global gpt_client
    if gpt_client is None:
        if not YANDEX_GPT_API_KEY or not YANDEX_FOLDER_ID:
            logger.warning("Yandex GPT credentials not configured")
            return None
        gpt_client = YandexGPTClient(YANDEX_GPT_API_KEY, YANDEX_FOLDER_ID)
    return gpt_client


async def creative_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show creative mode menu - start context collection."""
    query = update.callback_query
    await query.answer()
    
    # Initialize context collection
    context.user_data['creative_context'] = {}
    context.user_data['creative_step'] = 1
    
    message = """💡 **Генератор идей проектов**

Давай придумаем проект специально для тебя!

Я задам тебе 3 быстрых вопроса, чтобы понять твои интересы и цели.

**Вопрос 1 из 3:**
Для кого будет этот проект?"""
    
    keyboard = [
        [InlineKeyboardButton("🎓 Для себя (учеба/хобби)", callback_data="target_self")],
        [InlineKeyboardButton("💼 Для работы/организации", callback_data="target_work")],
        [InlineKeyboardButton("🚀 Для бизнеса/стартапа", callback_data="target_business")],
        [InlineKeyboardButton("🔙 В главное меню", callback_data="back_to_main")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(message, reply_markup=reply_markup, parse_mode='Markdown')
    
    return 4  # CREATIVE_INPUT state


async def handle_target_audience(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle target audience selection (Question 1)."""
    query = update.callback_query
    await query.answer()
    
    # Map callback data to audience text
    audience_map = {
        "target_self": "Для себя (учеба/хобби)",
        "target_work": "Для работы/организации",
        "target_business": "Для бизнеса/стартапа"
    }
    
    audience = audience_map.get(query.data, "не указано")
    context.user_data['creative_context']['target_audience'] = audience
    context.user_data['creative_step'] = 2
    
    message = """✅ Отлично!

**Вопрос 2 из 3:**
Расскажи, какую проблему хочешь решить или что хочешь создать?

💬 Напиши своими словами:
_Например: "Хочу сайт для книжного клуба" или "Нужна автоматизация отчетов"_"""
    
    keyboard = [
        [InlineKeyboardButton("🔙 Назад", callback_data="mode_creative")],
        [InlineKeyboardButton("🏠 В главное меню", callback_data="back_to_main")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(message, reply_markup=reply_markup, parse_mode='Markdown')
    
    return 4  # Stay in CREATIVE_INPUT state


async def handle_problem_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle problem/goal text input (Question 2)."""
    user_input = update.message.text
    
    # Save problem description
    context.user_data['creative_context']['problem'] = user_input
    context.user_data['creative_step'] = 3
    
    message = """✅ Понял!

**Вопрос 3 из 3:**
Какой тип проекта тебе интереснее?"""
    
    keyboard = [
        [InlineKeyboardButton("🌐 Веб-сайт", callback_data="tech_web")],
        [InlineKeyboardButton("🤖 Телеграм-бот", callback_data="tech_bot")],
        [InlineKeyboardButton("📱 Мобильное приложение", callback_data="tech_mobile")],
        [InlineKeyboardButton("❓ Не знаю, посоветуй", callback_data="tech_any")],
        [InlineKeyboardButton("🏠 В главное меню", callback_data="back_to_main")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(message, reply_markup=reply_markup, parse_mode='Markdown')
    
    return 4  # Stay in CREATIVE_INPUT state


async def handle_tech_preference(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle tech preference selection (Question 3) and generate ideas."""
    query = update.callback_query
    await query.answer()
    
    # Map callback data to tech preference text
    tech_map = {
        "tech_web": "Веб-сайт",
        "tech_bot": "Телеграм-бот",
        "tech_mobile": "Мобильное приложение",
        "tech_any": "Не знаю, посоветуй"
    }
    
    tech = tech_map.get(query.data, "не указано")
    context.user_data['creative_context']['tech_preference'] = tech
    
    # Show loading message
    loading_message = """⏳ **Обрабатываю твой запрос...**

Генерирую идеи специально для тебя. Это займет несколько секунд...

🤖 AI думает..."""
    
    await query.edit_message_text(loading_message, parse_mode='Markdown')
    
    # Get GPT client
    client = get_gpt_client()
    
    if not client:
        # API credentials not configured - show helpful message
        error_message = """⚠️ **Режим AI временно недоступен**

Для работы генератора идей нужны API ключи Yandex GPT.

**Как получить доступ:**
1. Зарегистрируйся на cloud.yandex.ru
2. Создай API ключ для Yandex GPT
3. Добавь ключ в .env файл бота

А пока предлагаю изучить основы создания проектов →"""
        
        keyboard = [
            [InlineKeyboardButton("📚 Изучить основы", callback_data="mode_educational")],
            [InlineKeyboardButton("🏠 В главное меню", callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(error_message, reply_markup=reply_markup, parse_mode='Markdown')
        return 1  # Return to MODE_SELECTION
    
    # Generate ideas using Yandex GPT
    user_id = update.effective_user.id
    creative_context = context.user_data['creative_context']
    
    result = await client.generate_ideas(user_id, creative_context)
    
    if result.get("error"):
        # Handle errors
        error_msg = result.get("message", "❌ Неизвестная ошибка")
        
        if result.get("error") == "rate_limit":
            # Rate limit error - show when can retry
            keyboard = [
                [InlineKeyboardButton("📚 Изучить основы", callback_data="mode_educational")],
                [InlineKeyboardButton("🏠 В главное меню", callback_data="back_to_main")]
            ]
        else:
            # Other errors - offer to try again
            keyboard = [
                [InlineKeyboardButton("🔄 Попробовать еще раз", callback_data="mode_creative")],
                [InlineKeyboardButton("📚 Изучить основы", callback_data="mode_educational")],
                [InlineKeyboardButton("🏠 В главное меню", callback_data="back_to_main")]
            ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(error_msg, reply_markup=reply_markup, parse_mode='Markdown')
        return 1  # Return to MODE_SELECTION
    
    # Success - format and show ideas
    ideas = result['ideas']
    formatted_message = client.format_ideas_for_telegram(ideas)
    
    keyboard = [
        [InlineKeyboardButton("💡 Еще идеи", callback_data="mode_creative")],
        [InlineKeyboardButton("📚 Изучить основы", callback_data="mode_educational")],
        [InlineKeyboardButton("🏠 В главное меню", callback_data="back_to_main")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(formatted_message, reply_markup=reply_markup, parse_mode='Markdown')
    
    logger.info(f"Successfully generated and displayed {len(ideas)} ideas for user {user_id}")
    
    return 1  # Return to MODE_SELECTION


async def process_creative_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Route creative input based on current step."""
    step = context.user_data.get('creative_step', 1)
    
    if step == 2:
        # Expecting problem description text
        return await handle_problem_input(update, context)
    else:
        # Unexpected text input - guide user
        message = """💬 Пожалуйста, используй кнопки для выбора вариантов, или введи описание проблемы, когда бот попросит."""
        await update.message.reply_text(message)
        return 4  # Stay in current state
