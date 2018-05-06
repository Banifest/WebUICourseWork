# @method_decorator(csrf_exempt, name='dispatch')
import requests
from django.views.generic import TemplateView

from webui.req import do_request, get_url, get_all_items


class MainView(TemplateView):
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

        return self.render_to_response(context={
            'user_info': user,
            'groups': groups_dict
        })

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

        return self.get(request, *args, **kwargs)
