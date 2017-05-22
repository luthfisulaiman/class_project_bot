import requests
import psycopg2
import dropbox

from pydub import AudioSegment


class DatabaseStorage:
    POSTGRES_HOST = "ec2-54-83-26-65.compute-1.amazonaws.com"
    POSTGRES_DB = "desfv1778rcs9q"
    POSTGRES_USERNAME = "idqeyhxhszyuek"
    POSTGRES_PORT = 5432
    POSTGRES_PASSWORD = "9b89a50509da6d8fcf2250c9a74343b811c75e01b02b7ca223c5cf9635a4eabe"
    TABLE_SCHEMA = """
                   CREATE TABLE IF NOT EXIST love_live_song(
                   ID SERIAL PRIMARY KEY,
                   itunes_id INT UNIQUE,
                   japan_name VARCHAR(255) NOT NULL,
                   romaji_name VARCHAR(255),
                   english_name VARCHAR(255),
                   artist_name VARCHAR(255) NOT NULL,
                   preview_url VARCHAR(255) NOT NULL,
                   storage_url VARCHAR(255)
                   );
                   """

    SEARCH_QUERY = """
                   SELECT *
                   FROM love_live_song
                   WHERE itunes_id = %s;
                   """

    ALL_QUERY = """
                SELECT id, japan_name,  artist name
                FROM love_live_song
                """

    INSERT_QUERY = """
                   INSERT INTO love_live_song
                   (itunes_id, japan_name, romaji_name, english_name,
                   artist_name, preview_url, storage_url)
                   VALUES (%s, %s, %s, %s, %s, %s, %s);
                   """

    DELETE_QUERY = """
                   DELETE FROM love_live_song
                   WHERE itunes_id = %s;
                   """

    def __init__(self):
        try:
            self.conn = psycopg2.connect(
                                    dbname=self.POSTGRES_DB,
                                    user=self.POSTGRES_USERNAME,
                                    password=self.POSTGRES_PASSWORD,
                                    host=self.POSTGRES_HOST,
                                    port=self.POSTGRES_PORT
                                    )
        except Exception as e:
            raise e

    def get_song(self, itunes_id):
        cur = self.conn.cursor()

        try:
            cur.execute(self.SEARCH_QUERY, (itunes_id,))
        except psycopg2.ProgrammingError:
            self.create_table_schema()
            cur.execute(self.SEARCH_QUERY, (itunes_id,))
        res = cur.fetchone()
        cur.close()
        return res

    def get_all_songs(self):
        cur = self.conn.cursor()

        try:
            cur.execute(self.ALL_QUERY)
        except psycopg2.ProgrammingError:
            self.create_table_schema()
            cur.execute(self.ALL_QUERY)
        res = cur.getchone()
        cur.close()
        return res

    def store_song(self, val):
        cur = self.conn.cursor()

        try:
            cur.execute(self.INSERT_QUERY, val)
        except psycopg2.ProgrammingError:
            self.create_table_schema()
            cur.execute(self.INSERT_QUERY, val)
        self.conn.commit()
        cur.close()

    def delete_song(self, itunes_id):
        cur = self.conn.cursor()

        cur.execute(self.DELETE_QUERY, (itunes_id,))
        self.conn.commit()
        cur.close()

    def create_table_schema(self):
        cur = self.conn.cursor()
        cur.execute(self.TABLE_SCHEMA)
        self.conn.commit()
        cur.close()


class CloudStorage:
    ACCESS_TOKEN = "zBTjwpY7xaYAAAAAAAAH4hiVQl6j6bH7VAsK5H3aCi-BqLp1a8mlvbiQtZBICZSI"

    def __init__(self):
        self.dbx = dropbox.Dropbox(self.ACCESS_TOKEN)

    def store_file(self, f, filename):
        f.seek(0)
        self.dbx.files_upload(f.read(), "/" + filename)

        url = self.dbx.sharing_create_shared_link("/" + filename).url
        url = url.replace("www.dropbox", "dl.dropboxusercontent")

        return url


class ClipHandler:
    LOVE_LIVE_API_URL = u"http://schoolido.lu/api/songs/?search={search}"
    ITUNES_LOOKUP_URL = "https://itunes.apple.com/lookup?id={id}"

    def __init__(self, need_cloud=False):
        self.db = DatabaseStorage()
        if need_cloud:
            self.storage = CloudStorage()

    def add_song(self, query):
        song = self.search_song(query)
        if not song or song['itunes_id'] is None:
            return "This song not found or doesn't available in itunes :("

        itunes_id = song['itunes_id']

        result = self.db.get_song(itunes_id)
        if result is not None:
            return "This song is already added."

        english_name = song['translated_name']
        romaji_name = song['romaji_name']
        japan_name = song['name']
        artist_name = song['main_unit']
        preview_url = self.get_preview_url(itunes_id)
        storage_url = self.store_song(itunes_id, preview_url)

        values = (itunes_id, japan_name, romaji_name, english_name,
                  artist_name, preview_url, storage_url)

        self.db.store_song(values)
        return "Song successfully added"

    def remove_song(self, query):
        song = self.search_song(query)

        itunes_id = song['itunes_id']
        self.db.delete_song(itunes_id)

        return "Song successfully deleted"

    def get_all_songs(self):
        songlist = self.db.get_all_songs()

    def search_song(self, query):
        r = requests.get(self.LOVE_LIVE_API_URL.format(search=query))
        info_json = r.json()

        if info_json['count'] == 0:
            return False

        return info_json['results'][0]

    def get_preview_url(self, itunes_id):
        r = requests.get(self.ITUNES_LOOKUP_URL.format(id=itunes_id))

        info_json = r.json()

        return info_json['results'][0]['previewUrl']

    def store_song(self, itunes_id, url):
        r = requests.get(url)

        filename = str(itunes_id) + ".m4a"
        f = open(filename, "wb")
        f.write(r.content)
        f.close()

        converted_song = self.convert_m4a_to_mp3(itunes_id)

        return self.storage.store_file(converted_song, str(itunes_id) + ".mp3")

    def send_clip(self, query):
        pass

    def convert_m4a_to_mp3(self, itunes_id):
        song = AudioSegment.from_file   (str(itunes_id) + ".m4a", format="m4a")
        converted_song = song.export(str(itunes_id) + ".mp3")

        return converted_song


class AnisonRadio:
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
