import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    Message, InlineKeyboardMarkup, InlineKeyboardButton,
    LabeledPrice, PreCheckoutQuery, CallbackQuery
)

TOKEN = "8277869771:AAGUXjrUh_7oLYbEavCkSWBVIpAPd4lOWF8"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Barcha narxlar (Stars)
PRICES = {
    "play_1": {"stars": 1, "emoji": "⭐"},
    "play_5": {"stars": 5, "emoji": "⭐"},
    "play_10": {"stars": 10, "emoji": "⭐"},
    "play_15": {"stars": 15, "emoji": "⭐"},
    "play_25": {"stars": 25, "emoji": "⭐⭐"},
    "play_50": {"stars": 50, "emoji": "⭐⭐"},
    "play_100": {"stars": 100, "emoji": "⭐⭐⭐"},
    "play_200": {"stars": 200, "emoji": "⭐⭐⭐"},
    "play_300": {"stars": 300, "emoji": "⭐⭐⭐"},
    "play_500": {"stars": 500, "emoji": "⭐⭐⭐⭐"},
    "play_750": {"stars": 750, "emoji": "⭐⭐⭐⭐"},
    "play_1000": {"stars": 1000, "emoji": "⭐⭐⭐⭐⭐"}
}

@dp.message(F.text == "/start")
async def start(message: Message):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            # 1-qator: kichik narxlar
            [
                InlineKeyboardButton(text="⭐ 1", callback_data="play_1"),
                InlineKeyboardButton(text="⭐ 5", callback_data="play_5"),
                InlineKeyboardButton(text="⭐ 10", callback_data="play_10"),
            ],
            # 2-qator: o'rta narxlar
            [
                InlineKeyboardButton(text="⭐ 15", callback_data="play_15"),
                InlineKeyboardButton(text="⭐ 25", callback_data="play_25"),
                InlineKeyboardButton(text="⭐ 50", callback_data="play_50"),
            ],
            # 3-qator: katta narxlar
            [
                InlineKeyboardButton(text="⭐⭐ 100", callback_data="play_100"),
                InlineKeyboardButton(text="⭐⭐ 200", callback_data="play_200"),
                InlineKeyboardButton(text="⭐⭐ 300", callback_data="play_300"),
            ],
            # 4-qator: juda katta narxlar
            [
                InlineKeyboardButton(text="⭐⭐⭐ 500", callback_data="play_500"),
                InlineKeyboardButton(text="⭐⭐⭐ 750", callback_data="play_750"),
            ],
            # 5-qator: maksimal
            [
                InlineKeyboardButton(text="⭐⭐⭐⭐⭐ 1000", callback_data="play_1000")
            ]
        ]
    )
    await message.answer(
        "🎮 <b>O'yinga xush kelibsiz!</b>\n\n"
        "💰 Narxni tanlang (Telegram Stars):\n"
        "⭐ 1 dan 1000 gacha\n\n"
        "<i>Qaysi narxda o'ynamoqchisiz?</i>",
        reply_markup=kb,
        parse_mode="HTML"
    )

@dp.callback_query(F.data.in_(PRICES.keys()))
async def invoice(call: CallbackQuery):
    # Tanlangan narxni olish
    price_data = PRICES[call.data]
    stars_amount = price_data["stars"]
    emoji = price_data["emoji"]
    
    await bot.send_invoice(
        chat_id=call.from_user.id,
        title=f"🎮 O'yin - {stars_amount} Stars",
        description=f"O'yinni boshlash uchun {stars_amount} {emoji}",
        payload=call.data,
        provider_token="",      # Stars uchun bo'sh
        currency="XTR",         # Telegram Stars
        prices=[LabeledPrice(label=f"{stars_amount} Stars", amount=stars_amount)]
    )
    await call.answer(f"Invoice yuborildi: {stars_amount} ⭐")

@dp.pre_checkout_query()
async def pre_checkout(query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(query.id, ok=True)

@dp.message(F.successful_payment)
async def success(message: Message):
    payment = message.successful_payment
    stars_paid = payment.total_amount
    
    await message.answer(
        f"✅ <b>To'lov muvaffaqiyatli!</b>\n\n"
        f"💰 To'langan: {stars_paid} ⭐\n"
        f"🎮 O'yin boshlandi!\n\n"
        f"<i>Omad yor bo'lsin! 🍀</i>",
        parse_mode="HTML"
    )

async def main():
    print("🚀 Bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
