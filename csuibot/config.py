from os import environ


mytoken = '374007525:AAEP0C78JLnn6oq-wK2xs2LfY0rsavW9j88'
APP_ENV = environ.get('APP_ENV', 'development')
DEBUG = environ.get('DEBUG', 'true') == 'true'
TELEGRAM_BOT_TOKEN = environ.get('TELEGRAM_BOT_TOKEN', mytoken)
LOG_LEVEL = environ.get('LOG_LEVEL', 'DEBUG')
WEBHOOK_HOST = environ.get('WEBHOOK_HOST', 'https://newicktreeapp.herokuapps.com')
