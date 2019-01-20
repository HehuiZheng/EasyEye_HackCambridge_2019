from datetime import datetime, timedelta, timezone
from api.models import SecondData, Alert

def create_alert(alert_wrong_direction=0,
                 alert_blink_slow=0,
                 alert_blur_sight=0,
                 alert_usage_overtime=0):
    alert = Alert()
    alert.start_time = datetime.now(timezone.utc)
    alert.alert_usage_overtime=alert_usage_overtime
    alert.alert_blink_slow = alert_blink_slow
    alert.alert_blur_sight = 0#alert_blur_sight
    alert.alert_wrong_direction = alert_wrong_direction
    alert.save()
    print(alert)


def get_evaluation_data(timespan=5*60):
    end_time = datetime.now(timezone.utc)
    # end_time = SecondData.objects.all().order_by('-start_time')[1000].start_time
    records = SecondData.objects.filter(start_time__gte=end_time-timedelta(seconds=timespan),
                                        start_time__lt=end_time).order_by('start_time')
    data = {
        'timestamp':[],
        'blink':[],
        'deviation':[],
        'squint':[],
    }
    for record in records:
        data['timestamp'].append(record.start_time)
        data['blink'].append(record.blink)
        data['deviation'].append(record.direction)
        data['squint'].append(record.squint)
    start_records = SecondData.objects.filter(start_point=True).order_by('-start_time')
    if start_records.count() >= 1:
        data['start_point'] = start_records[0].start_time

    return data

def get_all_data():
    records = SecondData.objects.filter(start_time__gte=end_time-timedelta(seconds=timespan)).order_by('start_time')
    print(records)
    data = {
        'timestamp':[],
        'blink':[],
        'deviation':[],
        'squint':[],
        'start_point':[]
    }
    for record in records:
        data['timestamp'].append(record.start_time)
        data['blink'].append(record.blink)
        data['deviation'].append(record.direction)
        data['squint'].append(record.squint)
        data['start_point'].append(record.start_point)

    return data