import random
import time

import aiohttp
import datetime
import logging
import xml.etree.ElementTree as ET

from ..exceptions import *
from .types import *


async def parse_result(post_element):


    id = int(post_element.get('id'))
    height = int(post_element.get('height'))
    width = int(post_element.get('width'))
    url = post_element.get('file_url')

    sample_height = int(post_element.get('sample_height'))
    sample_width = int(post_element.get('sample_width'))
    sample_url = post_element.get('sample_url')

    sample_post = Rule34SamplePost(sample_height, sample_width, sample_url, id)

    preview_height = int(post_element.get('preview_height'))
    preview_width = int(post_element.get('preview_width'))
    preview_url = post_element.get('preview_url')

    preview_post = Rule34PreviewPost(preview_height, preview_width, preview_url, id)

    score = int(post_element.get('score'))
    rating = post_element.get('rating')
    creator_id = int(post_element.get('creator_id'))
    tags = post_element.get('tags')
    has_children = post_element.get('has_children') == 'true'
    created_date = datetime.datetime.strptime(post_element.get('created_at'), "%a %b %d %H:%M:%S %z %Y")
    status = post_element.get('status')
    source = post_element.get('source')
    has_notes = post_element.get('has_notes') == 'true'
    has_comments = post_element.get('has_comments') == 'true'

    main_post = Rule34MainPost(score, rating, creator_id, tags, has_children, created_date, status,
                               source, has_notes, has_comments, height, width, url, id)

    return main_post, sample_post, preview_post

class Rule34Api:
    def __init__(self):
        self.header = {'User-Agent': 'rule34-simple-api 0.1.5.3 (Request)'}
    async def get_post_count(self, tags: str = '') -> int:
        async with aiohttp.ClientSession(headers=self.header) as session:
            async with session.get(f'https://api.rule34.xxx/index.php?'
                                   f'page=dapi&s=post&q=index&tags={tags}') as response:
                xml_data = await response.text()

        xml_root = ET.fromstring(xml_data)

        return int(xml_root.get('count'))

    async def get_post(self, id: int):
        st = time.time()

        async with aiohttp.ClientSession(headers=self.header) as session:
            async with session.get(f'https://api.rule34.xxx/index.php?'
                                   f'page=dapi&s=post&q=index&id={id}') as response:
                xml_data = await response.text()

        try:
            xml_root = ET.fromstring(xml_data)
        except:
            return None

        post_element = xml_root.find('post')

        parsed = await parse_result(post_element)

        if parsed is None:
            return None
        else:
            main_post, sample_post, preview_post = parsed

        logging.info(f"Post where found in {time.time() - st}s")

        return Rule34PostData(id, main_post, sample_post, preview_post)

    async def get_random_post(self, tags: str = '', forbidden_tags: list[str] = []):
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

        logging.info(f"Random post where found in {time.time() - start_time}s")

        return post_list_[random.randint(0, len(post_list_) - 1)] if len(post_list_) > 0 else None

    async def get_random_posts(self, tags: str = '', count: int = 8, forbidden_tags: list[str] = []) -> list[Rule34PostData]:
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

        logging.info(f"{count} random posts where found in {time.time() - st}s")

        return getted

    async def get_post_list(self, limit: int = 1000, page_id: int = 0, tags: str = '', forbidden_tags: list[str] = [])\
            -> list[Rule34PostData]:
        async with aiohttp.ClientSession(headers=self.header) as session:
            if limit > 1000:
                raise ToBigRequestException(f"The max size of request is 1000 when you tried to request {limit}")

            start_time = time.time()

            async with session.get(f'https://api.rule34.xxx/index.php?'
                                   f'page=dapi&s=post&q=index&limit={limit}&pid={page_id}&tags={tags}') as response:
                xml_data = await response.text()

            logging.debug(f"Request with {limit} limit posts were done in {time.time() - start_time}s")

            xml_root = ET.fromstring(xml_data)
            posts = xml_root.findall('post')
            post_list = []

            start_time = time.time()

            for post_element in posts:
                parsed = await parse_result(post_element)

                if parsed is None:
                    return []
                else:
                    main_post, sample_post, preview_post = parsed

                post_list.append(Rule34PostData(main_post.id, main_post, sample_post, preview_post))

            logging.debug(f"Creating {len(posts)} objects was done in {time.time() - start_time}s")

            post_list_ = []

            for post in post_list:
                if any(tag in forbidden_tags for tag in post.main.tags):
                    pass
                else:
                    post_list_.append(post)

            logging.info(f"{len(post_list_)} posts where found in {time.time() - start_time}s")

            return post_list_
