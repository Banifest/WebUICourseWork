from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'index.html'

    def get(self, request: HttpRequest, **kwargs) -> HttpResponse:
        if request.user:
            return redirect('/main/', permanent=True)
        else:
            return redirect('/auth/', permanent=True)
