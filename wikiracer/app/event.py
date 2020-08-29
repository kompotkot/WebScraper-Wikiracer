import asyncio

import time
from itertools import islice

from wikiracer.app.crawler import request


def task_generator(loop, dct: dict, origin_url: str, work_depth: int, parallels: int = 5) -> None:
    """
    Crawl all links for one parent.
    """
    # Create set from dictionary(dct) with proper depth and un-parsed
    links = {link for link in dct.keys() if dct[link]['depth'] == work_depth and dct[link]['parsed'] is False}

    while len(links) > 0:
        # Generate chunk with length according to
        # parallel tasks to avoid dos service
        if len(links) > parallels:
            chunk = set(islice(links, parallels))
        else:
            chunk = links.copy()

        # Task scheduling
        # Scheduling tasks in our loop event, and schedule our coroutines
        tasks = [asyncio.ensure_future(request(dct, origin_url, i, dct[i]['parent'], work_depth)) for i in chunk]
        # Use gather to wait for all pending tasks
        loop.run_until_complete(asyncio.gather(*tasks))

        time.sleep(1)

        # Remove chunk from set of links
        links.difference_update(chunk)


def event_rec(dct: dict, end_url: str, origin_url: str, work_depth: int = 0):
    loop = asyncio.get_event_loop()

    if end_url in dct.keys():
        print(f'\nWe found it! Total links in final dictionary is: {len(dct.keys())}\n'
              f'Chain:\n'
              f'Depth: {dct[end_url]["depth"]}, URL: {end_url}, parent: {dct[end_url]["parent"]}')

        # Print parent chain
        target_parent = dct[end_url]['parent']
        parent_len = dct[end_url]['depth']
        while parent_len > 0:
            # Find in dictionary(dct) link from previous link's parent with lower depth
            p = list(filter(
                lambda elem: elem[0] == target_parent and elem[1]['depth'] == parent_len - 1,
                dct.items()
            ))[0]
            print(f'Depth: {p[1]["depth"]}, URL: {p[0]}, parent: {p[1]["parent"]}')

            target_parent = p[1]['parent']
            parent_len -= 1

    else:
        print(f'\n \nWork depth is: {work_depth}\n \n')
        task_generator(loop, dct, origin_url, work_depth)

        # Restart functions with another depth
        event_rec(dct, end_url, origin_url, work_depth + 1)
