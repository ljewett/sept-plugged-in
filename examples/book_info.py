#!/usr/bin/env python

import re
import requests
import sys
import time

from lxml import html, etree


amazon_url = "https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Dstripbooks&field-keywords="

def get_book_url(text):
    parsed = html.fromstring(text)
    titles = parsed.cssselect('.s-access-detail-page')
    if titles > 0:
        return titles[0].get('href')
    return None

def get_page(url, isbn=''):
    return requests.get(url + str(isbn))

def get_isbn_10(parsed):
    count = len(parsed.cssselect('#productDetailsTable li'))
    return parsed.cssselect('#productDetailsTable li:nth-child({})'.format(count - 8))[0].xpath('./text()')[0].strip()

def get_isbn_13(parsed):
    count = len(parsed.cssselect('#productDetailsTable li'))
    return parsed.cssselect('#productDetailsTable li:nth-child({})'.format(count - 7))[0].xpath('./text()')[0].strip()

def get_title(parsed):
    return parsed.cssselect('#productTitle')[0].text

def clean_text(text):
    text = text.strip()
    text = re.sub(r'<.+?>', '\n', text)
    text = re.sub(r'&.+?;', '', text.encode('ascii'))
    return text

def get_description(parsed):
    try:
        pattern = re.compile(r'<(p|br|div)>(.+?)</\1>')
        full_description = etree.tostring(parsed.cssselect('#bookDescription_feature_div')[0].xpath('./noscript')[0])
        return clean_text(re.search(pattern, full_description).group(2))
    except:
        return "DESCRIPTION NOT FOUND"

def get_image_url(parsed):
    return parsed.cssselect('#imgBlkFront')[0].get('src')

def output(parsed):
    print "\nIMAGE: " + get_image_url(parsed)
    print "\nTITLE:\t\t" + get_title(parsed)
    print "\nISBN 10:\t" + str(get_isbn_10(parsed))
    print "\nISBN 13:\t" + str(get_isbn_13(parsed))
    print "\n\nDESCRIPTION:\n\n" + get_description(parsed).encode('ascii')
    return True

def main():
    if len(sys.argv) == 1:
        print "PLEASE INPUT ISBN"
        return

    for i in xrange(1, 6):
        print "ATTEMPT: %d" % i
        try:
            r = get_page(amazon_url, sys.argv[1])
            url = get_book_url(r.text)
            r = get_page(url)
            parsed = html.fromstring(r.text)
            if output(parsed):
                break
            time.sleep(1)
        except Exception as e:
            print e
            pass


if __name__ == '__main__':
    main()
