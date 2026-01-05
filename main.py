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
BOT_TOKEN = os.getenv("BOT_TOKEN") or "8075927150:AAEMrd_YNPCGVnKRVbvI3gP3cqodfSMnF-o"

ADMIN_IDS = [
    2034173364,
    5909893805,
    143688902
]

CHANNEL_LINK = "https://t.me/thekhaitov/580"
# =================================================

if not BOT_TOKEN or ":" not in BOT_TOKEN:
    raise RuntimeError("❌ BOT_TOKEN noto‘g‘ri yoki topilmadi!")

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

# 📦 FOYDALANUVCHILAR BAZASI (xotirada)
USERS = set()

# ================== /start ==================
@dp.message(CommandStart())
async def cmd_start(message: Message):
    USERS.add(message.from_user.id)

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

# ================== KONTAKT ==================
@dp.message(F.contact)
async def get_contact(message: Message):
    USERS.add(message.from_user.id)

    phone = message.contact.phone_number
    text = (
        "📥 <b>Yangi foydalanuvchi</b>\n\n"
        f"📱 Telefon: {phone}\n"
        f"👤 Ism: {message.from_user.full_name}\n"
        f"🆔 Telegram ID: {message.from_user.id}\n"
        f"🔗 Username: @{message.from_user.username or 'yo‘q'}"
    )

    for admin_id in ADMIN_IDS:
        await bot.send_message(admin_id, text)

    await message.answer(
        f"✅ Rahmat!\n\n📚 Bepul darslik 👉 {CHANNEL_LINK}",
        reply_markup=ReplyKeyboardRemove()
    )

# ================== ADMIN → BARCHAGA MATN ==================
@dp.message(F.text & F.from_user.id.in_(ADMIN_IDS))
async def admin_text_broadcast(message: Message):
    sent = 0
    for user_id in USERS:
        try:
            await bot.send_message(user_id, message.text)
            sent += 1
        except:
            pass

    await message.answer(f"✅ Xabar {sent} ta foydalanuvchiga yuborildi")

# ================== ADMIN → BARCHAGA RASM ==================
@dp.message(F.photo & F.from_user.id.in_(ADMIN_IDS))
async def admin_photo_broadcast(message: Message):
    photo_id = message.photo[-1].file_id

    for user_id in USERS:
        try:
            await bot.send_photo(
                user_id,
                photo=photo_id,
                caption=message.caption
            )
        except:
            pass

    await message.answer("✅ Rasm barcha foydalanuvchilarga yuborildi")

# ================== ADMIN → BARCHAGA VIDEO ==================
@dp.message(F.video & F.from_user.id.in_(ADMIN_IDS))
async def admin_video_broadcast(message: Message):
    for user_id in USERS:
        try:
            await bot.send_video(
                user_id,
                video=message.video.file_id,
                caption=message.caption
            )
        except:
            pass

    await message.answer("✅ Video barcha foydalanuvchilarga yuborildi")

# ================== FOYDALANUVCHI VIDEO → ADMINGA ==================
@dp.message(F.video)
async def user_video_to_admin(message: Message):
    USERS.add(message.from_user.id)

    user = message.from_user
    caption = (
        "🎬 <b>Yangi video</b>\n\n"
        f"👤 {user.full_name}\n"
        f"🆔 {user.id}\n"
        f"🔗 @{user.username or 'yo‘q'}"
    )

    if message.caption:
        caption += f"\n\n📝 Izoh:\n{message.caption}"

    for admin_id in ADMIN_IDS:
        await bot.send_video(
            admin_id,
            message.video.file_id,
            caption=caption
        )

    await message.answer("✅ Video adminga yuborildi")

# ================== BOTNI ISHGA TUSHIRISH ==================
async def main():
    print("🤖 Bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
