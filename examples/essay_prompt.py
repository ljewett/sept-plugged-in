#!/usr/bin/env python

from lxml import html as lxml
import requests
from random import randint

def get_page():
    headers = {'User-Agent': ''}
    return requests.get('https://magoosh.com/gre/2016/gre-essay-topics/', headers=headers)

def is_prompt(paragraph):
    cleaned = unicode(paragraph).strip()
    return cleaned.startswith(u'\u201c')

def gather_items(text):
    parsed = lxml.fromstring(text)
    items = parsed.cssselect('p')
    return filter(lambda x: is_prompt(x.text), items)

def main():
    r = get_page()
    items = gather_items(r.text)
    rand = randint(0, len(items) - 1)
    print items[rand].text.strip()

if __name__ == '__main__':
    main()
