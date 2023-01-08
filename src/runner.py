import logging
from aiogram import executor

import db
import handlers
from core import dp

# Configure logging
logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    db.initialise()

    # Run bot in long-polling mode
    executor.start_polling(dp, skip_updates=True)
