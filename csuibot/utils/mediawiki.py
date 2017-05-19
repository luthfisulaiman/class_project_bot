import mwclient
import urllib.parse
from urllib.request import urlopen
from bs4 import BeautifulSoup


class MediaWiki:

    def __init__(self, url):
        self._url = url

    def save_url(self):
        try:
            mwclient.Site(self.host, path=self.path)
        except Exception as e:
            raise Exception('Invalid url or url is not WikiMedia endpoint')
        else:
            with open('.url_wiki', 'w') as file:
                file.write(self._url)
            return 'Url saved!'

    def get_list_pages(self):
        results = []
        idx = 0
        limit = 5
        mw = mwclient.Site(self.host, path=self.path)
        pages = mw.random('0', limit=limit)
        for page in pages:
            results.append('/random_wiki_article {}'.format(page['title']))
            idx += 1
            if idx >= limit:
                break
        return results

    def get_page(self, title):
        mw_site = mwclient.Site(self.host, path=self.path)
        mw_page = mwclient.page.Page(mw_site, title)
        mw_images = mw_page.images()
        mw_image = ' - '
        for image in mw_images:
            mw_image = image.imageinfo['url']
            break
        source = 'http://{}/wiki/{}'.format(self.host, urllib.parse.quote(mw_page.name))
        soup = BeautifulSoup(urlopen(source), "html.parser")
        elements = soup.select("#mw-content-text > p")
        content = ''
        for element in elements:
            if element.get_text() is not '':
                content = content + '\n' + element.get_text()
            if len(content) > 360:
                break
        return '{}\n\n{}\n\nimage: {}\n\nsource: {}'.format(
            mw_page.name, content.strip(), mw_image, source
        )

    @property
    def host(self):
        return urllib.parse.urlparse(self._url).hostname

    @property
    def path(self):
        return urllib.parse.urlparse(self._url).path.rstrip('api.php')
