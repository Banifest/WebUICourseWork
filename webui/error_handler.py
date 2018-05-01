from django.contrib import messages
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin

# Mixin for compatibility with Django <1.10
from webui.exceptions import AuthException


class HandleExceptionMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        if isinstance(exception, AuthException):
            response = redirect('/auth', permanent=True)
            response.delete_cookie('login')
            response.delete_cookie('sessionid')
            response.delete_cookie('csrftoken')
            return response