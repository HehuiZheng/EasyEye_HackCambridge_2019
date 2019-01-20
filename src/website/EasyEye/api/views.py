import json
import pytz
from datetime import datetime, timedelta
from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse
from api.models import SecondData, Alert

# Create your views here.


class GetAlertView(TemplateView):
    # API call processing

    def get(self, request, *args, **kwargs):
        #received_json_data = json.loads(request.body)
        try:
            alerts = Alert.objects.all().order_by('-start_time')
            if alerts.count() == 0:
                return JsonResponse({
                    'msg': 'Return Successfully',
                    'alert': [],
                })
            else:
                alert = alerts[0]
            return JsonResponse({
                'msg': 'Return Successfully',
                'alert': [
                    alert.alert_wrong_direction,
                    alert.alert_blink_slow,
                    alert.alert_blur_sight,
                    alert.alert_usage_overtime,
                          ],
                'timestamp': alert.start_time.strftime('%Y-%m-%d %H:%M:%S.%f'),
            })
        except:
            return JsonResponse({
                'msg': 'Fail',
            })

class DataUploadView(TemplateView):
    # API call processing
    '''
    '''
    def get(self, request, *args, **kwargs):

        try:
            received_json_data = json.loads(request.body.decode("utf-8"))
            print(received_json_data)
            '''
            for i in range(len(timestamps)):
            data = []
            new_record = SecondData()
            start_time = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")
            start_time = pytz.timezone('UTC').localize(start_time)
            #print(start_time)
            new_record.start_time = start_time
            new_record.blink = data[0]
            new_record.direction = data[1]
            new_record.squint = data[2]
            if SecondData.objects.filter(start_time__gt=datetime.utcnow() - timedelta(minutes=1)).count() == 0:
                new_record.start_point = True
            print(new_record)
            new_record.save()
            '''
            return JsonResponse({
                'msg': 'Success',
                'data': received_json_data,
            })
        except:
            return JsonResponse({
                'msg': 'Fail',
            })



