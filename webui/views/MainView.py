# @method_decorator(csrf_exempt, name='dispatch')
import requests
from django.views.generic import TemplateView

from webui.CustomTemplateView import CustomTemplateView
from webui.req import do_request, get_all_items


class MainView(CustomTemplateView):
    template_name = 'main.html'

    def get(self, request, *args, **kwargs):
        user = do_request(
                method='GET',
                request=request,
        ).json()

        references = get_all_items(name='references', request=request)
        groups = get_all_items(name='groups', request=request)

        groups_dict = {}
        for x in groups:
            x['refs'] = []
            groups_dict[x['id']] = x

        for x in references:
            groups_dict[x['group']]['refs'].append(x)

        return self.re_render_to_response(context={
            'user_info': user,
            'groups': groups_dict
        },
        request=request)

    def post(self, request, *args, **kwargs):
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

        return self.get(request, *args, **kwargs)
