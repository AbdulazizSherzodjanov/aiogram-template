from aiogram import types
import time
from data.config import ADMINS
from loader import db,dp,bot
from states.reklama import sendReklom
from aiogram.dispatcher import FSMContext
@dp.message_handler(text="/alluser",user_id=ADMINS)
async def get_all_users(message: types.Message):
    users = db.select_all_users()
    print(users[0][0])
    await message.answer(users)

@dp.message_handler(text="/reklama",user_id=ADMINS,state=None)
async def send_ad_to_all(message:types.Message):
    await message.answer("Reklama yuboring!")
    await sendReklom.ad.set()

@dp.message_handler(content_types=types.ContentType.ANY,state=sendReklom.ad)
async def send_ad(message:types.Message,state:FSMContext):
    await state.finish()
    users = db.select_all_users()

    if message.content_type == "photo":
        file_id = message.photo[-1]['file_id']
        caption = message.caption
        for user in users:
            user_id = user[0]
            await bot.send_photo(chat_id=user_id,photo=file_id,caption=f"{caption}")
            time.sleep(0.25)
    else:
        for user in users:
            user_id = user[0]
            await bot.send_message(chat_id=user_id,text=f"{caption}")
            time.sleep(0.25)            

    # users = db.select_all_users()
    # for user in users:
    #     user_id = user[0]
    #     await bot.send_message(chat_id=user_id,text="Reklama")
    #     time.sleep(1)