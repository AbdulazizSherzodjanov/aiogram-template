from aiogram import types
import sqlite3
from aiogram.dispatcher.filters.builtin import CommandStart

from data.config import ADMINS
from loader import dp, db, bot


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    name = message.from_user.full_name
    usern = message.from_user.username

    try:
        db.add_user(id=message.from_user.id,
                    name=name,username=usern)
    except sqlite3.IntegrityError as err:
        # await bot.send_message(chat_id=ADMINS[0],text=err)
        pass

    count = db.count_users()[0]

    msg = f"{message.from_user.full_name} bazaga qo'shildi.\n Bazada {count} ta foydalanuvchi bor."
    await bot.send_message(chat_id=ADMINS[0],text=msg) 
    await message.answer(f"Salom, {message.from_user.full_name}!")
