import re
from os import getenv

from dotenv import load_dotenv
from pyrogram import filters

load_dotenv()
from telegram.ext import Updater, MessageHandler, Filters
from google.cloud import vision
import imagehash
from PIL import Image

def detect_copyright(file_path):
    # Using Google Vision API
    client = vision.ImageAnnotatorClient()
    with open(file_path, "rb") as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = client.web_detection(image=image)
    # Custom logic to identify if content is copyrighted
    if response.web_detection.full_matching_images:
        return True  # Flag as copyrighted

    # Perceptual Hashing for additional checks
    known_hashes = {"known_hash_1", "known_hash_2"}  # Example set of known copyrighted hashes
    image = Image.open(file_path)
    img_hash = imagehash.phash(image)
    if str(img_hash) in known_hashes:
        return True  # Flag as copyrighted
    return False

def handle_media(update, context):
    if update.message.photo or update.message.video or update.message.sticker:
        file = update.message.photo[-1].get_file()  # Adjust for videos, stickers
        file_path = file.download()
        if detect_copyright(file_path):
            update.message.delete()

def main():
    updater = Updater("YOUR_BOT_TOKEN", use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.photo | Filters.video | Filters.sticker, handle_media))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()



# Get this value from my.telegram.org/apps
API_ID = int(getenv("API_ID"))
API_HASH = getenv("API_HASH")

# Get your token from @BotFather on Telegram.
BOT_TOKEN = getenv("BOT_TOKEN")

# Get your mongo url from cloud.mongodb.com
MONGO_DB_URI = getenv("MONGO_DB_URI", None)

DURATION_LIMIT_MIN = int(getenv("DURATION_LIMIT", 777777))

# Chat id of a group for logging bot's activities
LOGGER_ID = int(getenv("LOGGER_ID", None))

# Get this value from @FallenxBot on Telegram by /id
OWNER_ID = int(getenv("OWNER_ID", 6885582933))

 


BANNED_USERS = filters.user()
adminlist = {}
lyrical = {}
votemode = {}
autoclean = []
confirmer = {}






if SUPPORT_CHAT:
    if not re.match("(?:http|https)://", SUPPORT_CHAT):
        raise SystemExit(
            "[ERROR] - Your SUPPORT_CHAT url is wrong. Please ensure that it starts with https://"
        )
