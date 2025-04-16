from aiogram import Bot
from dotenv import dotenv_values

cfg = dotenv_values(".env")

bot = Bot(token=cfg.get('TOKEN'))