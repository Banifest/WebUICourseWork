import requests
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.views.generic import TemplateView

from webui.req import do_request


class SettingView(TemplateView):
    template_name = 'setting.html'

    def get(self, request, *args, **kwargs):
        if 'login' not in request.COOKIES:
            return redirect('auth.html')

        res = do_request(
                method='GET',
                request=request,
        ).json()

        return self.render_to_response(context={'user_info': res})

    def post(self, request: HttpRequest) -> HttpResponse:
        if 'change-color' in request.POST:
            do_request(
                    'PATCH',
                    'groups',
                    request,
                    obj=request.POST['group-id'],
                    data={"color": request.POST['color'], },
            )
        elif 'delete-ref' in request.POST:
            do_request(
                    'DELETE',
                    'references',
                    request,
                    obj=request.POST['ref-id'],
            )
        elif 'add-ref' in request.POST:
            do_request(
                    'POST',
                    'references',
                    request,
                    data={
                        'name': request.POST['name'],
                        'ref_url': request.POST['url'],
                        'group': request.POST['group-id']
                    },
            )
        elif 'add-group' in request.POST:
            do_request(
                    'POST',
                    'groups',
                    request,
                    data={
                        'name': request.POST['name'],
                        'color': request.POST['color'],
                        'priority': request.POST['priority']
                    },
            )
        elif 'delete-group' in request.POST:
            do_request(
                    'DELETE',
                    'groups',
                    request,
                    obj=request.POST['group-id'],
            )
        elif 'change-ref' in request.POST:
            do_request(
                    method='PATCH',
                    url='references',
                    request=request,
                    obj=request.POST['ref-id'],
                    data={
                        'ref_url': request.POST['url'],
                        'name': request.POST['name'],
                    }
            )

        return self.get(request)
