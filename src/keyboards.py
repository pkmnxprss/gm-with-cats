from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import DAILY_LIMIT


def get_cat_keyboard(limit_counter: int) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(
        text='Мяу😸({}/{})'.format(limit_counter, DAILY_LIMIT),
        callback_data='cat')
    )
    return markup
