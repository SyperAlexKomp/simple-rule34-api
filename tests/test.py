from SimpleRule34.src.SimpleRule34.aio.ARule34 import Rule34Api
from SimpleRule34.src.SimpleRule34 import Rule34Api
import asyncio


async def main1():

    r = Rule34Api()
    print("=====ALL 10=====")
    lis = await r.get_post_list(tags='', limit=10)

    for x in lis:
        print(x)

    print("=====FIRST 5=====")
    lis = await r.get_post_list(tags='brawl_stars', limit=5)

    for x in lis:
        print(x)

    print("=====SECOND 5=====")
    lis = await r.get_post_list(tags='brawl_stars', limit=5, page_id=1)

    for x in lis:
        print(x)

    print("=====EDITED=====")
    post_list_ = await r.get_post_list(tags='brawl_stars', limit=100, page_id=0,
                                            forbidden_tags=['male'])

    chunk_size = 5
    for i in range(0, len(post_list_), chunk_size):
        chunk = post_list_[i:i + chunk_size]
        print(f"=====CHUNK {i}=====")
        for x in chunk:
            print(x)
    i = 4
    chunk = post_list_[i:i + chunk_size]
    print(f"=====CHUNK {i}=====")
    for x in chunk:
        print(x)


    print("=====TEST=====")
    original_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]

    chunk_size = 5
    for i in range(0, len(original_list), chunk_size):
        print(i)
        chunk = original_list[i:i + chunk_size]
        print(chunk)

    return


async def main():
    r = Rule34Api()
    p = r.get_post(213)
    print(p)

if __name__ == '__main__':
    asyncio.run(main())