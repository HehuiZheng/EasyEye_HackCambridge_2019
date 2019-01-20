import numpy as np
import cv2
from scipy.spatial import distance as dist
# set up CV modules
from imutils import face_utils
import numpy as np
import imutils
import cv2
import time
from datetime import datetime

class feature_extractor:
    def __init__(self):
        self.miss_counter = 0
        self.ears = []
        self.eye_regions = []
        self.avg_diff = -1

    def point2line(self, p, p0, p1):
        return np.abs(np.cross(p0 - p, p1 - p)) / np.linalg.norm(p1 - p0)

    def get_avg_intensity(self, image):
        """
        get average intensity of an image
        :param image: an image
        :return: average intensity
        """
        mean = image.sum() / image.shape[0] / image.shape[1]
        threshold = image.copy()
        threshold[threshold<mean/2] = 0
        if np.count_nonzero(threshold) > 0:
            return threshold.sum() / np.count_nonzero(threshold)
        else:
            return 1e-5

    def eye_aspect_ratio(self, eye):
        """
        get eye aspect ratio for one input eye
        :param eye: list of 6 key points describing an eye
        :return: the eye aspect ratio
        """
        A = self.point2line(eye[1], eye[0], eye[3]) + self.point2line(eye[5], eye[0], eye[3])
        B = self.point2line(eye[2], eye[0], eye[3]) + self.point2line(eye[4], eye[0], eye[3])

        # compute the euclidean distance between the horizontal
        # eye landmark (x, y)-coordinates
        C = dist.euclidean(eye[0], eye[3])

        # compute the eye aspect ratio
        ear = (A + B) / (2.0 * C)

        # return the eye aspect ratio
        return ear

    def extract_eye_region(self, eye, image, expand_ratio=0.15, size=(30, 10)):
        """
        extract the image of eye
        :param eye: points of an eye
        :param image: the frame
        :param expand_ratio: expand the default bounding box
        :return: the region of the image of the eye
        """
        # get boundary of image
        min_x = min(eye, key=lambda x: x[0])[0]
        max_x = max(eye, key=lambda x: x[0])[0]
        min_y = min(eye, key=lambda x: x[1])[1]
        max_y = max(eye, key=lambda x: x[1])[1]

        # expend the eye by given ratio
        x_len = max_x - min_x
        y_len = max_y - min_y
        min_x = int(max((0, min_x - x_len * expand_ratio)))
        max_x = int(min((image.shape[1], max_x + x_len * expand_ratio)))
        min_y = int(max((0, min_y - y_len * expand_ratio)))
        max_y = int(min((image.shape[0], max_y + y_len * expand_ratio)))

        return cv2.resize(image[min_y:max_y, min_x:max_x], size)

    def update(self, eyes, image):
        """
        update eye points
        :param eyes: two list of 6 points describing eyes
        """
        if len(eyes) == 0:
            self.miss_counter += 1
            if self.miss_counter > 2:
                self.miss_counter = 0
                self.ears = []
                self.eye_regions = []
        else:
            # crop the image of eyes
            if len(self.eye_regions) == 5:
                self.eye_regions.pop(0)
            self.eye_regions.append(
                cv2.addWeighted(self.extract_eye_region(eyes[0], image), 0.5, self.extract_eye_region(eyes[1], image),
                                0.5, 0))

            # get ear of eyes
            avg_ear = self.eye_aspect_ratio(eyes[0]) + self.eye_aspect_ratio(eyes[1])
            avg_ear /= 2

            # store ear in ears
            self.ears.append(avg_ear)

            # cut the ears if length is too long
            if len(self.ears) > 15:
                self.ears.pop(0)

    def is_blink(self, update_ratio=0.1):
        """
        Using the sequence of ears, we can detect blinks
        :return: a int, -1 as unknown, 1 as blink detected, 0 as blink undetected
        """
        # use ears as the first filter for a blink
        ears_is_blink = False
        if len(self.ears) < 5:
            return -1

        # check if based on ears, it can be a blink
        center_ear = self.ears[-3]
        end_ear = (self.ears[-5] + self.ears[-1]) / 2

        ratio = end_ear / center_ear
        if ratio >= 1.06:
            ears_is_blink = True

        # use the eye region images as the second blink detection filter
        region_is_blink = False
        center_eye_region = self.eye_regions[-3]
        end_eye_region = cv2.addWeighted(self.eye_regions[-5], 0.5, self.eye_regions[-1], 0.5, 0)
        # get the average intensity of eye region difference
        diff = self.get_avg_intensity(cv2.subtract(center_eye_region, end_eye_region))

        # update average diff
        ratio = diff / self.avg_diff
        if self.avg_diff == -1:
            self.avg_diff = diff
        elif ratio < 1.75:
            self.avg_diff = (1 - update_ratio) * self.avg_diff + update_ratio * diff
        if ratio >= 2.5:
            region_is_blink = True

        # return ears_is_blink and region_is_blink
        return int(region_is_blink and ears_is_blink)

    def deviated_sight(self, shape):
        """
        determine the ratio of deviation: left2nose / right2nose
        :param shape: all facial landmarks
        :return: left2nose / right2nose
        """
        left_eye = shape[39]
        right_eye = shape[42]
        up_nose = shape[27]
        low_nose = shape[30]
        left2nose = self.point2line(left_eye, up_nose, low_nose)
        right2nose = self.point2line(right_eye, up_nose, low_nose)
        return left2nose / right2nose

def fetch_data(cycle_len, stream, detector, predictor, fe):
    # Fetch left right eye id range
    left_eye_start_id, left_eye_end_id = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
    right_eye_start_id, right_eye_end_id = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

    # Init data upload time recorder
    data_time_start = time.clock()
    outputs = []

    # p = Process(target=lambda x: print("initiating multithreading"), args=(None, ))
    # p.start()

    while True:
        # (Re)Init output data variable
        output = {}

        # upload data
        if time.clock() - data_time_start >= cycle_len:
            print("cycle length: ", time.clock() - data_time_start)
            # upload_data_sql(outputs)
            print("data length: ", len(outputs))
            return outputs

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
                cv2.putText(frame, "Blink: " + str(is_blink), (left_eye[0][0], left_eye[0][1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
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