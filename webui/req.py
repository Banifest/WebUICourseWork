BASE_API_URL = 'http://127.0.0.1:8000/api'

def get_url(url: str, user: str=None):
    return '{0}/{1}/{2}/'.format(BASE_API_URL, url, user) \
        if user else '{0}/{1}/'.format(BASE_API_URL, url)