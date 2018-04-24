import requests
from django.contrib.auth import login, authenticate
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic import TemplateView
from jinja2 import Template

from webui.req import BASE_API_URL


class AuthView(TemplateView):
    template_name = 'auth.html'

    def get(self, request, *args, **kwargs):
        return self.render_to_response(context={})

    def post(self, request: HttpRequest) -> HttpResponse:
        user = authenticate(username=request.POST['login'], password=request.POST['password'])
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/main/', permanent=True)
            else:
                return self.render_to_response(context={'error': 'No possible auth'})
        else:
            return self.render_to_response(context={'error': 'No possible auth'})


class LogOut(TemplateView):
    template_name = 'auth.html'


class IndexView(TemplateView):
    template_name = 'index.html'

    def get(self, request: HttpRequest, **kwargs) -> HttpResponse:
        if request.user.is_active:
            return redirect('/main/', permanent=True)
        else:
            return redirect('/auth/', permanent=True)


class RegView(TemplateView):
    template_name = 'reg.html'

    def post(self, request: HttpRequest) -> HttpResponse:

        return self.render_to_response(context={})


class MainView(TemplateView):
    template_name = 'main.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_active:
            user = requests.request(
                    'GET',
                    'http://127.0.0.1:8000/api/users/1/',
                    cookies=request.COOKIES,
            ).json()

            references = requests.request(
                    'GET',
                    'http://127.0.0.1:8000/api/references/',
                    cookies=request.COOKIES,
            ).json()

            return self.render_to_response({})
            # user = User.objects.filter(id=request.user.id)
            # references = Reference.objects.filter(user=user[0]).all()
            # return self.render_to_response({'references': references, user: user, })
        else:
            return redirect('/main/', permanent=True)
