from django.http import HttpRequest, HttpResponse
from django.views.generic import TemplateView

from webui.req import do_request


class RegView(TemplateView):
    template_name = 'reg.html'

    def post(self, request: HttpRequest) -> HttpResponse:
        user = do_request(
                'POST',
                'users',
                request,
                data={
                    'username': request.POST['username'],
                    'password': request.POST['password'],
                    'firstname': request.POST['firstname'],
                    'lastname': request.POST['lastname'],
                }
        )
        return self.render_to_response(context={})