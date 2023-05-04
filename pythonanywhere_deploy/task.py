#!/home/gmwcbot/venv/bin/python3
# --------------------------------------------------- #
#  Scheduled task.                                    #
#  According to the idea of this project, the task    #
#  should be performed once every morning.            #
# --------------------------------------------------- #

if __name__ == '__main__':
    from main import get_users, reset_limit_counter, send_cat

    reset_limit_counter()
    for user in get_users():
        send_cat(telegram_id=user[0], chat_id=user[0], type='morning')
