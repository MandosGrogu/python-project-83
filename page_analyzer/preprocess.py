from bs4 import BeautifulSoup
from urllib.parse import urlparse

def url_parse(data):

    parsed = urlparse(data)
    data = f'{parsed.scheme}://{parsed.netloc}'
    return data

def normalize(text):

    res_text = text
    if len(text) > 200:
        res_text = text[0:201] + '...'
    return res_text

def html_parse(text):

    res_dict = {}
    soup = BeautifulSoup(text, 'html.parser')
    h1 = normalize(soup.find('h1').get_text()) if soup.find('h1') is not None else ''
    res_dict['h1'] = h1
    title = normalize(soup.find('title').get_text()) if soup.find('title') is not None else ''
    res_dict['title'] = title
    if soup.find('meta') is not None and 'name' in soup.find('meta').attrs.keys() \
    and soup.find('meta')['name'] == 'description':
        descr = normalize(soup.find('meta')['content'])
    else:
        descr = ''
    res_dict['descr'] = descr
    return res_dict
    