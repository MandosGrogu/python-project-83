from urllib.parse import urlparse

from bs4 import BeautifulSoup


def url_parse(data):

    parsed = urlparse(data)
    data = f'{parsed.scheme}://{parsed.netloc}'
    return data


def normalize(text):

    res_text = text
    if len(text) > 200:
        res_text = text[0:200] + '...'
    return res_text


def html_parse(text):

    res_dict = {}
    s = BeautifulSoup(text, 'html.parser')
    h1 = normalize(s.find('h1').get_text()) if s.find('h1') is not None else ''
    res_dict['h1'] = h1
    t = normalize(s.find('title').get_text()) \
    if s.find('title') is not None else ''
    res_dict['title'] = t
    if s.find('meta') is not None and 'name' in s.find('meta').attrs.keys() \
    and s.find('meta')['name'] == 'description':
        descr = normalize(s.find('meta')['content'])
    else:
        descr = ''
    res_dict['descr'] = descr
    return res_dict
    