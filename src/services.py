import json
import aiohttp
from aiogram.utils.exceptions import BotBlocked

import db
from core import bot
from keyboards import get_cat_keyboard
from config import CAT_URL


async def send_cat(telegram_id: int, type = None) -> None:
    """This function sends a message with a cat to the user and increases a daily limit counter."""
    db.increase_limit_counter(telegram_id)

    async with aiohttp.ClientSession() as session:
        async with session.get(url=CAT_URL) as response:
            data = json.loads(await response.text())
        async with session.get(url=data[0].get('url')) as response:
            try:
                await bot.send_message(chat_id=telegram_id, text='💕')
                await bot.send_message(chat_id=telegram_id, text='💫')
                if type == 'night':
                    await bot.send_photo(chat_id=telegram_id,
                                         photo=response.content,
                                         caption='🌙🌑 ✨✨✨ ✨✨✨ 🌑🌙\n'
                                                 '😽💖 _Спокойной ночки!_ 💖😽',
                                         parse_mode='Markdown',
                                         reply_markup=get_cat_keyboard(db.get_limit_counter(telegram_id)))
                elif type == 'morning':
                    await bot.send_photo(chat_id=telegram_id,
                                         photo=response.content,
                                         caption='🌈☀️ ☁️☁️☁️☁️☁️☁️☀️🌈\n'
                                                 '😽😸 _Доброе утречко!_ 😸😽',
                                         parse_mode='Markdown',
                                         reply_markup=get_cat_keyboard(db.get_limit_counter(telegram_id)))
                else:
                    await bot.send_photo(chat_id=telegram_id,
                                         photo=response.content,
                                         reply_markup=get_cat_keyboard(db.get_limit_counter(telegram_id)))
            except BotBlocked:
                # Occurs when bot is blocked by the user.
                # Skip this exception because it doesn't matter in this context.
                pass  # todo: delete user from database
