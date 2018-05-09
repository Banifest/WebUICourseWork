from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.views.generic import TemplateView

from webui.CustomTemplateView import CustomTemplateView
from webui.req import do_request


class RegView(CustomTemplateView):
    template_name = 'reg.html'

    def get(self, request, *args, **kwargs):
        if 'login' in request.POST:
            return redirect('MainView', permanent=True)
        return self.render_to_response(context={})

    def post(self, request: HttpRequest) -> HttpResponse:
        user = do_request(
                method='POST',
                request=request,
                data={
                    'username': request.POST['username'],
                    'password': request.POST['password'],
                    'email': request.POST['email'],
                    'firstname': request.POST['firstName'],
                    'lastname': request.POST['lastName'],
                },
                auth=False,
        )
        return self.re_render_to_response(context={}, request=request)