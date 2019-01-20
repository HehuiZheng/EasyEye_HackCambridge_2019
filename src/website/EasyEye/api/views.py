import json
import pytz
import time
from datetime import datetime, timedelta, timezone
from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse
from api.models import SecondData, Alert
from api.evaluation import evaluation

# Create your views here.

#for i in range(10):
#    evaluation()
#    time.sleep(1)


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
                    'timestamp': datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S.%f')
                })
            else:
                alert = alerts[0]
            alert_message = []
            if alert.alert_blink_slow:
                alert_message.append('blink_too_slow')
            if alert.alert_wrong_direction:
                alert_message.append('wrong_direction')
            if alert.alert_blur_sight:
                alert_message.append('blur_sight')
            if alert.alert_usage_overtime:
                alert_message.append('usage_overtime')
            return JsonResponse({
                'msg': 'Return Successfully',
                'alert': alert_message,
                'timestamp': alert.start_time.strftime('%Y-%m-%d %H:%M:%S.%f'),
            })
        except:
            return JsonResponse({
                'msg': 'Fail',
            })

class DataUploadView(TemplateView):
    # API call processing
    '''
    [{"deviation": 0.7222222222222222,
    "squint": 0.26785714285714285,
    "blink": 0,
     "time": "2019-01-20 03:46:40.621979"},
     '''
    def post(self, request, *args, **kwargs):

        try:
            # print('processing...')
            received_json_data = json.loads(request.body.decode('utf-8'))

            for record in received_json_data:
                time1 = time.time()
                new_record = SecondData()
                start_time = datetime.strptime(record['time'], "%Y-%m-%d %H:%M:%S.%f")
                start_time = pytz.timezone('UTC').localize(start_time)
                # print(start_time)
                new_record.start_time = start_time
                new_record.blink = record['blink']
                new_record.direction = record['deviation']
                new_record.squint = record['squint']
                time2 = time.time()
                if SecondData.objects.filter(start_time__gt=datetime.utcnow() - timedelta(minutes=1)).count() == 0:
                    new_record.start_point = True
                time3 = time.time()
                #print(new_record)
                new_record.save()
                time4 = time.time()
                print(time2-time1, time3-time2, time4-time3)

            return JsonResponse({
                'msg': 'Success',
                'data': received_json_data,
            })
        except:
            return JsonResponse({
                'msg': 'Fail',
            })


class IndexView(TemplateView):
    template_name = 'api/index.html'
    def get(self, request, *args, **kwargs):
        params={}
        with open('api/data_output.txt') as f:
            data = json.load(f)
            print(data)
            data['average_blink'] = int(data['average_blink'])

            params = data

        return self.render_to_response(params)