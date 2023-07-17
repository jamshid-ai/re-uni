import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve()

load_dotenv()

DOMAIN = os.environ.get('DOMAIN', 'http://127.0.0.1:8000')
APP_ENVIRONMENT = os.environ.get('APP_ENV', 'development')

BOT_TOKEN = os.environ.get('BOT_TOKEN')
WEBHOOK_PATH = f'/{BOT_TOKEN}/webhook'
WEBHOOK_URL = f'{DOMAIN}{WEBHOOK_PATH}'
BOT_PUBLIC_PORT = os.environ.get('BOT_PUBLIC_PORT', 8080)

DB_URL = os.environ.get('DB_URL')
REDIS_HOST = os.environ.get('REDIS_HOST', 'redis')
REDIS_PORT = os.environ.get('REDIS_PORT', 6379)
APP_DIR: Path = Path(__file__).parent
LOCALES_DIR = APP_DIR / 'locales'

DATABASES = {
    'FSM': 2,
    'CUSTOM_DATA': 4
}

BOT_ROOT = os.path.join(BASE_DIR, "edubot")