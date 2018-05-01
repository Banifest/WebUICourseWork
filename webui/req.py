import requests
from django.http import HttpRequest

from webui.exceptions import AuthException

BASE_API_URL = 'http://127.0.0.1:8000/api'


def get_url(url: str, user: str, str=None):
    return '{0}/{1}/{2}/'.format(BASE_API_URL, url, user) \
        if user else '{0}/{1}/'.format(BASE_API_URL, url)


def do_request(method: str, url: str, request: HttpRequest, obj: str = None, data: dict = None) -> requests.Response:
    if 'login' not in request.COOKIES:
        raise AuthException()

    request_url = '{0}/users/{1}/{2}/'.format(BASE_API_URL, request.COOKIES['login'], url)
    if obj is not None:
        request_url += obj + '/'

    res: requests.Response
    if data is not None:
        res = requests.request(
                method,
                request_url,
                cookies=request.COOKIES,
                json=data,
                headers={'X-CSRFTOKEN': request.COOKIES['csrftoken']},
        )
    else:
        res = requests.request(
                method,
                request_url,
                cookies=request.COOKIES,
                headers={'X-CSRFTOKEN': request.COOKIES['csrftoken']},
        )

    if res.status_code == 403:
        raise AuthException()

    return res
