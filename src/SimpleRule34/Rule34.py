import random
import time
import typing

import requests
import datetime
import logging
import xml.etree.ElementTree as ET

from .exceptions import *
from .types import Rule34MainPost, Rule34PostData, Rule34SamplePost, Rule34PreviewPost


class Rule34Api:
    """
    Sync main api class

    """

    def __init__(self):
        self.s = requests.Session()

    def get_post_count(self, tags: str = '') -> int:
        """
        This function will search amount of posts with your tags from rule34.xxx

        :param tags: Tags in format 'tag1 tag2 ...'. Base ''
        :type tags: str

        :return: Amount of posts with current tags
        :rtype: int
        """


        r = self.s.get(f'https://api.rule34.xxx/index.php?'
                       f'page=dapi&s=post&q=index&tags={tags}')

        xml_root = ET.fromstring(r.text)

        return int(xml_root.get('count'))

    def get_post(self, id: int) -> typing.Optional[Rule34PostData]:
        """
        This function will search post with your id from rule34.xxx

        :param id: id of post
        :type id: int

        :return: On success, returns Rule34PostData object
        :rtype: :obj: 'typing.Optional[Rule34PostData]'
        """

        r = self.s.get(f'https://api.rule34.xxx/index.php?'
                       f'page=dapi&s=post&q=index&id={id}')

        try:
            xml_root = ET.fromstring(r.text)
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

        sample_post = Rule34SamplePost(sample_height, sample_width, sample_url, id, self.s)

        preview_height = int(post_element.get('preview_height'))
        preview_width = int(post_element.get('preview_width'))
        preview_url = post_element.get('preview_url')

        preview_post = Rule34PreviewPost(preview_height, preview_width, preview_url, id, self.s)

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
                                   source, has_notes, has_comments, height, width, url, id, self.s)

        return Rule34PostData(id, main_post, sample_post, preview_post)

    def get_random_post(self, tags: str = '') -> typing.Optional[Rule34PostData]:
        """
        This function will search 1 random post with your tags from rule34.xxx

        :param tags: Tags in format 'tag1 tag2 ...' with which post will be searching. Base ''
        :type tags: str

        :return: On success, returns Rule34PostData object
        :rtype: :obj: 'typing.Optional[Rule34PostData]'
        """

        post_count = self.get_post_count(tags)

        page_count = post_count // 1000

        if page_count > 0:
            post_list = self.get_post_list(page_id=random.randint(0, page_count if page_count <= 200 else 200),
                                           tags=tags, limit=1000)

        else:
            post_list = self.get_post_list(tags=tags, limit=1000)

        return post_list[random.randint(0, len(post_list) - 1)] if len(post_list) > 0 else None

    def get_random_posts(self, tags: str = '', count: int = 8) -> list[Rule34PostData]:
        """
        This function will search your amount of random posts with your tags from rule34.xxx

        :param tags: Tags in format 'tag1 tag2 ...' with which post will be searching. Base ''
        :type tags: str

        :param count: Amount of posts that will need to be founded. Base 8
        :type count: int

        :return: List with founded posts
        :rtype: :obj: 'list[Rule34PostData]'

        """

        st = time.time()

        request_count = 1

        post_list = []

        if count > 1000:
            request_count = count // 1000

        for pid in range(request_count + 1):
            post_list += self.get_post_list(tags=tags)

        getted = [post_list[random.randint(0, len(post_list) - 1)] if len(post_list) > 0 else None for x in
                  range(count)]

        logging.debug(f"{count} random posts where founded in {time.time() - st}")

        return getted

    def get_post_list(self, limit: int = 1000, page_id: int = 0, tags: str = '') -> list[Rule34PostData]:
        """
        This function will get list of posts with your tags on page

        :param limit: limit of posts in list. Base value is 1000
        :type limit: int

        :param page_id: number of page with posts. Base value is 0
        :type page_id: int

        :param tags: Tags in format 'tag1 tag2 ...' with which post will be searching. Base values is ''
        :type tags: str

        :return: :obj: 'list[Rule34PostData]'
        """

        if limit > 1000:
            raise ToBigRequestException(f"The max size of request is 1000 when you tried to request {limit}")

        start_time = time.time()

        r = self.s.get(f'https://api.rule34.xxx/index.php?'
                       f'page=dapi&s=post&q=index&limit={limit}&pid={page_id}&tags={tags}')

        logging.debug(f"Request with {limit}limit posts where done in {time.time() - start_time}s")

        xml_root = ET.fromstring(r.text)
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

            sample_post = Rule34SamplePost(sample_height, sample_width, sample_url, id, self.s)

            preview_height = int(post_element.get('preview_height'))
            preview_width = int(post_element.get('preview_width'))
            preview_url = post_element.get('preview_url')

            preview_post = Rule34PreviewPost(preview_height, preview_width, preview_url, id, self.s)

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
                                       source, has_notes, has_comments, height, width, url, id, self.s)

            post_list.append(Rule34PostData(id, main_post, sample_post, preview_post))
        logging.debug(f"Creating {len(posts)} objects where done in {time.time() - start_time}s")
        return post_list


if __name__ == '__main__':
    r34 = Rule34Api()

    for pd in r34.get_post_list(tags='marinette_cheng', limit=30):
        print(pd.main.download(path=r'C:\Users\alexk\PycharmProjects\Rule34Bot\test\data\marinette_cheng'))
