import requests
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.views.generic import TemplateView


class AuthView(TemplateView):
    template_name = 'auth.html'

    def get(self, request, *args, **kwargs):
        return self.render_to_response(context={})

    def post(self, request: HttpRequest) -> HttpResponse:
        res = requests.request(
                'POST',
                'http://127.0.0.1:8000/api/users/login/',
                json={
                    'username': request.POST['login'],
                    'password': request.POST['password']
                },
            )
        if res.status_code == 201:
            response = redirect('/main/', permanent=True,)
            response.set_cookie('login', request.POST['login'])
            response.set_cookie('csrftoken', res.cookies.get('csrftoken'))
            response.set_cookie('sessionid', res.cookies.get('sessionid'))
            return response
        else:
            return self.render_to_response(context={'error': 'No possible auth'})
