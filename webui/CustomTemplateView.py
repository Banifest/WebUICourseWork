from django.http import HttpRequest
from django.views.generic import TemplateView


class CustomTemplateView(TemplateView):
    def re_render_to_response(self, context, request: HttpRequest):
        if 'status_code' in request.GET:
            context['error'] = request.GET['status_code']
        return self.render_to_response(context=context)
