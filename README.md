## Run on your local machine (long-polling)

Get the source code from this repository.

```bash
git clone https://github.com/pkmnxprss/gm-with-cats.git
```

Switch to the working directory and create a new virtual environment.

```bash
cd gm-with-cats/
python3 -m venv venv
source venv/bin/activate
```

Install project dependencies using python package manager pip.

```bash
pip install aiogram
```

Obtain bot token and write it to `src/config.py`

Now you can run app and send cats.

```bash
python3 src/runner.py
python3 src/task.py
```

## Deploy to [pythonanywhere.com](https://www.pythonanywhere.com) (webhook)

1. Create account
2. Add a new web app
3. Select a Flask framework
4. Select python version (e.g. Python 3.10 (Flask 2.1.2))
5. Edit a path to your Flask app (e.g. `/home/<username>/bot/code.py`)
6. Start a new Bash console
7. Create virtual environment `python3 -m venv venv `
8. Go to Web and enter a path to it `/home/<username>/venv`
9. Start a new console in this virtual environment
10. Install dependencies `pip install pyTelegramBotAPI flask`
11. Replace `code.py` and add `task.py` files from `deploy-pythonanywhere` folder
12. Edit config vars
13. Reload web application
14. To send a cat run `python3 bot/task.py` (within venv) or create a scheduled task
