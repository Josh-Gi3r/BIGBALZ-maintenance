#!/usr/bin/env python3
"""
Temporary maintenance bot for BIGBALZ
Responds with maintenance message when tagged or messaged
"""

import os
import logging
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Your maintenance message with strikethrough
MAINTENANCE_MESSAGE = """Lord Josh is ~breaking my BALZ~ updating me now\\.
Please be patient I should be back up in a few days\\."""

async def maintenance_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send maintenance message for any interaction"""
    try:
        # Check if bot is mentioned or if it's a DM
        message = update.message or update.edited_message
        if not message:
            return

        # In groups, only respond if mentioned
        if message.chat.type != 'private':
            # Check if bot is mentioned
            if message.text:
                bot_username = (await context.bot.get_me()).username
                if f'@{bot_username}' not in message.text:
                    return

        # Send the maintenance message with MarkdownV2 formatting
        await message.reply_text(
            MAINTENANCE_MESSAGE,
            parse_mode='MarkdownV2'
        )

    except Exception as e:
        logger.error(f"Error sending maintenance message: {e}")

def main():
    """Start the maintenance bot"""
    # Get token from environment
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        logger.error("No TELEGRAM_BOT_TOKEN found in environment!")
        exit(1)

    # Create application
    application = Application.builder().token(token).build()

    # Add handler for all messages
    application.add_handler(MessageHandler(
        filters.ALL,  # Respond to everything
        maintenance_reply
    ))

    # Start the bot
    logger.info("🔧 Maintenance bot starting...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()