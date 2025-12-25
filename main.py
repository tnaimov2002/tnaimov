import asyncio
import os

from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove
)

# ================== SOZLAMALAR ==================
BOT_TOKEN = os.getenv("BOT_TOKEN") or "BU_YERGA_YANGI_TOKEN"
ADMIN_ID = 143688902
CHANNEL_LINK = "https://t.me/thekhaitov/580"
# =================================================

if not BOT_TOKEN or ":" not in BOT_TOKEN:
    raise RuntimeError("❌ BOT_TOKEN noto‘g‘ri yoki topilmadi!")

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

# ================== /start ==================
@dp.message(CommandStart())
async def cmd_start(message: Message):
    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📱 Kontaktni yuborish", request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    await message.answer(
        "👋 Salom! <b>Khaitov Online School</b> botiga xush kelibsiz.\n\n"
        "Bepul darslik qo‘lga kiritish uchun <b>kontaktingizni</b> qoldiring 👇",
        reply_markup=kb
    )

# ================== KONTAKTNI QABUL QILISH ==================
@dp.message(F.contact)
async def get_contact(message: Message):
    phone = message.contact.phone_number

    await bot.send_message(
        ADMIN_ID,
        "📥 <b>Yangi foydalanuvchi</b>\n\n"
        f"📱 Telefon: {phone}\n"
        f"🆔 Telegram ID: {message.from_user.id}\n"
        f"🔗 Username: @{message.from_user.username or 'yo‘q'}"
    )

    await message.answer(
        "✅ Rahmat!\n\n"
        f"Bepul darslik 👉 {CHANNEL_LINK}",
        reply_markup=ReplyKeyboardRemove()
    )

# ================== BOTNI ISHGA TUSHIRISH ==================
async def main():
    print("🤖 Bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
