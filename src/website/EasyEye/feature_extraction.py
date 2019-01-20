"""
Extract user's eyes' feature realtime
"""

# suppress warning
import warnings
warnings.filterwarnings("ignore")

# set up sql interface
import django
import os
import pymysql
pymysql.install_as_MySQLdb()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "EasyEye.settings")
django.setup()
from django.conf import settings
from api.models import SecondData, Alert
from datetime import datetime, timedelta
import pytz

# set up CV modules
from imutils import face_utils
import numpy as np
import imutils
from imutils.video import WebcamVideoStream
import dlib
import cv2
import time
import urllib
import json
from multiprocessing import Process, Queue, Pool
from datetime import datetime

from feature_extractor import feature_extractor, fetch_data

def open_response(req):
    resp = urllib.request.urlopen(req).read()
    print(resp.read())

def upload_data_sql(data):
    for record in data:
        new_record = SecondData()
        start_time = datetime.strptime(record['time'], "%Y-%m-%d %H:%M:%S.%f")
        start_time = pytz.timezone('UTC').localize(start_time)
        new_record.start_time = start_time
        new_record.blink = record['blink']
        new_record.direction = record['deviation']
        new_record.squint = record['squint']
        if SecondData.objects.filter(start_time__gt=datetime.utcnow() - timedelta(minutes=1)).count() == 0:
            new_record.start_point = True
        new_record.save()
    return None

if __name__ == "__main__":
    # Initiate face detection module
    detector = dlib.get_frontal_face_detector()

    # Initiate facial landmark detector
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

    # Initiate feature extractor
    fe = feature_extractor()

    # # Fetch left right eye id range
    # left_eye_start_id, left_eye_end_id = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
    # right_eye_start_id, right_eye_end_id = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

    # Open the camera
    try:
        stream = WebcamVideoStream(0).start()
    except:
        # Check if camera opened successfully
        print("Fail to access camera")
        raise

    q = Queue()

    outputs = fetch_data(1, stream, detector, predictor, fe)
    while True:
        tmp = time.time()

        # p = Process(target=upload_data_sql, args=(outputs, ))
        # p.start()
        # result = fetch_data(1, stream, detector, predictor, fe)
        # p.join()
        # outputs = result

        # upload_data_sql(outputs)
        outputs = fetch_data(1, stream, detector, predictor, fe)
        print("complete cycle: ", time.time()-tmp)