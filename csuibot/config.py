from os import environ


APP_ENV = environ.get('APP_ENV', 'development')
DEBUG = environ.get('DEBUG', 'true') == 'true'
TELEGRAM_BOT_TOKEN = environ.get('TELEGRAM_BOT_TOKEN', 'somerandomstring')
LOG_LEVEL = environ.get('LOG_LEVEL', 'DEBUG')
WEBHOOK_HOST = environ.get('WEBHOOK_HOST', '127.0.0.1')
