import telegram
from dotenv import load_dotenv

load_dotenv()

def notify(photo, caption):
    # You can require a token for your bot
    # bot = telegram.Bot(token=os.getenv("TELEGRAM_TOKEN"))
    # bot.send_photo('-382513146', photo=open(photo, 'rb'), caption=caption)
    print('notified')
