import asyncio
import os
from datetime import datetime, timedelta

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# ================== НАСТРОЙКИ ==================

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

# ================== ПАМЯТЬ БОТА ==================

subscriptions = {}  # user_id: expiry_datetime

# ================== КЛАВИАТУРА ==================

def main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🏋️ Тренировки")],
            [KeyboardButton(text="🥗 Питание")],
            [KeyboardButton(text="💳 Купить подписку")],
        ],
        resize_keyboard=True
    )

# ================== ВСПОМОГАТЕЛЬНО ==================

def has_subscription(user_id: int) -> bool:
    if user_id not in subscriptions:
        return False
    return subscriptions[user_id] > datetime.now()

# ================== ХЕНДЛЕРЫ ==================

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "Привет! 👋\n\n"
        "Я твой фитнес-бот 💪\n"
        "Выбирай, что тебя интересует:",
        reply_markup=main_menu()
    )

@dp.message(lambda m: m.text == "🏋️ Тренировки")
async def workouts(message: types.Message):
    if not has_subscription(message.from_user.id):
        await message.answer("🔒 Тренировки доступны только по подписке.")
        return

    await message.answer(
        "🏋️ ТРЕНИРОВКИ\n\n"
        "День 1 — Грудь + Трицепс\n"
        "День 2 — Спина + Бицепс\n"
        "День 3 — Ноги + Плечи\n\n"
        "Хочешь подробный план — напишу 😉"
    )

@dp.message(lambda m: m.text == "🥗 Питание")
async def food(message: types.Message):
    if not has_subscription(message.from_user.id):
        await message.answer("🔒 Питание доступно только по подписке.")
        return

    await message.answer(
        "🥗 ПИТАНИЕ\n\n"
        "Завтрак: овсянка + яйца\n"
        "Обед: курица + рис\n"
        "Ужин: рыба + овощи\n\n"
        "Хочешь меню на неделю?"
    )

@dp.message(lambda m: m.text == "💳 Купить подписку")
async def buy(message: types.Message):
    subscriptions[message.from_user.id] = datetime.now() + timedelta(days=30)

    await message.answer(
        "✅ Подписка активирована на 30 дней!\n\n"
        "Теперь тебе доступны тренировки и питание 💪🔥",
        reply_markup=main_menu()
    )

# ================== ЗАПУСК ==================

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())