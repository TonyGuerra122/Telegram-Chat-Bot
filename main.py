from controllers.BotController import BotController
import os
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()

    API_KEY = os.getenv("API_KEY")
    bot = BotController(API_KEY)
    bot.init()