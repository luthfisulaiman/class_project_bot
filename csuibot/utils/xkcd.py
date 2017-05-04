import requests


class Comic:

    # Return alt text and img url of an xkcd comic
    @classmethod
    def get_latest_comic(self):
        # Use xkcd JSON API
        r = requests.get('https://xkcd.com/info.0.json')
        # Check the response status
        r.raise_for_status()
        json = r.json()
        return "{}\n{}".format(json['alt'], json['img'])
