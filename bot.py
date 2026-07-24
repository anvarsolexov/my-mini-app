import asyncio
import logging
import os
import sys
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

TOKEN = os.getenv("BOT_TOKEN")
WEB_APP_URL = "https://username.github.io/my-mini-app/" # O'zingizning GitHub sayt havolangizni yozasiz

def get_main_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🚀 Do'konni ochish (Mini App)", web_app=WebAppInfo(url=WEB_APP_URL))]
        ]
    )

async def start_cmd(message: types.Message):
    await message.answer(
        "Assalomu alaykum! Do'konimizga xush kelibsiz.\n\nXizmatlarni ko'rish va buyurtma berish uchun pastdagi tugmani bosing:",
        reply_markup=get_main_menu()
    )

async def web_app_handler(message: types.Message):
    data = message.web_app_data.data
    user = message.from_user
    
    response_text = (
        f"✅ **Buyurtma qabul qilindi!**\n\n"
        f"📌 **Xizmat:** {data}\n"
        f"👤 **Mijoz:** @{user.username if user.username else user.first_name}\n\n"
        f"To'lov qilish uchun admin bilan bog'laning."
    )
    await message.answer(response_text)

async def main():
    if not TOKEN:
        print("Xatolik: BOT_TOKEN topilmadi!")
        return
        
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    
    dp.message.register(start_cmd, Command(commands=["start"]))
    dp.message.register(web_app_handler, lambda message: message.web_app_data is not None)
    
    print("Bot Render serverida ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
