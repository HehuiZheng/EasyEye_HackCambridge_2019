import numpy as np
import datetime
import urllib.request
import urllib.parse
from statistics import median
import json
from api.evaluation_interface import get_all_data


def summary():
    data_summary = {}
    # wrong_eye_direction, blink_too_slow, blur_sight, usage_too_long
    data = get_all_data(timespan=24*60*60)
    times = data["timestamp"]
    blink = data['blink']
    deviation = data['deviation']
    squint = data['squint']
    start_point = data['start_point']
    data_summary['average_blink'],
    data_summary['total_usage_time'],
    data_summary['time_list'],
    data_summary['average_blink_list'] = average_blink_per_min(blink, times, start_point)

    return data_summary


def total_usage_time(start_list, end_list):
    total = datetime.timedelta(seconds=0)
    for (start_time, end_time) in zip(start_list,end_list):
        total += (end_time-start_time)
    return total

def average_blink_per_min(blink, times, start_point_list):
    blink_total_count = np.count_nonzero(np.array(blink))
    time_prev = None
    for time in times:
        if time_prev == N
    total_time = total_usage_time(start_list, end_list)
    return average_blink, total_usage_time, time_list, average_blink_list
