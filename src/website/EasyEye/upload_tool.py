
import django
import os
import time
# Use pymysql lib instead of mysqlclient
# remove when needed
import pymysql
pymysql.install_as_MySQLdb()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "EasyEye.settings")
django.setup()

from django.conf import settings
from api.models import SecondData, Alert
from datetime import datetime, timedelta
import pytz


if __name__ == "__main__":
    received_json_data = []
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
        # print(new_record)
        new_record.save()
        time4 = time.time()
        print(time2 - time1, time3 - time2, time4 - time3)