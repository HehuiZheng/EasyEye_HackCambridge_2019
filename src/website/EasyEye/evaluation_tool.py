
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
from api.evaluation import evaluation



if __name__ == "__main__":
    print('running test')
    while True:
        evaluation()
        time.sleep(1)
