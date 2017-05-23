import json

import pytest


@pytest.fixture
def client():
    """Return Flask test client that is configured for testing.

    Testing configuration should be placed in `tests/.env` file.
    """
    from csuibot import app
    app.config['TESTING'] = True
    return app.test_client()


def do_post(client, payload):
    config = client.application.config
    base_path = '/{}'.format(config['TELEGRAM_BOT_TOKEN'])
    return client.post(base_path, data=json.dumps(payload),
                       content_type='application/json')


def test_get_index(client):
    rv = client.get('/')

    assert rv.status_code == 200
    assert rv.get_data(as_text=True) == 'Bot is running'


def test_post_webhook(client, mocker):
    mocked_process = mocker.patch('csuibot.bot.process_new_messages')
    payload = dict(update_id=12345)
    rv = do_post(client, payload)

    assert rv.status_code == 200
    assert mocked_process.called


def test_invalid_json_data(client, mocker):
    with client as cli:
        mocker.patch('csuibot.get_req_body_as_json', return_value=None)
        mocked_abort = mocker.patch('csuibot.abort', return_value='Oops')

        do_post(cli, {})

        assert mocked_abort.called_once_with(403)
