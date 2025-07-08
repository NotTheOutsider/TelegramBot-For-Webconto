import os
import datetime
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.enums import ParseMode
from services.common.helpers import generate_verification_code
from services.common.db import collectionVerification, collectionChats, collectionOrders
# Надо обдумать функционал с удалением чата из БД
# Сейчас есть общая функция, которая в уже существующих заявках делитает или меняет маску
# И эта функци юзается в АПИ и Боте, а в хелперы её выносить глупо, пока что будет импорт контроллера сюда
# UPDT: ИМПОРТА НЕ БУДЕТ ИЗ-ЗА circular import
# ААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААА С*КА

load_dotenv()

bot = Bot(token=os.getenv('TOKEN'))

dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    kb = [
        [
            types.KeyboardButton(text="Включить уведомления"),
            types.KeyboardButton(text="Отключить уведомления")
         ],
        [types.KeyboardButton(text="Привязать телеграм")],
        [types.KeyboardButton(text="Отвязать телеграм от всех конфигураций")] 
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Что сегодня будем делать?"
    )
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
    await message.answer("Начнем работу! Что Вы хотите сделать?", reply_markup=keyboard)

@dp.message(F.text.lower() == "включить уведомления")
async def cmd_start(message: types.Message):
    await message.answer("Дэлаю")

@dp.message(F.text.lower() == "отключить уведомления")
async def cmd_start(message: types.Message):
    await message.answer("Дэлаю")

@dp.message(F.text.lower() == "привязать телеграм")
async def cmd_start(message: types.Message):
    chatID = message.chat.id
    verificationCode = generate_verification_code()
    
    # Checking if this code exists in collection
    
    # Че это за ху**я? Это Г не будет работать, надо переписать, а лучше всю "логику бота" в отдельный файл вынести, а здесь будут чисто роутеры
    existingCode = await collectionVerification.find_one({"verification": verificationCode})
    while existingCode != None:
        verificationCode = generate_verification_code()
        
    # Checking if this chat in collection
    existingDoc = await collectionVerification.find_one({"chat": chatID})
    if existingDoc:
        result = await collectionVerification.find_one_and_update(
            {"chat": chatID},
            {"$set": {"verification": verificationCode, "date": datetime.datetime.now().strftime('%Y-%m-%d, %H:%M:%S')}},
            return_document=True
        )
    else:
        await collectionVerification.insert_one({
            "chat": chatID,
            "verification": verificationCode,
            "date": datetime.datetime.now().strftime('%Y-%m-%d, %H:%M:%S')
        })
        
    await message.answer(
        f'Вот Ваш код для верификации, *никому его не показывайте*:\n`{verificationCode}`\n\nСрок действия кода 15 минут',
        parse_mode=ParseMode.MARKDOWN_V2
    )
    
@dp.message(F.text.lower() == "отвязать телеграм от всех конфигураций")
async def cmd_start(message: types.Message):
    chatID = message.chat.id
    
    try:
        filter = {'chatID': chatID}
            
        existing_chat = await collectionChats.find_one_and_delete(filter)
            
        filter = {'telegramMask': existing_chat['telegramMask']}
        updated_value = {'$set': {'telegramMask': None, 'status': 'pending'}}
        
        await collectionOrders.update_many(filter, updated_value)
    except Exception as e:
        await message.answer(
            f'Произошла ошибка:\n_{e}_\nПопробуйте повторить операцию позже или обратитесь к разработчику', 
            parse_mode=ParseMode.MARKDOWN_V2
        )
    
    await message.answer(
            '*Телеграм был успешно отвязан\\!*\n\nОтветы по вашим заявкам не смогут больше приходить в этот чат', 
            parse_mode=ParseMode.MARKDOWN_V2
        )
    
if __name__ == '__main__':
    dp.run_polling(bot)