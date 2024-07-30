# API_TOKEN = '7482452539:AAGpAW8VXjO9CGpYU57Xyv8xUcsfcKGx9SI'
from aiogram import Bot, Dispatcher, executor, types

# Замените этот токен на токен вашего бота
API_TOKEN = '7482452539:AAGpAW8VXjO9CGpYU57Xyv8xUcsfcKGx9SI'
# Укажите ваш канал
CHANNEL_USERNAME = '@adelya_test_for_test'

LESSONS_LINK = 'https://disk.yandex.ru/d/ivmqD-gXCg3mhw'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    # Приветственное сообщение
    welcome_text = (
        "Добро пожаловать! 🌟\n"
        "Чтобы получать много полезной информации и эксклюзивные материалы, "
        "подпишитесь на наш канал. 🎉\n\n"
        "В качестве подарка за подписку вы получите доступ к нашим уникальным видеоурокам! 🎥"
    )

    # Кнопка для подписки на канал
    subscribe_button = types.InlineKeyboardButton(
        text="Подписаться на канал", url=f"https://t.me/{CHANNEL_USERNAME}"
    )
    # Кнопка для получения видеоуроков
    lessons_button = types.InlineKeyboardButton(
        text="Получить видеоуроки", callback_data='get_lessons'
    )

    # Создаем клавиатуру с кнопками
    keyboard = types.InlineKeyboardMarkup().add(subscribe_button, lessons_button)

    # Отправляем сообщение с клавиатурой
    await message.reply(welcome_text, reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data == 'get_lessons')
async def process_lessons_request(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    chat_member = await bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)

    if chat_member.is_chat_member() or chat_member.status in ['member', 'administrator', 'creator']:
        await bot.send_message(callback_query.from_user.id, f"Спасибо за подписку! Вот ссылка на видеоуроки: \n{LESSONS_LINK}")
    else:
        await bot.send_message(callback_query.from_user.id, (
            "К сожалению, я не могу предоставить доступ к видеоурокам без подписки. "
            "Пожалуйста, подпишитесь на наш канал, чтобы получать много полезной информации и эксклюзивные материалы. "
            "После подписки нажмите на кнопку «Получить видеоуроки» снова! 🎁"
        ))

    await bot.answer_callback_query(callback_query.id)

@dp.message_handler()
async def echo(message: types.Message):
    # Отправляем обратно полученное сообщение
    await message.answer(message.text)

if __name__ == '__main__':
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)