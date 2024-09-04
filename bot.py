import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.enums import ParseMode
# from aiogram.client.session.aiohttp import AiohttpSession

from main import MainProgram

from manage_text import ManagerText

from config import (
    API,
    IDs,
    PROXY
)

# session = AiohttpSession(proxy=PROXY)

bot = Bot(token=API, )  # session = session

dp = Dispatcher()

mt = ManagerText()

mp = MainProgram()


@dp.message(CommandStart())
async def cmd_start(message: Message):
    text = mt.get_start_text()

    await message.answer(
        text=text,
        parse_mode=ParseMode.MARKDOWN
    )


@dp.message(Command('help'))
async def cmd_help(message: Message):
    text = mt.get_help_text()

    await message.answer(
        text=text,
        parse_mode=ParseMode.MARKDOWN
    )


@dp.message(Command('add'))
async def cmd_add(message: Message):
    change_cmd = mt.change_cmd_add(message.text)

    print(change_cmd)

    flag = change_cmd[0]
    district, url = change_cmd[1]
    text = change_cmd[2]
    if flag:
        res = mp.set_url(
            name=district,
            url=url
        )

    if not res[0]:
        text = res[1]

    await message.answer(
        text=text,
        parse_mode=ParseMode.MARKDOWN
    )


@dp.message(Command('week'))
async def cmd_week(message: Message):
    data = mp.get_week()

    text = mt.change_week_text(
        data=data
    )

    await message.answer(
        text=text,
        parse_mode=ParseMode.MARKDOWN
    )

@dp.message(Command('district'))
async def cmd_district(message: Message):
    dis = mp.get_district()

    text = mt.get_district_text(
        txt=dis
    )

    await message.answer(
        text=text,
        parse_mode=ParseMode.MARKDOWN
    )

# @dp.message()
async def cmd_send_offer():
    await asyncio.sleep(60)

    data = mp.get_clear_data()

    text = mt.change_ofer_text(
        urls=data
    )

    for id in IDs:
        await bot.send_message(
            chat_id=id,
            text=text,
            parse_mode=ParseMode.MARKDOWN
        )




async def main():
    asyncio.create_task(cmd_send_offer())
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
