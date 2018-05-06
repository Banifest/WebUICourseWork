from django.http import HttpResponse, HttpRequest
from django.views.generic import TemplateView

from webui.exceptions import AuthException


class LogOutView(TemplateView):
    template_name = 'auth.html'

    def post(self, request: HttpRequest) -> HttpResponse:
        raise AuthException()
