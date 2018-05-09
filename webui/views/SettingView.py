import requests
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from webui.CustomTemplateView import CustomTemplateView
from webui.req import do_request


class SettingView(CustomTemplateView):
    template_name = 'setting.html'

    def get(self, request, *args, **kwargs):
        if 'login' not in request.COOKIES:
            return redirect('auth.html')

        res = do_request(
                method='GET',
                request=request,
        ).json()

        return self.re_render_to_response(context={'user_info': res}, request=request)

    def post(self, request: HttpRequest) -> HttpResponse:
        if 'change-pass' in request.POST:
            if request.POST['password1'] == request.POST['password2']:
                res = do_request(
                        method='PATCH',
                        request=request,
                        data={
                            "password": request.POST['password1'],
                        },
                        auth=False,
                )
        elif 'change-user' in request.POST:
            do_request(
                    method='PATCH',
                    request=request,
                    data={
                        'first_name': request.POST['first-name'],
                        'last_name': request.POST['last-name'],
                        'email': request.POST['email'],
                    }
            )
        return self.get(request)
