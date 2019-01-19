import json
from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse

# Create your views here.


class GetAlertView(TemplateView):
    # API call processing
    template_name = 'live_search/index.html'

    def get(self, request, *args, **kwargs):
        #received_json_data = json.loads(request.body)

        data = {
            'msg':'Success',
            #'data':received_json_data,
        }

        return JsonResponse({
            'data': data,
        })