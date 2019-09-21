import os
import telegram
from dotenv import load_dotenv

load_dotenv()

def notify(photo, caption="human detected"):
    # You can require a token for your bot
    bot = telegram.Bot(token=os.getenv("TELEGRAM_TOKEN"))
    bot.send_photo(os.getenv("TELEGRAM_CHAT_ID"), photo=open(photo, 'rb'), caption=caption)
