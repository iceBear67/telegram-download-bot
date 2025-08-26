import asyncio
import logging
from shutil import move

from telegram import Update
from telegram.ext import (Application, CommandHandler, ContextTypes,
                          MessageHandler, filters)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = "BOT-TOKEN"
BASE_URL = "http://localhost:8081/bot"
OUTPUT_DIR = "/home/potato/tgdownloadbot/"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!"
    )

async def downloader(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    document = update.message.document or update.message.video or update.message.photo or update.message.video_note
    if document:
        await update.message.reply_text("Downloading!")
    else:
        await update.message.reply_text("Invalid media!")
        return
    file = await context.bot.get_file(document.file_id)
    out_path = OUTPUT_DIR + document.file_name
    asyncio.create_task(file.download_to_drive(out_path))
    await update.message.reply_text(f"File {document.file_name} downloaded to {out_path}")

def main() -> None:
    application = Application.builder().token(TOKEN).base_url(BASE_URL)
    if "localhost" in BASE_URL:
        application.base_file_url("")
    application = application.read_timeout(864000).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.ALL, downloader))
    application.run_polling()



if __name__ == "__main__":
    main()
