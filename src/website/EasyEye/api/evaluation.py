import numpy as np
import datetime
import urllib.request
import urllib.parse
from statistics import median
import json
from api.evaluation_interface import create_alert, get_evaluation_data


def evaluation():
    condition = np.array([0, 0, 0, 0])
    # wrong_eye_direction, blink_too_slow, blur_sight, usage_too_long
    data = get_evaluation_data()
    time = data["timestamp"]
    start_time = data["start_point"]

    if len(time) < 1:
        return condition
    total_run_time = time[-1] - start_time
    curr_time_interval = time[-1] - time[0]
    condition[0] = wrong_direction(data['deviation'], curr_time_interval)
    condition[1] = blink_too_slow(data['blink'], time, curr_time_interval)
    condition[2] = blur_sight(data['squint'], time, curr_time_interval)
    condition[3] = usage_too_long(total_run_time)
    create_alert(alert_wrong_direction=condition[0],
                 alert_blink_slow=condition[1],
                 alert_blur_sight=condition[2],
                 alert_usage_overtime=condition[3])
    return condition


def wrong_direction(direction, curr_time_interval, interval_threshold=datetime.timedelta(minutes=5),
                    threshold=0.5):
    if curr_time_interval < interval_threshold:
        return 0
    # direction = median_filter(direction)
    direction_avg = np.average(direction)
    if abs(direction_avg-1) > threshold:
        return 1
    else:
        return 0


def blink_too_slow(blink, time, curr_time_interval, interval_threshold=datetime.timedelta(seconds=10)):
    if curr_time_interval < interval_threshold:
        return 0
    index = len(blink)-1
    # while index > -1:
    #     if time[-1] - time[index] > interval_threshold:
    #         break
    num_entry = np.count_nonzero(np.array(time) > (time[-1]-interval_threshold))
    if 1 not in blink[-num_entry:]:
        return 1
    else:
        return 0


def blur_sight(squint, time, curr_time_interval, interval_threshold=datetime.timedelta(minutes=2),
               squint_ratio=0.1):
    if curr_time_interval < interval_threshold:
        return 0
    index = len(squint) - 1
    # while index > -1:
    #     if time[-1] - time[index] > interval_threshold:
    #         break
    num_entry = np.count_nonzero(np.array(time) > (time[-1] - interval_threshold))
    threshold = num_entry * squint_ratio
    if np.count_nonzero(np.array(squint[-num_entry:]) < 0.24) > threshold:
        return 1
    else:
        return 0


def usage_too_long(total_run_time, time_threshold=datetime.timedelta(hours=1)):
    if total_run_time > time_threshold:
        return 1
    else:
        return 0


def median_filter(direction):
    filtered_direction = np.zeros_like(direction)
    for i in range(1,len(direction)-1):
        filtered_direction = median(direction[i-1, i+1])
    return filtered_direction


# send_alert([0,0,0,0])
# upload_data([0,1,2])
# get_request()

