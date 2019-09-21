import os
import telegram
import datetime
from settings import get_env_value 

def notify(photo, caption=""):
    bot = telegram.Bot(token=get_env_value("TELEGRAM_TOKEN"))
    caption = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    bot.send_photo(get_env_value("TELEGRAM_CHAT_ID"), photo=open(photo, 'rb'), caption=caption)
