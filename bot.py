import asyncio
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

TOKEN = "8397024658:AAEraTVtW5sCAG-Nj3glqELtgpab5g-eAlo"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# ---------------- ПАМЯТЬ БОТА ----------------
subscriptions = {}  # здесь будем хранить подписки


# ---------------- КЛАВИАТУРЫ ----------------

def main_menu():
    return types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="💳 Купить подписку")],
            [types.KeyboardButton(text="🍽 Питание"), types.KeyboardButton(text="🏋️ Тренировки")],
        ],
        resize_keyboard=True
    )


# ---------------- ВСПОМОГАТЕЛЬНАЯ ФУНКЦИЯ ----------------

def has_subscription(user_id: int) -> bool:
    """Проверяем, есть ли активная подписка"""
    if user_id not in subscriptions:
        return False

    return subscriptions[user_id] > datetime.now()


# ---------------- ХЭНДЛЕРЫ ----------------

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "Привет! Это бот для спорта и питания 💪\n"
        "Чтобы открыть доступ, нужна подписка.",
        reply_markup=main_menu()
    )


@dp.message(lambda m: m.text == "💳 Купить подписку")
async def buy_subscription(message: types.Message):
    # ⚠️ ПОКА ЭТО ИМИТАЦИЯ ОПЛАТЫ
    subscriptions[message.from_user.id] = datetime.now() + timedelta(days=30)

    await message.answer(
        "✅ Подписка активирована!\n"
        "Срок: 30 дней\n"
        "Цена: 999 ₽\n\n"
        "Теперь тебе доступен контент 💪",
        reply_markup=main_menu()
    )


@dp.message(lambda m: m.text == "🍽 Питание")
async def food(message: types.Message):
    if not has_subscription(message.from_user.id):
        await message.answer("❌ У тебя нет активной подписки")
        return

    await message.answer(
        "🍽 Питание\n\n"
        "Здесь будет меню, планы и советы."
    )


@dp.message(lambda m: m.text == "🏋️ Тренировки")
async def training(message: types.Message):
    if not has_subscription(message.from_user.id):
        await message.answer("❌ У тебя нет активной подписки")
        return

    await message.answer(
        "🏋️ Тренировки\n\n"
        "Здесь будут программы тренировок."
    )


# ---------------- ЗАПУСК ----------------

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
