import requests
from django.http import HttpRequest

from webui.exceptions import AuthException, ErrorStatus

# BASE_API_URL = 'http://127.0.0.1:8000/api'
BASE_API_URL = 'https://pscaserv.herokuapp.com/api'


def do_request(method: str, url: str = '', request: HttpRequest = None, obj: str = None, data: dict = None,
               query: dict = None, auth=True) \
        -> requests.Response:
    request_url: str
    if auth and 'login' not in request.COOKIES:
        raise AuthException()

    if auth:
        request_url = '{0}/users/{1}/{2}/'.format(BASE_API_URL, request.COOKIES['login'], url)
    else:
        request_url = '{0}/users/{1}/'.format(BASE_API_URL, url)

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

    if res.status_code // 100 in {4, 5}:
        try:
            res.json()
        except:
            raise ErrorStatus(res.status_code, {'detail': 'Unknown error'})
        else:
            if 'detail' in res.json() and res.json()['detail'] == 'Authentication credentials were not provided.':
                raise AuthException()
            raise ErrorStatus(res.status_code, res.json())

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
