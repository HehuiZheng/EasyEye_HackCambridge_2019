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
    alert.alert_blur_sight = alert_blur_sight
    alert.alert_wrong_direction = alert_wrong_direction
    alert.save()


def get_evaluation_data(timespan=5*60):
    end_time = datetime.now(timezone.utc)
    records = SecondData.objects.filter(start_time__gte=end_time-timedelta(seconds=timespan)).order_by('start_time')
    print(records)
    data = {
        'timestamp':[],
        'data':[],
    }
    for record in records:
        data['timestamp'].append(record.start_time.strftime("%Y-%m-%d %H:%M:%S.%f"))