import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.types import FSInputFile
from aiogram.client.session.aiohttp import AiohttpSession

from main import MainProgram
from manage_text import ManagerText
from config import API, IDs, PROXY

# Створюємо сесію з проксі
session = AiohttpSession(proxy=PROXY)

# Ініціалізація бота та диспетчера
bot = Bot(token=API, session=session)
dp = Dispatcher()

# Ініціалізація класів для управління текстом та основної логіки
mt = ManagerText()
mp = MainProgram()


# Команда старту
@dp.message(CommandStart())
async def cmd_start(message: Message):
    text = mt.get_start_text()
    await message.answer(text=text, parse_mode=ParseMode.MARKDOWN)


# Команда допомоги
@dp.message(Command('help'))
async def cmd_help(message: Message):
    text = mt.get_help_text()
    await message.answer(text=text, parse_mode=ParseMode.MARKDOWN)


# Команда додавання
@dp.message(Command('add'))
async def cmd_add(message: Message):
    change_cmd = mt.change_cmd_add(message.text)
    flag = change_cmd[0]
    district, url = change_cmd[1]
    text = change_cmd[2]

    if flag:
        res = mp.set_url(name=district, url=url)
        if not res[0]:
            text = res[1]

    await message.answer(text=text, parse_mode=ParseMode.MARKDOWN)


# Команда для отримання даних за тиждень
@dp.message(Command('week'))
async def cmd_week(message: Message):
    data = mp.get_week()
    text = mt.change_week_text(data=data)
    await message.answer(text=text, parse_mode=ParseMode.MARKDOWN)


# Команда для отримання даних за місяць
@dp.message(Command('month'))
async def cmd_week(message: Message):
    data = mp.get_month()

    text = mt.change_week_text(
        data=data
    )

    await message.answer(
        text=text,
        parse_mode=ParseMode.MARKDOWN
    )


# Команда для отримання даних про райони
@dp.message(Command('district'))
async def cmd_district(message: Message):
    dis = mp.get_district()
    text = mt.get_district_text(txt=dis)
    await message.answer(text=text)


# Команда для отримання бази даних
@dp.message(Command('get_db'))
async def cmd_get_db(message: Message):
    file = FSInputFile(path='data.db')
    await bot.send_document(chat_id=message.chat.id, document=file)


# Функція для автоматичної відправки пропозицій
async def cmd_send_offer():
    while True:
        await asyncio.sleep(60)  # Чекаємо перед відправкою
        data = mp.get_clear_data()
        text = mt.change_ofer_text(urls=data)

        for user_id in IDs:
            if text == 'Null':
                break
            await bot.send_message(chat_id=user_id, text=text, parse_mode=ParseMode.MARKDOWN)

        await asyncio.sleep(30 * 60)  # Повтор кожні 30 хвилин


# Функція для стартового повідомлення при запуску бота
async def cmd_start_bot():
    text = mt.get_start_bot_text()
    for user_id in IDs:
        await bot.send_message(chat_id=user_id, text=text, parse_mode=ParseMode.MARKDOWN)


# Основна функція
async def main():
    # Запускаємо відправку стартового повідомлення в першому потоці
    await cmd_start_bot()

    # Другий потік: надсилаємо пропозиції паралельно з роботою бота
    asyncio.create_task(cmd_send_offer())

    # Стартуємо бота в основному потоці
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
