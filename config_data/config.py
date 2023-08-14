import os
from dotenv import load_dotenv, find_dotenv
from utils.exceptions import EnvError

# Проверка наличия новых переменных окружения
if not find_dotenv():
    raise EnvError("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    # Загрузка переменных окружений из файла .env
    load_dotenv()


# Формирование ссылок на переменные окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

# Проверка наличия переменных в файле .env
if not (BOT_TOKEN and API_KEY and API_SECRET):
    raise EnvError('Переменные окружения не загружены, т.к. отсутствует информация о них в файле .env')

# Файл с БД
DB_PATH = 'database/pf_database.db'
