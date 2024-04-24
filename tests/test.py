from SimpleRule34.src.SimpleRule34.Rule34 import Rule34Api
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

    return


async def main():
    r = Rule34Api()
    p = await r.get_post_list(limit=10)
    print(p)

if __name__ == '__main__':
    asyncio.run(main())