from setuptools import setup, find_packages

setup(
    name='SimpleRule34',
    version='0.1',
    description='Simple api wrapper of rule34.xxx for python with asynchronous support',
    packages=find_packages(),
    install_requires=[
        'aiohttp==3.8.4',
        'aiosignal==1.3.1',
        'async-timeout==4.0.2',
        'attrs==23.1.0',
        'certifi==2023.5.7',
        'charset-normalizer==3.2.0',
        'docopt==0.6.2',
        'frozenlist==1.4.0',
        'idna==3.4',
        'multidict==6.0.4',
        'pipreqs==0.4.13',
        'requests==2.31.0',
        'urllib3==2.0.3',
        'yarg==0.1.9',
        'yarl==1.9.2',
    ],
    url='https://github.com/Loshok229/rule34-simple-api'
)