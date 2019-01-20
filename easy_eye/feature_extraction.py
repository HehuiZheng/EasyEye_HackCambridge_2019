"""
Extract user's eyes' feature realtime
"""
from imutils import face_utils
import numpy as np
import imutils
from imutils.video import WebcamVideoStream
import dlib
import cv2
import time
import urllib
import json
from datetime import datetime

import feature_extractor

def upload_data(data):
    s = time.clock()
    url = "https://zhilingmail.pythonanywhere.com/api/upload_data"
    data = json.dumps(data)
    data = data.encode("utf-8")
    req = urllib.request.Request(url, data)
    resp = urllib.request.urlopen(req)
    print(resp.read())
    print(time.clock()-s)

if __name__ == "__main__":
    # Initiate face detection module
    detector = dlib.get_frontal_face_detector()

    # Initiate facial landmark detector
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

    # Initiate feature extractor
    fe = feature_extractor.feature_extractor()

    # Fetch left right eye id range
    left_eye_start_id, left_eye_end_id = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
    right_eye_start_id, right_eye_end_id = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

    # Open the camera
    try:
        stream = WebcamVideoStream(0).start()
    except:
        # Check if camera opened successfully
        print("Fail to access camera")
        raise

    # Init FPS counter
    start = time.clock()
    counter = 0
    outputs = []

    while True:
        # (Re)Init output data variable
        output = {}

        # Display fps and upload data
        counter += 1
        if time.clock() - start >= 1:
            # upload data
            try:
                upload_data(outputs)
            except:
                pass
            print(outputs)
            outputs = []

            # print fps
            print("FPS: ", counter)
            start = time.clock()
            counter = 0

        # Capture frame-by-frame
        frame = stream.read()

        # Resize the frame
        frame = imutils.resize(frame, width=500)

        # Gray scale the frame
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the grayscale image
        rects = detector(gray, 1)

        # Make sure no second face is detected or no face is detected
        if len(rects) >= 2 or len(rects) == 0:
            # if no proper detection of eyes is made, update a empty eyes to feature_extractor
            fe.update([], None)
        else:
            # determine the facial landmarks for the face region, then
            # convert the facial landmark (x, y)-coordinates to a NumPy
            # array
            shape = predictor(gray, rects[0])
            shape = face_utils.shape_to_np(shape)

            # find points for left and right eye
            left_eye = shape[left_eye_start_id:left_eye_end_id]
            right_eye = shape[right_eye_start_id:right_eye_end_id]

            # get eye aspect ratio and print it
            # left_ear = eye_aspect_ratio(left_eye)
            # right_ear = eye_aspect_ratio(right_eye)
            # avg_ear = (left_ear + right_ear) / 2
            # cv2.putText(frame, "ear: " + str(avg_ear), (0, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # update the eyes to feature_extractor
            fe.update([left_eye, right_eye], gray)

            # plot the two eyes
            for (x, y) in left_eye:
                cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)
            for (x, y) in right_eye:
                cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)

            # do blink detection
            is_blink = fe.is_blink()
            if is_blink == -1 or is_blink == 1:
                cv2.putText(frame, "Blink: "+str(is_blink), (left_eye[0][0], left_eye[0][1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    # print(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f'), "blink")

            # do deviated sight measure
            deviation_ratio = fe.deviated_sight(shape)
            # cv2.putText(frame, "Deviation: " + str(deviation_ratio), (right_eye[0][0], right_eye[0][1]+10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # do squint detection
            ear = np.median(fe.ears)
            # cv2.putText(frame, "Ear: " + str(ear), (right_eye[0][0], right_eye[0][1] + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # pack data
            if is_blink != -1:
                output["time"] = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')
                output["blink"] = is_blink
                output["deviation"] = deviation_ratio
                output["squint"] = ear
                outputs.append(output)

        # Display camera captured video
        cv2.imshow('Frame', frame)

        # Quit video when q is pressed
        key = cv2.waitKey(1)
        if key == ord('q'):
            break