from os import environ


APP_ENV = environ.get('APP_ENV', 'development')
DEBUG = environ.get('DEBUG', 'true') == 'true'
TELEGRAM_BOT_TOKEN = environ.get('TELEGRAM_BOT_TOKEN', 'randomstring')
LOG_LEVEL = environ.get('LOG_LEVEL', 'DEBUG')
WEBHOOK_HOST = environ.get('WEBHOOK_HOST', 'https://csui-bot-lightmire.herokuapp.com/')
IMAGGA_API_KEY = environ.get('IMAGGA_API_KEY', 'somerandomstring')
IMAGGA_API_SECRET = environ.get('IMAGGA_API_SECRET', 'somerandomstring')
DANDELION_KEY = environ.get('DANDELION_KEY')
