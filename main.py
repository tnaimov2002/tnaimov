import asyncio
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

# ==== BOT TOKEN va ADMIN ID-ni ====
BOT_TOKEN = "8075927150:AAFLN1UaCMjRnPIZ8TkERrjXWhCBlVOydzM"   # token
ADMIN_ID = 143688902                # Telegram ID
CHANNEL_LINK = "https://t.me/thekhaitov"  # Kanal havolasi

# Bot obyektini yaratamiz (3.7.0 ga mos)
bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

# --- Holatlar ---
class RegForm(StatesGroup):
    full_name = State()
    contact = State()

# --- Start ---
@dp.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "👋 Salom! <b>Khaitov Online Academy</b> botiga xush kelibsiz.\n\n"
        "Iltimos, <b>ism-familyangizni</b> yuboring.\n\n"
        
    )
    await state.set_state(RegForm.full_name)

# --- Ism-Familya qabul qilish ---
@dp.message(RegForm.full_name)
async def get_full_name(message: Message, state: FSMContext):
    full_name = message.text.strip()
    if len(full_name) < 3:
        await message.answer("❗️Iltimos, to‘liq ism-familyangizni yuboring.")
        return

    await state.update_data(full_name=full_name)

    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📱 Kontaktni yuborish", request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer(
        "Rahmat! Endi <b>telefon raqamingizni</b> yuboring 👇",
        reply_markup=kb
    )
    await state.set_state(RegForm.contact)

# --- Kontaktni olish ---
@dp.message(RegForm.contact, F.contact)
async def get_contact(message: Message, state: FSMContext):
    phone = message.contact.phone_number
    data = await state.get_data()
    full_name = data.get("full_name")

    # Admin'ga yuborish
    text_for_admin = (
        "📥 Yangi foydalanuvchi ro‘yxatdan o‘tdi!\n\n"
        f"👤 Ism-familya: {full_name}\n"
        f"📱 Telefon: {phone}\n"
        f"🆔 Telegram ID: {message.from_user.id}\n"
        f"🔗 Username: @{message.from_user.username or 'yo‘q'}"
    )
    await bot.send_message(ADMIN_ID, text_for_admin)

    # Foydalanuvchiga kanal havolasini yuborish
    await message.answer(
        f"✅ Rahmat, {full_name}!\n\n"
        f"Quyidagi havola orqali kanalimizga qo‘shilishingiz mumkin:\n\n"
        f"{CHANNEL_LINK}",
        reply_markup=ReplyKeyboardRemove()
    )

    await state.clear()

# --- Telefon raqamni matn ko‘rinishida yuborsa ---
@dp.message(RegForm.contact, F.text)
async def get_contact_as_text(message: Message, state: FSMContext):
    phone = message.text.strip()
    data = await state.get_data()
    full_name = data.get("full_name")

    # Admin'ga yuborish
    text_for_admin = (
        "📥 Yangi foydalanuvchi ro‘yxatdan o‘tdi!\n\n"
        f"👤 Ism-familya: {full_name}\n"
        f"📱 Telefon: {phone}\n"
        f"🆔 Telegram ID: {message.from_user.id}\n"
        f"🔗 Username: @{message.from_user.username or 'yo‘q'}"
    )
    await bot.send_message(ADMIN_ID, text_for_admin)

    # Foydalanuvchiga kanal havolasini yuborish
    await message.answer(
        f"✅ Rahmat, {full_name}!\n\n"
        f"Quyidagi havola orqali kanalimizga qo‘shilishingiz mumkin:\n\n"
        f"{CHANNEL_LINK}",
        reply_markup=ReplyKeyboardRemove()
    )

    await state.clear()

# --- Botni ishga tushirish ---
async def main():
    print("🤖 Bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("⛔ Bot to‘xtadi.")



