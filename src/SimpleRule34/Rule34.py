import random
import time

import aiohttp
import datetime
import logging
import xml.etree.ElementTree as ET

from .exceptions import *
from .types import *


class Rule34Api:
    def __init__(self):
        self.header = {'User-Agent': 'rule34-simple-api 0.1.5.6 (Request)'}
    async def get_post_count(self, tags: str = '') -> int:
        async with aiohttp.ClientSession(headers=self.header) as session:
            async with session.get(f'https://api.rule34.xxx/index.php?'
                                   f'page=dapi&s=post&q=index&tags={tags}') as response:
                xml_data = await response.text()

        xml_root = ET.fromstring(xml_data)

        return int(xml_root.get('count'))

    async def get_post(self, id: int) -> Post:
        st = time.time()

        async with aiohttp.ClientSession(headers=self.header) as session:
            async with session.get(f'https://api.rule34.xxx/index.php?'
                                   f'json=1&page=dapi&s=post&q=index&id={id}') as response:
                if response.status != 200:
                    raise ApiException(f"Api returned status code {response.status} with message"
                                       f" {await response.text()}")

                j = await response.json()
                data = j[0]

        data["main"] = {
            "url": data['file_url']
        }
        data["preview"] = {
            "url": data['preview_url']
        }
        data["tags"] = data["tags"].split(" ")

        logging.debug(f"Post[{id}] where found in {time.time() - st}s")

        return Post(**data)

    async def get_random_post(self, tags: str = '', forbidden_tags: list[str] = []) -> Post:
        start_time = time.time()

        post_count = await self.get_post_count(tags)

        page_count = post_count // 1000

        if page_count > 0:
            post_list = await self.get_post_list(page_id=random.randint(0, page_count if page_count <= 200 else 200),
                                                 tags=tags, limit=1000)

        else:
            post_list = await self.get_post_list(tags=tags, limit=1000)

        post_list_ = []

        for post in post_list:
            if any(tag in forbidden_tags for tag in post.main.tags):
                pass
            else:
                post_list_.append(post)

        logging.debug(f"Random posts where found in {time.time() - start_time}s")

        return post_list_[random.randint(0, len(post_list_) - 1)] if len(post_list_) > 0 else None

    async def get_random_posts(self, tags: str = '', count: int = 8, forbidden_tags: list[str] = []) -> list[Post]:
        st = time.time()

        request_count = 1
        true_count = count*20

        post_list = []

        if true_count > 1000:
            request_count = true_count // 1000

        post_count = await self.get_post_count(tags)
        page_id = int(random.randint(0, int(post_count / true_count)) / 8)  if post_count >= true_count else 0

        for pid in range(request_count + 1):
            post_list += await self.get_post_list(tags=tags, forbidden_tags=forbidden_tags,
                                                  page_id=page_id, limit=true_count if true_count <= 1000 else 1000)

        getted = []

        for x in range(count):
            if len(post_list) > 0:
                getted.append(post_list[random.randint(0, len(post_list) - 1)])
            else:
                pass

        logging.debug(f"{count} random posts where found in {time.time() - st}s")

        return getted

    async def get_post_list(self, limit: int = 1000, page_id: int = 0, tags: str = '', forbidden_tags: list[str] = [])\
            -> list[Post]:
        if limit > 1000:
            raise ToBigRequestException(f"The max size of request is 1000 when you tried to request {limit}")

        async with aiohttp.ClientSession(headers=self.header) as session:
            start_time = time.time()

            async with session.get(f'https://api.rule34.xxx/index.php?'
                                   f'json=1&page=dapi&s=post&q=index&limit={limit}&pid={page_id}&tags={tags}') as response:
                if response.status != 200:
                    raise ApiException(f"Api returned status code {response.status} with message"
                                       f" {await response.text()}")

                data = await response.json()

            logging.debug(f"Request with {limit} limit posts were done in {time.time() - start_time}s")

            post_list = []
            for post_data in data:
                post_data["main"] = {
                    "url": post_data['file_url']
                }
                post_data["preview"] = {
                    "url": post_data['preview_url']
                }
                post_data["tags"] = post_data["tags"].split(" ")

                post_list.append(Post(**post_data))

            start_time = time.time()

            post_list_ = []

            for post in post_list:
                if any(tag in forbidden_tags for tag in post.tags):
                    pass
                else:
                    post_list_.append(post)

            logging.debug(f"{len(post_list_)} posts where found in {time.time() - start_time}s")

            return post_list_
