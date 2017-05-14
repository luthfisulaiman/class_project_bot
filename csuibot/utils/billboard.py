from xml.etree import ElementTree as ET
import requests
chart_urls = {
    '200': 'http://www.billboard.com/rss/charts/billboard-200',
    'hot100': 'http://www.billboard.com/rss/charts/hot-100',
    'tropical': 'http://www.billboard.com/rss/charts/tropical-songs'
}


def get_top10(chart_category):
    try:
        chart_url = chart_urls[str(chart_category)]
    except KeyError:
        return 'Invalid chart category'
    chart_xml_text = requests.get(chart_url).text
    items = parse_chart_xml(chart_xml_text)
    result = {
        'title': chart_category,
        'items': items
    }
    return result


def parse_chart_xml(chart_xml):
    root = ET.ElementTree(ET.fromstring(chart_xml))
    elements = root.find('channel').findall('item')
    items = [elements[i] for i in range(0, 10)]
    return items
