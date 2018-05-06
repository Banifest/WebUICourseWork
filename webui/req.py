import requests
from django.http import HttpRequest

from webui.exceptions import AuthException

BASE_API_URL = 'http://127.0.0.1:8000/api'


def get_url(url: str, user: str, str=None):
    return '{0}/{1}/{2}/'.format(BASE_API_URL, url, user) \
        if user else '{0}/{1}/'.format(BASE_API_URL, url)


def do_request(method: str, url: str = '', request: HttpRequest = None, obj: str = None, data: dict = None,
               query: dict = None) \
        -> requests.Response:
    if 'login' not in request.COOKIES:
        raise AuthException()

    request_url = '{0}/users/{1}/{2}/'.format(BASE_API_URL, request.COOKIES['login'], url)
    if request_url[-2:] == '//':
        request_url = request_url[:-1]

    if obj is not None:
        request_url += obj + '/'

    if query is not None:
        request_url += '?'
        for x in query.items():
            request_url += x[0] + '=' + str(x[1]) + '&'

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


def get_all_items(name: str, request: HttpRequest) -> list:
    answ = []

    page = 1
    res = do_request(
            method='GET',
            url=name,
            request=request,
            query={
                'page': page,
                'limit': 100,
            }
    ).json()
    while res['next'] is not None:
        page += 1
        answ += res['results']
        res = do_request(
                method='GET',
                url=name,
                request=request,
                query={
                    'page': page,
                    'limit': 100,
                }
        ).json()
    else:
        answ = res['results']
    return answ
