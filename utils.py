import requests


def get_file_size(url, session: requests.Session):
    response = session.head(url, allow_redirects=True)
    if 'Content-Length' in response.headers:
        size = int(response.headers['Content-Length'])
        return size
    else:
        return None


def get_file_type(url):
    file_extension = url.split('.')[-1].lower()
    if file_extension in ['jpg', 'jpeg', 'png']:
        return 'photo'
    elif file_extension in ['mp4', 'avi', 'mov']:
        return 'video'
    elif file_extension == '.gif':
        return 'animation'
    else:
        return None
