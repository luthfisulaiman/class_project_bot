from flask import Flask, request, abort
import telebot

app = Flask(__name__)
app.config.from_object('{}.config'.format(__name__))

bot = telebot.TeleBot(app.config['TELEGRAM_BOT_TOKEN'], threaded=False)

from . import handlers  # noqa

# Why do this? See https://core.telegram.org/bots/api#setwebhook
webhook_url_path = '/{}'.format(app.config['TELEGRAM_BOT_TOKEN'])
webhook_url_base = app.config['WEBHOOK_HOST']

# Configure application logging
app.logger.setLevel(app.config['LOG_LEVEL'])


@app.route('/')
def index():
    return 'Bot is running'


@app.route(webhook_url_path, methods=['POST'])
def webhook():
    json_data = get_req_body_as_json()
    if json_data is not None:
        app.logger.debug('Update received')
        update = telebot.types.Update.de_json(json_data)
        bot.process_new_messages([update.message])
        return ''
    else:
        return abort(403)


def get_req_body_as_json():
    return request.get_json(silent=True)


if app.config['APP_ENV'] != 'development':  # pragma: no cover
    bot.set_webhook(url='{}{}'.format(webhook_url_base, webhook_url_path))
