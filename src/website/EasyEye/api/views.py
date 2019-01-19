from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse

# Create your views here.

class GetAlertView(TemplateView):
    # API call processing
    template_name = 'live_search/index.html'

    def get(self, request, *args, **kwargs):
        data = {}

        return JsonResponse({
            'data': data,
        })