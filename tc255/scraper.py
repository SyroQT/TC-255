"""Scrapes an n ammount of data from an ebay search
of keyword
"""
import math

from bs4 import BeautifulSoup
import pandas as pd
import requests


def scrape_ebay(keyword: (str), n: (int) = 3000):
    """Scrapes ebay for keyword and return dataframe
    of size n
    """
    data = {
        'category': [],
        'title': [],
        'price': [],
        'item_url': [],
        'img_url': [],
    }
    headers = {"User-Agent": "Mozilla/5.0"}

    # Calculate how many pages need to be checked
    steps = math.ceil(n / 200)

    for step in range(1, steps+1,):
        url = f'https://www.ebay.com/sch/i.html?_nkw={keyword}\
            &_sacat=0&_ipg=200&_pgn={step}'
        r = requests.get(url, headers=headers)

        soup = BeautifulSoup(r.content, "html.parser")
        items_list = soup.find_all('div', class_='s-item__wrapper clearfix')

        for item in items_list:
            # category
            data['category'].append(
                keyword
            )
            # title
            data['title'].append(
                item.find('a',
                          class_='s-item__link').text
            )
            # price
            data['price'].append(
                item.find('span',
                          class_='s-item__price').text[1:]
            )

            items_urls = item.find('div', class_="s-item__image-section")
            # item_url
            data['item_url'].append(
                item.find('a',
                          class_='s-item__link')['href']
            )
            # img_url
            img = items_urls.find('img',
                                  class_='s-item__image-img')['src']
            data['img_url'].append(img)

    df = pd.DataFrame(data)

    # Return only n rows
    shape = df.shape[0]
    if shape > n:
        to_drop = shape - n
        df.drop(df.tail(to_drop).index, inplace=True)

    return df
