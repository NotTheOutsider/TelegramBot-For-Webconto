import os
from dotenv import load_dotenv
from aiogram import Bot

load_dotenv()

bot = Bot(token=os.getenv('TOKEN'))