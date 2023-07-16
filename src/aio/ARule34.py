import random
import time

import aiohttp
import datetime
import logging
import xml.etree.ElementTree as ET

from ..exceptions import *


class Rule34Api:
    async def get_post_count(self, tags: str = '') -> int:
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.rule34.xxx/index.php?'
                                   f'page=dapi&s=post&q=index&tags={tags}') as response:
                xml_data = await response.text()

        xml_root = ET.fromstring(xml_data)

        return int(xml_root.get('count'))

    async def get_post(self, id: int):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.rule34.xxx/index.php?'
                                   f'page=dapi&s=post&q=index&id={id}') as response:
                xml_data = await response.text()

        try:
            xml_root = ET.fromstring(xml_data)
        except:
            return None
        post_element = xml_root.find('post')

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

        return Rule34PostData(id, main_post, sample_post, preview_post)

    async def get_random_post(self, tags: str = ''):
        post_count = await self.get_post_count(tags)

        page_count = post_count // 1000

        if page_count > 0:
            post_list = await self.get_post_list(page_id=random.randint(0, page_count if page_count <= 200 else 200),
                                                 tags=tags, limit=1000)

        else:
            post_list = await self.get_post_list(tags=tags, limit=1000)

        return post_list[random.randint(0, len(post_list) - 1)] if len(post_list) > 0 else None

    async def get_random_posts(self, tags: str = '', count: int = 8) -> list[Rule34PostData]:
        st = time.time()

        all_posts = await self.get_post_count(tags)

        #if count > all_posts:
        #    raise RequestMoreThanAvailableException(f"Only available {all_posts}, while tried to request {count}",
        #                                            count, all_posts)

        request_count = 1

        post_list = []

        if count > 1000:
            request_count = count // 1000

        for pid in range(request_count + 1):
            post_list += await self.get_post_list(tags=tags)

        getted = [post_list[random.randint(0, len(post_list) - 1)] if len(post_list) > 0 else None for x in
                  range(count)]

        logging.debug(f"{count} random posts where found in {time.time() - st}")

        return getted

    async def get_post_list(self, limit: int = 1000, page_id: int = 0, tags: str = '') -> list[Rule34PostData]:
        async with aiohttp.ClientSession() as session:
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

                post_list.append(Rule34PostData(id, main_post, sample_post, preview_post))
            logging.debug(f"Creating {len(posts)} objects was done in {time.time() - start_time}s")
            return post_list
