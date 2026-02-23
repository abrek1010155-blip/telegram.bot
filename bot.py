import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

# Твой токен уже вставлен
TOKEN = "8356295701:AAFSOGwoY5d01sAcHI0VP-ssK760TubVBBY"

# Логи для отладки
logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Привет! Я твой бот. Пиши /help, если хочешь что-то узнать.")

@dp.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer("Пока умею только здороваться. Добавь мне функций — я не против!")

@dp.message()
async def echo(message: Message):
    await message.answer(f"Ты сказал: {message.text}\n(пока просто эхо)")

async def main():
    try:
        await dp.start_polling(bot, skip_updates=True)
    finally:
        await bot.session.close()  # Чистое завершение

if __name__ == "__main__":
    asyncio.run(main())
