#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
DigiLib Assistant - Telegram Bot for Digital Product Creation Guide

Main entry point with ConversationHandler state machine.
Implements the hierarchical menu structure from UI/UX Creative Phase.
"""

import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ConversationHandler,
    filters,
    ContextTypes,
)

from src.config import TELEGRAM_BOT_TOKEN, validate_config, DEBUG, LOG_LEVEL
from src.handlers import (
    start_command,
    help_command,
    cancel_command,
    educational_menu,
    show_topic,
    back_to_topics,
    back_to_main,
    creative_menu,
    process_creative_input,
    handle_target_audience,
    handle_tech_preference,
)

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=getattr(logging, LOG_LEVEL)
)
logger = logging.getLogger(__name__)

# Conversation states
MODE_SELECTION = 1
EDUCATIONAL_TOPICS = 2
EDUCATIONAL_CONTENT = 3
CREATIVE_INPUT = 4


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle errors in the bot."""
    logger.error(f"Exception while handling an update: {context.error}", exc_info=context.error)


def main() -> None:
    """Main function to run the bot with ConversationHandler."""
    print("\n" + "="*60)
    print("🚀 DigiLib Assistant - Full Implementation")
    print("="*60 + "\n")

    # Validate configuration
    if not validate_config():
        print("\n❌ Configuration validation failed!")
        print("Please set TELEGRAM_BOT_TOKEN environment variable")
        print("Check Railway Variables tab and make sure token is set")
        import sys
        sys.exit(1)

    print("\n🔧 Creating bot application...")
    print(f"   Using token: {TELEGRAM_BOT_TOKEN[:10]}...{TELEGRAM_BOT_TOKEN[-4:]}")

    try:
        # Create the Application
        print("   Connecting to Telegram API...")
        application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
        print("✅ Bot application created successfully")

        # Define conversation handler with states
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('start', start_command)],
            states={
                MODE_SELECTION: [
                    CallbackQueryHandler(educational_menu, pattern='^mode_educational$'),
                    CallbackQueryHandler(creative_menu, pattern='^mode_creative$'),
                    CallbackQueryHandler(help_command, pattern='^help$'),
                ],
                EDUCATIONAL_TOPICS: [
                    CallbackQueryHandler(show_topic, pattern='^topic_'),
                    CallbackQueryHandler(back_to_main, pattern='^back_to_main$'),
                ],
                EDUCATIONAL_CONTENT: [
                    CallbackQueryHandler(show_topic, pattern='^topic_'),
                    CallbackQueryHandler(back_to_topics, pattern='^back_to_topics$'),
                    CallbackQueryHandler(back_to_main, pattern='^back_to_main$'),
                    CallbackQueryHandler(creative_menu, pattern='^mode_creative$'),
                ],
                CREATIVE_INPUT: [
                    CallbackQueryHandler(handle_target_audience, pattern='^target_'),
                    CallbackQueryHandler(handle_tech_preference, pattern='^tech_'),
                    MessageHandler(filters.TEXT & ~filters.COMMAND, process_creative_input),
                    CallbackQueryHandler(creative_menu, pattern='^mode_creative$'),
                    CallbackQueryHandler(back_to_main, pattern='^back_to_main$'),
                ],
            },
            fallbacks=[
                CommandHandler('cancel', cancel_command),
                CommandHandler('start', start_command),
            ],
            allow_reentry=True,
        )

        # Register handlers
        application.add_handler(conv_handler)
        application.add_handler(CommandHandler("help", help_command))

        # Register error handler
        application.add_error_handler(error_handler)

        print("✅ Bot handlers registered")
        print(f"✅ Debug mode: {DEBUG}")
        print(f"✅ Log level: {LOG_LEVEL}")
        print("\n📊 Bot Features:")
        print("   • 📚 Educational Mode (6 topics)")
        print("   • 💡 Creative Mode (AI placeholder)")
        print("   • 🎯 Hierarchical menu navigation")
        print("   • ⚡ State machine with ConversationHandler")
        print("\n" + "="*60)
        print("🤖 Bot is running... Press Ctrl+C to stop")
        print("="*60 + "\n")

        # Start the bot
        application.run_polling(allowed_updates=Update.ALL_TYPES)

    except Exception as e:
        logger.error(f"Failed to start bot: {e}", exc_info=True)
        print(f"\n❌ Error starting bot: {e}")
        print(f"   Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        import sys
        sys.exit(1)


if __name__ == '__main__':
    main()
