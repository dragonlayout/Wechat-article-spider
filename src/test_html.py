#!/usr/bin/python
# coding=utf-8
from bs4 import BeautifulSoup

if __name__ == '__main__':
    with open('1.html') as html_str:
        soup = BeautifulSoup(html_str, features='html.parser')
        for img_tag in soup.find_all(name='img'):
            img_attrs: dict = img_tag.attrs
            print(type(img_attrs))
            print(img_attrs.get('data-src'))

        # img_tag = soup.img
        # data-src data-backsrc src
        # print(img_tag.attrs)
        # src_url = soup.img['data-src'] or soup.img['data-backsrc'] or soup.img['src']
        # print(src_url)
