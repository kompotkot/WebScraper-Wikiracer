import aiohttp

import re
from yarl import URL
from requests.utils import requote_uri

from bs4 import BeautifulSoup as bf

# from wikiracer.db import db


def url_cleaner(raw_url_list: list, dct) -> set:
    """
    Find urls with proper origins and return set of them
    """
    url_set = set()

    for url in raw_url_list:
        url = URL(url)

        if url.host is None:
            if '.' not in url.path:
                if url.path[:5] == '/wiki' and url.path != '/wiki/Main_Page':
                    if len(url.path) > 1:
                        url_set.add(requote_uri(url.path))

    # Remove urls which we already have in DB
    known_urls = {i for i in dct.keys()}
    url_set.difference_update(known_urls)

    return url_set


async def fetch(session: aiohttp.client.ClientSession, url: str, dct) -> set:
    print(f'Fetching: {url}')

    async with session.get(url) as response:
        html = await response.text()

        # Get all href from response
        # url_list = re.findall('href="(.[^"]+)"', html)
        soup = bf(html, features="lxml")
        url_list = [a['href'] for a in soup.find_all('a', href=True)]
        # Clean url set from trash values
        cleared_url_set = url_cleaner(url_list, dct)
        return cleared_url_set


async def request(dct, origin_url, path: str, parent: str, work_depth: int) -> None:
    url = f'https://en.{origin_url}{path}'

    async with aiohttp.ClientSession() as session:
        cleared_url_dct = await fetch(session, url, dct)

        # Update dct we work with
        dct.update({path: {'depth': work_depth, 'parent': parent, 'parsed': True}})

        # Add new urls
        # await db.add_many(cleared_url_dct, path, work_depth + 1)
        for url in cleared_url_dct:
            # Check if new url we inserted in dictionary is not parsed url in this cycle
            if url != path:
                dct.update({url: {'depth': work_depth + 1, 'parent': path, 'parsed': False}})
