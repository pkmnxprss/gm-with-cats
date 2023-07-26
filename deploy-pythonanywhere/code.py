# --------------------------------------------------- #
#  Source code for pythonanywhere.com deploy.         #
#                                                     #
#  pyTelegramBotAPI + webhook + flask                 #
# --------------------------------------------------- #

from telebot import TeleBot, types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.apihelper import ApiTelegramException
from flask import Flask, request, abort
import requests
import sqlite3
from time import sleep
import logging

# ----------------    secret!    ---------------- #
BOT_TOKEN = ''
SECRET = '646f3ba8-7073-43de-ba41-ecc73250cbfd'  # random string
WEBHOOK_HOST = "https://gmwcbot.pythonanywhere.com/"
WEBHOOK_URL = WEBHOOK_HOST + SECRET
DB_NAME = 'db.sqlite3'
CAT_URL = 'https://cataas.com/cat'
# CAT_URL = 'http://aws.random.cat/meow'  # Don't work, because of redirect to non-whitelist URL.
DAILY_LIMIT = 10
# ----------------------------------------------- #

bot = TeleBot(token=BOT_TOKEN, threaded=False)

bot.remove_webhook()
sleep(1)
# Use lower values to limit the load on your bot’s server
bot.set_webhook(url=WEBHOOK_URL, max_connections=10, drop_pending_updates=True)

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

# ----------------------------------------------- #
#                   database                      #
# ----------------------------------------------- #

def initialise() -> None:
    with sqlite3.connect(DB_NAME) as connection:
        cursor = connection.cursor()
        query = '''
            CREATE TABLE IF NOT EXISTS users
            (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id     INTEGER,
                limit_counter   INTEGER
            )
                '''
        cursor.execute(query)
        connection.commit()


def create_user(telegram_id: int) -> None:
    with sqlite3.connect(DB_NAME) as connection:
        cursor = connection.cursor()
        query = '''
            INSERT INTO users (telegram_id, limit_counter)
            VALUES (?, 0)
                '''
        params = (telegram_id,)
        cursor.execute(query, params)
        connection.commit()


def user_exists(telegram_id: int) -> bool:
    with sqlite3.connect(DB_NAME) as connection:
        cursor = connection.cursor()
        query = '''
            SELECT *
            FROM users
            WHERE telegram_id = ?
                '''
        params = (telegram_id,)
        cursor.execute(query, params)
        return bool(cursor.fetchone())


def get_users() -> list:
    with sqlite3.connect(DB_NAME) as connection:
        cursor = connection.cursor()
        query = '''
            SELECT telegram_id
            FROM users
                '''
        cursor.execute(query)
        return cursor.fetchall()


def get_limit_counter(telegram_id: int) -> int:
    with sqlite3.connect(DB_NAME) as connection:
        cursor = connection.cursor()
        query = '''
            SELECT limit_counter
            FROM users
            WHERE telegram_id = ?
                '''
        params = (telegram_id,)
        cursor.execute(query, params)
        return cursor.fetchone()[0]


def increase_limit_counter(telegram_id: int) -> None:
    with sqlite3.connect(DB_NAME) as connection:
        cursor = connection.cursor()
        query = '''
            UPDATE users
            SET limit_counter = limit_counter + 1
            WHERE telegram_id = ?
                '''
        params = (telegram_id,)
        cursor.execute(query, params)
        connection.commit()


def reset_limit_counter() -> None:
    with sqlite3.connect(DB_NAME) as connection:
        cursor = connection.cursor()
        query = '''
            UPDATE users
            SET limit_counter = 0
                '''
        cursor.execute(query)
        connection.commit()


# ----------------------------------------------- #
#                 end of database                 #
# ----------------------------------------------- #


def get_cat_keyboard(limit_counter: int) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    return markup.add(InlineKeyboardButton(
        text='Мяу😸({}/{})'.format(limit_counter+1, DAILY_LIMIT),
        callback_data='cat'))


def send_cat(telegram_id: int, chat_id: int, type=None, first_name='Unknown') -> None:
    logging.info('Sending a cat to {}...'.format(first_name))
    try:
        response = requests.get(url=CAT_URL, timeout=10)
        try:
            bot.send_message(chat_id=chat_id, text='💕')
            bot.send_message(chat_id=chat_id, text='💫')
            if type == 'morning':
                bot.send_photo(chat_id=chat_id,
                               photo=response.content,
                               caption='🌈☀️ ☁️☁️☁️☁️☁️☁️☀️🌈\n'
                                       '😽😸 _Доброе утречко!_ 😸😽',
                               parse_mode='Markdown',
                               reply_markup=get_cat_keyboard(get_limit_counter(telegram_id)))
            elif type == 'night':
                bot.send_photo(chat_id=chat_id,
                               photo=response.content,
                               caption='🌙🌑 ✨✨✨ ✨✨✨ 🌑🌙\n'
                                       '😽💖 _Спокойной ночки!_ 💖😽',
                               parse_mode='Markdown',
                               reply_markup=get_cat_keyboard(get_limit_counter(telegram_id)))
            else:
                bot.send_photo(chat_id=chat_id,
                               photo=response.content,
                               reply_markup=get_cat_keyboard(get_limit_counter(telegram_id)))

            increase_limit_counter(telegram_id)

        except ApiTelegramException as e:
            logging.warning('{}'.format(e))
    except:
        logging.error('Can`t fetch a cat from {}'.format(CAT_URL))


# ----------------------------------------------- #
#                   handlers                      #
# ----------------------------------------------- #

@bot.message_handler(commands=['start'])
def welcome(message: types.Message):
    if not user_exists(message.from_user.id):
        create_user(message.from_user.id)
        logging.info(f'{message.from_user.first_name} has joined the bot.')
    bot.send_message(chat_id=message.from_user.id, text='Приветики😽')


@bot.callback_query_handler(lambda callback: callback.data == 'cat')
def cat(call: types.CallbackQuery):
    counter = get_limit_counter(call.from_user.id)
    if counter + 1 == DAILY_LIMIT:
        bot.answer_callback_query(callback_query_id=call.id)
        send_cat(
            telegram_id=call.from_user.id,
            chat_id=call.message.chat.id,
            type='night',
            first_name=call.from_user.first_name
        )
    elif counter < DAILY_LIMIT:
        bot.answer_callback_query(callback_query_id=call.id)
        send_cat(
            telegram_id=call.from_user.id,
            chat_id=call.message.chat.id,
            first_name=call.from_user.first_name
        )
    else:
        bot.answer_callback_query(callback_query_id=call.id, text='На сегодня всё 😿', show_alert=True)


# ----------------------------------------------- #
#                     flask                       #
# ----------------------------------------------- #

@app.route('/{}'.format(SECRET), methods=["POST"])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        try:
            json_string = request.stream.read().decode('utf-8')
            update = types.Update.de_json(json_string)
            bot.process_new_updates([update])
            return 'ok', 200
        except:
            logging.warning('BAD DATA')
            abort(400)
    else:
        abort(403)


# Empty webserver index, return nothing, just HTTP 200  todo: webhook controller
@app.route('/')
def index():
    return '<h1 style="color: silver; text-align: center">GMWC</h1>'


# ----------------------------------------------- #
initialise()
# ----------------------------------------------- #
