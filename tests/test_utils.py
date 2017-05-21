from csuibot import utils, config
from csuibot.utils import plant as p
from csuibot.utils import data_processor as processor
from csuibot.utils.message_dist import add_message_to_dist, get_message_dist
import os
import re
from requests.exceptions import ConnectionError
import requests
import json


class TestPreview:

    def test_valid(self):
        res = utils.preview_music("Supercell")
        assert res == "success"

    def test_invalid(self):
        res = utils.preview_music("Ilyas Fahreza")
        assert res == "Can\'t found the requested artist"
