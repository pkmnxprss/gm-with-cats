# --------------------------------------------------- #
#  Scheduled task.                                    #
#  According to the idea of this project, the task    #
#  should be performed once every morning.            #
# --------------------------------------------------- #

if __name__ == '__main__':
    from runner import executor
    from db import get_users, reset_limit_counter
    from core import dp
    from services import send_cat

    reset_limit_counter()
    for user in get_users():
        executor.start(dp, send_cat(telegram_id=user[0], type='morning'))
