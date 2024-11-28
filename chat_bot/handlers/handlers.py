from telegram import (
    Update,
    constants
)
from telegram.ext import (
    ContextTypes
)

from music_services.music_services import get_music_service, extract_url
from song_extractors.factory.se_factory import SongExtractorsFactory

factory = SongExtractorsFactory()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello! Add me to a group and mention me to see what I can do!")


async def mention_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    message = update.message
    bot_name = context.bot.username

    if bot_name in message.text and message.reply_to_message:
        given_url = extract_url(message.reply_to_message.text)
        music_service = get_music_service(given_url)

        if not music_service:
            await message.reply_text(
                "That's not a link to a song or such music service is not supported"
            )
            return None

        music_extractor = factory.get_song_extractor(music_service)
        song_details = music_extractor.extract_song_details(given_url)

        extractors = factory.get_extractors_by_exclusion(music_service)
        song_urls = []

        for service, extractor in extractors.items():
            song_url = extractor.get_song_url(song_details)
            link = (('[Album Link]' if song_details.is_album else '[Song Link]')
                    + f'({song_url})')
            song_urls.append(f"*{service}:* {link}")

        await message.reply_text(
            text="\n".join(song_urls),
            parse_mode=constants.ParseMode.MARKDOWN_V2
        )
