from telebot import TeleBot, types
from flask import Flask, request, abort
from time import sleep

TOKEN = ''
SECRET = '646f3ba8-7073-43de-ba41-ecc73250cbfd'
WEBHOOK_HOST = "https://gmwcbot.pythonanywhere.com/"  # do not forget to change username!
WEBHOOK_URL = WEBHOOK_HOST + SECRET

bot = TeleBot(TOKEN, threaded=False)

bot.remove_webhook()
sleep(1)
bot.set_webhook(url=WEBHOOK_URL, max_connections=1)  # use lower values to limit the load on your bot’s server

app = Flask(__name__)


@app.route('/{}'.format(SECRET), methods=["POST"])
def telegram_webhook():
    if request.headers.get('content-type') == 'application/json':
        # json_string = request.get_data().decode('utf-8')
        json_string = request.stream.read().decode('utf-8')
        update = types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return 'ok', 200
    else:
        abort(403)


# Empty webserver index, return nothing, just HTTP 200
@app.route('/')
def index():
    return 'Hello from Flask!'


# Bot program code ...
@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, 'Hello')
