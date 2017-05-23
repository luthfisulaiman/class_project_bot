from bs4 import BeautifulSoup
import urllib.request
import  urllib.error
import re

def Enterkomputer(category, item):
    url = urllib.request.Request("http://www.enterkomputer.com", headers={'User-Agent': 'Mozilla/5.0'})
    req = urllib.request.urlopen(url)
    soup = BeautifulSoup(req, "html.parser")
    links = soup.findAll('a', text=re.compile('^(?i).*%s.*$'%category))
    target_link = ""
    if (len(links) == 0):
        return("Category not found")
    else:
        for link in links:
            if ("http" in link['href']):
                target_link = link['href']

        url = urllib.request.Request(target_link, headers={'User-Agent': 'Mozilla/5.0'})
        req = urllib.request.urlopen(url)
        soup = BeautifulSoup(req, "html.parser")


        items = soup.findAll('tr')
        result = ''
        for res in items:
            td_list = res.find_all('td')
            if (re.compile('^(?i).*%s.*$'%item).match(td_list[0].text)):
                if (len(td_list) == 2):
                    result += td_list[0].text[:-8] + " - " + td_list[1].text + "\n"
                elif (len(td_list) == 3):
                    result += td_list[0].text[:-8] + " - " + td_list[1].text + ' - ' + td_list[2].text + "\n"
        return result

        if not result:
            print("Item Not Found")


