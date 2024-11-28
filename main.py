import os

from telegram.ext import (
    Application
)
from telegram.ext import (
    CommandHandler, MessageHandler, filters
)

from chat_bot.handlers import handlers


def main() -> None:
    token = os.environ['TG_TOKEN']
    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler('start', handlers.start))
    application.add_handler(MessageHandler(
                    filters.TEXT | filters.Entity("url"),
                    handlers.mention_handler
                ))

    application.run_polling()


if __name__ == '__main__':
    main()
