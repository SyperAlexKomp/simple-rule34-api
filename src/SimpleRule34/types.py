import os
import typing
import aiofiles
import aiohttp

from aiofiles import os as aos
from pydantic import BaseModel

from .exceptions import ApiException
from .utils import get_file_type


class File(BaseModel):
    url: str
    type: str = None

    def __init__(self, /, **data: typing.Any) -> None:
        super().__init__(**data)

        self.type = get_file_type(self.url)

    async def download(self, path: str = r'./rule34_download') -> str:
        try:
            await aos.mkdir(path)
        except:
            pass

        async with aiohttp.ClientSession() as session:
            async with session.get(self.url) as response:
                if response.status != 200:
                    raise ApiException(f"Api returned status code {response.status} with message"
                                       f" {await response.text()}")

                file_name = os.path.basename(self.url)
                save_path = os.path.join(path, file_name)

                async with aiofiles.open(save_path, 'wb') as file:
                    await file.write(await response.read())

                return save_path


class Post(BaseModel):
    directory: int
    hash: str
    width: int
    height: int
    id: int
    change: int
    owner: str
    parent_id: int
    rating: str
    sample: bool
    score: int
    tags: list
    source: str
    status: str
    has_notes: bool
    comment_count: int

    main: File
    preview: File
