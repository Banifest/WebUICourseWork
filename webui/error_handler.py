from django.contrib import messages
from django.http import HttpRequest
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin

# Mixin for compatibility with Django <1.10
from webui.exceptions import AuthException, ErrorStatus


class HandleExceptionMiddleware(MiddlewareMixin):
    def process_exception(self, request: HttpRequest, exception):
        if isinstance(exception, AuthException):
            response = redirect('/auth', permanent=True)
            response.delete_cookie('login')
            response.delete_cookie('sessionid')
            response.delete_cookie('csrftoken')
            return response
        elif isinstance(exception, ErrorStatus):
            response = redirect('{0}?status_code={1}'.format(request.path,  exception.detail['detail']),
                                permanent=True)
            return response