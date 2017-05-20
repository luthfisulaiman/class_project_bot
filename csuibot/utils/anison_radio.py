import requests
import pydub
import psycopg2


class PersistentStorage:
    POSTGRES_HOST = "ec2-54-83-26-65.compute-1.amazonaws.com"
    POSTGRES_DB = "desfv1778rcs9q"
    POSTGRES_USERNAME = "idqeyhxhszyuek"
    POSTGRES_PORT = 5432
    POSTGRES_PASSWORD = "9b89a50509da6d8fcf2250c9a74343b811c75e01b02b7ca223c5cf9635a4eabe"
    TABLE_SCHEMA = """
                   CREATE TABLE IF NOT EXIST love_live_song(
                   ID SERIAL PRIMARY KEY,
                   song_name VARCHAR(255) NOT NULL,
                   artist_name VARCHAR(255) NOT NULL,
                   preview_url VARCHAR(255) NOT NULL
                   )
                   """

    def __init__(self):
        try:
            conn = psycopg2.connect(
                                    dbname=self.POSTGRES_DB,
                                    user=self.POSTGRES_USERNAME,
                                    password=self.POSTGRES_PASSWORD,
                                    host=self.POSTGRES_HOST,
                                    port=self.POSTGRES_PORT
                                    )
        except Exception as e:
            raise e

    def get_song(self):
        pass

    def store_song(self):
        pass

    def create_table_schema(self):
        pass


class ClipHandler:
    LOVE_LIVE_API_URL = "http://schoolido.lu/api/songs/?search={search}"
    ITUNES_LOOKUP_URL = "https://itunes.apple.com/lookup?id={id}"

    def add_song(self):
        pass

    def remove_song(self):
        pass

    def send_clip(self):
        pass

    def get_clip_from_itunes(self)
        pass

    def convert_aac_to_mp3(self):
        pass

class anison_radio:
    @classmethod
    def get_clip(cls):
        pass

    @classmethod
    def search_song(cls):
        pass

    @classmethod
    def add_song(cls):
        pass

    @classmethod
    def remove_song(cls):
        pass
