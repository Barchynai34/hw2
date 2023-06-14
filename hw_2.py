from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from config import token
import sqlite3, time, logging

bot = Bot(token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)

database = sqlite3.connect('users.db')
cursor = database.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS users(
    user_id INT,
    chat_id INT,
    username VARCHAR(255),
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    created VARCHAR(100)
);
""")
cursor.connection.commit()

keyboard_buttons = [
    KeyboardButton('/backend'),
    KeyboardButton('/frontend'),
    KeyboardButton('/uxui'),
    KeyboardButton('/android'),
    KeyboardButton('/ios')
]
keyboard_one = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=30).add(*keyboard_buttons)

@dp.message_handler(commands='start')
async def start(message:types.Message):
    cursor.execute(f"SELECT * FROM users WHERE user_id = {message.from_user.id};")
    result = cursor.fetchall()
    if result == []:
        cursor.execute(f"""INSERT INTO users VALUES ({message.from_user.id},
                    {message.chat.id}, '{message.from_user.username}',
                    '{message.from_user.first_name}', 
                    '{message.from_user.last_name}',
                    '{time.ctime()}');
                    """)
    cursor.connection.commit()
    await message.answer(f"Привет {message.from_user.full_name}!", reply_markup=keyboard_one)


@dp.message_handler(commands='backend')
async def help(message:types.Message):
    await message.answer("Backend — это внутренняя часть сайта и сервера и т.д Стоимость 10000 сом в месяц Обучение: 5 месяц")


@dp.message_handler(commands='frontend')
async def help(message:types.Message):
    await message.answer("Frontend — это внешняя часть сайта и сервера и т.д Стоимость 10000 сом в месяц Обучение: 5 месяц")


@dp.message_handler(commands='uxui')
async def help(message:types.Message):
    await message.answer("UX/UI дизайнер - это специалист, ответственный за создание удобного и интуитивного интерфейса для веб-сайтов и мобильных приложений.Стоимость 11000 сом в месяц Обучение: 6 месяц")


@dp.message_handler(commands='android')
async def help(message:types.Message):
    await message.answer("Android – это такой разработчик, который, прежде всего, занимается созданием мобильных приложений: мессенджеров, онлайн-игр, соцсетей, интернет-магазинов и т.д Стоимость 12000 сом в месяц Обучение: 7 месяц")



@dp.message_handler(commands='ios')
async def help(message:types.Message):
    await message.answer("iOS developer, — это программист, который пишет сервисы и программы для айфонов. Стоимость 12000 сом в месяц Обучение: 7 месяц")

class MailingState(StatesGroup):
    text = State()

@dp.message_handler(commands='mailing')
async def mailing(message:types.Message):
    if message.from_user.id in [1181982807]:
        await message.reply("Введите текст для рассылки:")
        await MailingState.text.set()
    else:
        await message.answer("У вас нет прав")

executor.start_polling(dp)