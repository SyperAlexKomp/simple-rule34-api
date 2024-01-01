import datetime
import requests
import os

from .utils import get_file_type, get_file_size


class Rule34Post:
    def __init__(self, height: int, width: int, url: str, id: int):
        self.path = r'./rule34_download'
        self.s = requests.Session()

        self.height = height
        self.width = width
        self.url = url
        self.id = id

        self.file_type = get_file_type(self.url)

    def __str__(self):
        return f"<Rule34Post(id={self.id}, height={self.height}, width={self.width}, url={self.url})>"

    def get_file_size(self):
        return get_file_size(self.url, self.s)

    def download(self, path = r'./rule34_download'):
        r = self.s.get(self.url)
        if r.status_code == 200:
            try:
                os.mkdir(self.path)
            except:
                pass

            file_name = os.path.basename(self.url)
            save_path = os.path.join(path, file_name)
            with open(save_path, 'wb') as file:
                file.write(r.content)

            return save_path
        else:
            pass

    def get_bytes(self):
        r = self.s.get(self.url)

        return r.content


class Rule34MainPost(Rule34Post):
    def __init__(self, score: int, rating: str, creator_id: int, tags: str, has_children: bool,
                 created_date: datetime.datetime, status: str, source: str, has_notes: bool, has_comments: bool,
                 height: int, width: int, url: str, id: int):
        super().__init__(height, width, url, id)
        self.score = score
        self.rating = rating
        self.creator_id = creator_id
        self.tags = tags.split(" ")
        self.has_children = has_children
        self.created_date = created_date
        self.status = status
        self.source = source
        self.has_notes = has_notes
        self.has_comments = has_comments

    def __str__(self):
        return f"<Rule34MainPost(id={self.id}, height={self.height}, width={self.width}, url={self.url}," \
               f" score={self.score}, rating={self.rating}, creator_id={self.creator_id}," \
               f" has_children={self.has_children}, has_notes={self.has_notes}, has_comments={self.has_comments}" \
               f" created_date={self.created_date}, status={self.status}, tags={self.tags})>"

    def format_tags(self, format: str = "#"):
        str_tags = (format + ' ').join(self.tags)
        return str_tags.split(" ")


class Rule34SamplePost(Rule34Post):
    def __str__(self):
        return f"<Rule34SamplePost(id={self.id}, height={self.height}, width={self.width}, url={self.url})>"


class Rule34PreviewPost(Rule34Post):
    def __str__(self):
        return f"<Rule34PreviewPost(id={self.id}, height={self.height}, width={self.width}, url={self.url})>"


class Rule34PostData:
    def __init__(self, id: int, main: Rule34MainPost, sample: Rule34SamplePost, preview: Rule34PreviewPost):
        self.id = id
        self.main = main
        self.sample = sample
        self.preview = preview

    def __str__(self):
        return f"<Rule34PostData(id={self.id}, main={str(self.main)}, sample={str(self.sample)}," \
               f" preview={str(self.preview)})>"