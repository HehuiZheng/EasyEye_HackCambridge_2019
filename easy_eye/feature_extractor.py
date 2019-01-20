import numpy as np
import cv2
from scipy.spatial import distance as dist


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