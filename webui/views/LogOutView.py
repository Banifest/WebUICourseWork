from django.http import HttpResponse, HttpRequest
from django.shortcuts import redirect
from django.views.generic import TemplateView

from webui.exceptions import AuthException


class LogOutView(TemplateView):
    template_name = 'logout.html'

    def get(self, request, *args, **kwargs):
        response = redirect('auth.html', permanent=True)
        response.delete_cookie('login')
        response.delete_cookie('sessionid')
        response.delete_cookie('csrftoken')
        return response

    def post(self, request: HttpRequest) -> HttpResponse:
        response = redirect('auth.html', permanent=True)
        response.delete_cookie('login')
        response.delete_cookie('sessionid')
        response.delete_cookie('csrftoken')
        return response
