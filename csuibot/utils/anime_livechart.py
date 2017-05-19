import requests
from bs4 import BeautifulSoup


def get_anime_list(genre, season, year):
    url = 'https://www.livechart.me/{}-{}/all'.format(season, year)
    page = requests.get(url)
    html = BeautifulSoup(page.content, 'html.parser')
    anime_blocks = html.find_all('article', class_='anime')

    anime_by_genre = []
    for block in anime_blocks:
        tags = block.find(class_='anime-tags').find_all('li')
        genres = [t.get_text() for t in tags]
        if (genre in genres): #check genre
            title = block.find('h3', class_='main-title').get_text()
            synopsis = block.find('div', class_='anime-synopsis').get_text()
            anime = {'title': title, 'synopsis': synopsis}
            anime_by_genre.append(anime)

    return anime_by_genre
