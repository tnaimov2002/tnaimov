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
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext


# ================== SOZLAMALAR ==================
BOT_TOKEN = os.getenv("BOT_TOKEN") or "8075927150:AAEMrd_YNPCGVnKRVbvI3gP3cqodfSMnF-o"
ADMIN_ID = 143688902
CHANNEL_LINK = "https://t.me/thekhaitov/580"
# =================================================


# Token tekshiruvi (oldindan)
if not BOT_TOKEN or ":" not in BOT_TOKEN:
    raise RuntimeError("❌ BOT_TOKEN noto‘g‘ri yoki topilmadi!")


# Bot va Dispatcher
bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()


# ================== FSM HOLATLAR ==================
class RegForm(StatesGroup):
    full_name = State()
    contact = State()


# ================== /start ==================
@dp.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "👋 Salom! <b>Khaitov Online School</b> botiga xush kelibsiz.\n\n"
        "Bepul darslik olish uchun <b>ism-familyangizni</b> yuboring 👇"
    )
    await state.set_state(RegForm.full_name)


# ================== ISM-FAMILYA ==================
@dp.message(RegForm.full_name)
async def get_full_name(message: Message, state: FSMContext):
    full_name = (message.text or "").strip()

    if len(full_name) < 3:
        await message.answer("❗️Iltimos, to‘liq ism-familyangizni yozing.")
        return

    await state.update_data(full_name=full_name)

    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📱 Kontaktni yuborish", request_contact=True)]],
        resize_keyboard=True
    )

    await message.answer(
        "Rahmat! Endi <b>telefon raqamingizni</b> yuboring 👇",
        reply_markup=kb
    )
    await state.set_state(RegForm.contact)


# ================== KONTAKT (TUGMA ORQALI) ==================
@dp.message(RegForm.contact, F.contact)
async def get_contact(message: Message, state: FSMContext):
    phone = message.contact.phone_number
    data = await state.get_data()
    full_name = data.get("full_name")

    # Admin'ga yuborish
    await bot.send_message(
        ADMIN_ID,
        "📥 <b>Yangi foydalanuvchi</b>\n\n"
        f"👤 Ism-familya: {full_name}\n"
        f"📱 Telefon: {phone}\n"
        f"🆔 Telegram ID: {message.from_user.id}\n"
        f"🔗 Username: @{message.from_user.username or 'yo‘q'}"
    )

    # Foydalanuvchiga javob
    await message.answer(
        f"✅ Rahmat, <b>{full_name}</b>!\n\n"
        f"Bepul darslik 👉 {CHANNEL_LINK}",
        reply_markup=ReplyKeyboardRemove()
    )

    await state.clear()


# ================== KONTAKT (MATN ORQALI) ==================
@dp.message(RegForm.contact, F.text)
async def get_contact_text(message: Message, state: FSMContext):
    phone = message.text.strip()
    data = await state.get_data()
    full_name = data.get("full_name")

    await bot.send_message(
        ADMIN_ID,
        "📥 <b>Yangi foydalanuvchi</b>\n\n"
        f"👤 Ism-familya: {full_name}\n"
        f"📱 Telefon: {phone}\n"
        f"🆔 Telegram ID: {message.from_user.id}"
    )

    await message.answer(
        f"✅ Rahmat, <b>{full_name}</b>!\n\n"
        f"Bepul darslik 👉 {CHANNEL_LINK}",
        reply_markup=ReplyKeyboardRemove()
    )

    await state.clear()


# ================== BOTNI ISHGA TUSHIRISH ==================
async def main():
    print("🤖 Bot ishga tushdi...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("⛔️ Bot to‘xtadi.")



