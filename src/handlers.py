from asyncio import sleep
from aiogram import types

import db
from config import DAILY_LIMIT
from core import dp
from services import send_cat


@dp.message_handler(commands=['start'])
async def welcome(message: types.Message):
    """This handler will be called when user sends `/start` command."""
    if not db.user_exists(message.from_user.id):
        db.create_user(message.from_user.id)
    await message.answer(text='Приветики😽')


@dp.callback_query_handler(lambda callback: callback.data == 'cat')
async def cat(call: types.CallbackQuery):
    """This handler will be called when user interacts with the cat keyboard."""
    await call.answer(text='😽😽😽😽😽😽😽😽😽')
    await call.message.answer_chat_action(action='typing')
    await sleep(1)

    counter = db.get_limit_counter(call.from_user.id)
    if counter + 1 == DAILY_LIMIT:
        await send_cat(telegram_id=call.from_user.id, type='night')
    elif counter < DAILY_LIMIT:
        await send_cat(telegram_id=call.from_user.id)
    else:
        await call.message.answer(text='На сегодня всё 😿')
