import json

import requests
from django.contrib.auth import login, authenticate
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from jinja2 import Template

from webui.exceptions import AuthException
from webui.req import BASE_API_URL, get_url


class AuthView(TemplateView):
    template_name = 'auth.html'

    def get(self, request, *args, **kwargs):
        return self.render_to_response(context={})

    def post(self, request: HttpRequest) -> HttpResponse:
        res = requests.request(
                'POST',
                'http://127.0.0.1:8000/api/users/{0}/login/'.format(request.POST['login']),
                json={'password': request.POST['password']},
            )
        if res.status_code == 201:
            response = redirect('/main/', permanent=True,)
            response.set_cookie('login', request.POST['login'])
            return response
        else:
            return self.render_to_response(context={'error': 'No possible auth'})


class LogOut(TemplateView):
    template_name = 'auth.html'


class IndexView(TemplateView):
    template_name = 'index.html'

    def get(self, request: HttpRequest, **kwargs) -> HttpResponse:
        if request.user:
            return redirect('/main/', permanent=True)
        else:
            return redirect('/auth/', permanent=True)


class RegView(TemplateView):
    template_name = 'reg.html'

    def post(self, request: HttpRequest) -> HttpResponse:

        return self.render_to_response(context={})


#@method_decorator(csrf_exempt, name='dispatch')
class MainView(TemplateView):
    template_name = 'main.html'

    def get(self, request, *args, **kwargs):
        user = requests.request(
                'GET',
                get_url('users', 'banifest'),
                cookies=request.COOKIES,
        ).json()

        references = requests.request(
                'GET',
                get_url('users', 'banifest') + 'references/',
                cookies=request.COOKIES,
        ).json()

        groups = requests.request(
                'GET',
                get_url('users', 'banifest') + 'groups/',
                cookies=request.COOKIES,
        ).json()

        groups_dict = {}
        for x in groups:
            x['refs'] = []
            groups_dict[x['id']] = x

        for x in references:
            groups_dict[x['group']]['refs'].append(x)

        return self.render_to_response(context={
            'user_info': user,
            'groups': groups_dict
        })

    #@csrf_exempt
    def post(self, request, *args, **kwargs):
        if 'change-color' in request.POST:
            requests.request(
                    'PATCH',
                    get_url('users', 'banifest') + 'groups/{0}/'.format(request.POST['group-id']),
                    json={"color": request.POST['color'],},
                    cookies=request.COOKIES,
                    headers={'X-CSRFTOKEN': request.COOKIES['csrftoken']},
            )
        elif 'delete-ref' in request.POST:
            requests.request(
                    'DELETE',
                    get_url('users', 'banifest') + 'references/{0}/'.format(request.POST['ref-id']),
                    cookies=request.COOKIES,
                    headers={'X-CSRFTOKEN': request.COOKIES['csrftoken']},
            )
        elif 'add-ref' in request.POST:
            a = requests.request(
                    'POST',
                    get_url('users', 'banifest') + 'references/',
                    json={'name': request.POST['name'], 'ref_url': request.POST['url'], 'group': request.POST['group-id']},
                    cookies=request.COOKIES,
                    headers={'X-CSRFTOKEN': request.COOKIES['csrftoken']},
            )
        elif 'add-group' in request.POST:
            a = requests.request(
                    'POST',
                    get_url('users', 'banifest') + 'group/',
                    json={'name': request.POST['name'], 'ref_url': request.POST['url'], 'group': request.POST['group-id']},
                    cookies=request.COOKIES,
                    headers={'X-CSRFTOKEN': request.COOKIES['csrftoken']},
            )

        return self.get(request, *args, **kwargs)
