#!/usr/bin/env python

import requests
from lxml import html


powerball_url = 'http://www.powerball.com/powerball/pb_numbers.asp'


def gather_page():
    r = requests.get(powerball_url)
    return r.text


def select_date(parsed_page):
    try:
        return parsed_page.cssselect('tr:nth-child(2) .link_white b')[0].text.strip()
    except IndexError:
        return '(Date Not Available)'


def select_numbers(parsed_page):
    return [x.text for x in parsed_page.cssselect('tr:nth-child(2) b font')]


def parse_page(text):
    return html.fromstring(text)


def output(date, numbers):
    return 'The Following Powerball Numbers Were Selected {}:\n\n{}\n'.format(date, '\t'.join(numbers))


def main():
    parsed = parse_page(gather_page())
    date = select_date(parsed)
    nums = select_numbers(parsed)
    to_print = output(date, nums)

    print to_print

if __name__ == '__main__':
    main()
