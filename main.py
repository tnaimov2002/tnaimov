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

BOT_TOKEN = "TOKEN_BU_YERGA"
ADMIN_ID = 143688902
CHANNEL_LINK = "https://t.me/thekhaitov/580"

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

class RegForm(StatesGroup):
    full_name = State()
    contact = State()

@dp.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "👋 Salom! <b>Khaitov Online School</b> botiga xush kelibsiz.\n\n"
        "Bepul darslik qo‘lga kiritish uchun ism-familyangizni yuboring 👇"
    )
    await state.set_state(RegForm.full_name)

@dp.message(RegForm.full_name)
async def get_full_name(message: Message, state: FSMContext):
    full_name = message.text.strip()
    if len(full_name) < 3:
        await message.answer("❗️Iltimos, to‘liq ism-familyangizni yuboring.")
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

@dp.message(RegForm.contact, F.contact)
async def get_contact(message: Message, state: FSMContext):
    phone = message.contact.phone_number
    data = await state.get_data()
    full_name = data.get("full_name")

    await bot.send_message(
        ADMIN_ID,
        f"📥 Yangi foydalanuvchi:\n\n"
        f"👤 {full_name}\n"
        f"📱 {phone}\n"
        f"🆔 {message.from_user.id}"
    )

    await message.answer(
        f"✅ Rahmat, {full_name}!\n\n"
        f"Bepul darslik 👉 {CHANNEL_LINK}",
        reply_markup=ReplyKeyboardRemove()
    )

    await state.clear()

async def main():
    print("🤖 Bot ishga tushdi...")
    await dp.start_polling(bot)

if name == "__main__":
    asyncio.run(main())
