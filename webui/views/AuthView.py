import requests
from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.views.generic import TemplateView

from webui.CustomTemplateView import CustomTemplateView
from webui.exceptions import ErrorStatus, AuthException
from webui.req import BASE_API_URL


class AuthView(CustomTemplateView):
    template_name = 'auth.html'

    def get(self, request, *args, **kwargs):
        if 'login' in request.COOKIES:
            return redirect('main.html', permanent=True)
        return self.re_render_to_response(context={}, request=request)

    def post(self, request: HttpRequest) -> HttpResponse:
        res = requests.request(
                'POST',
                BASE_API_URL + '/users/login/',
                json={
                    'username': request.POST['login'],
                    'password': request.POST['password']
                },
        )
        if res.status_code == 201:
            response = redirect('main.html', permanent=True, )
            response.set_cookie('login', request.POST['login'])
            response.set_cookie('csrftoken', res.cookies.get('csrftoken'))
            response.set_cookie('sessionid', res.cookies.get('sessionid'))
            return response
        else:
            raise ErrorStatus(status_code=res.status_code, status=res.json())
