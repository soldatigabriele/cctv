import os
import telegram
import datetime
from dotenv import load_dotenv

load_dotenv()

def notify(photo, caption=""):
    bot = telegram.Bot(token=os.getenv("TELEGRAM_TOKEN"))
    caption = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    bot.send_photo(os.getenv("TELEGRAM_CHAT_ID"), photo=open(photo, 'rb'), caption=caption)
