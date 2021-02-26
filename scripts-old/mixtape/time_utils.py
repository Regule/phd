import numpy as np
from datetime import datetime, timedelta

EPOCH_STR_FORMAT = '%Y-%m-%d %H:%M:%S'

def epoch_str_to_timestamp(epoch_str):
    return datetime.strptime(epoch_str, EPOCH_STR_FORMAT).timestamp()

def timestamp_to_epoch_str(timestamp):
    dt = datetime.fromtimestamp(timestamp)
    return dt.strftime(EPOCH_STR_FORMAT)

def date_str_to_datetime(date_str):
    return datetime.strptime(date_str,'%Y-%m-%d')


def build_timestamps(start, end, delta):
    timestamps = []
    if type(start) == float:
        start = datetime.fromtimestamp(start)
    if type(start) == float:
        end = datetime.fromtimestamp(end)
    timestamp = start
    delta = timedelta(minutes=delta)
    while timestamp < end:
        timestamps.append(timestamp)
        timestamp += delta
    timestamps = np.asarray(list(map(lambda x: x.timestamp(), timestamps)))
    return timestamps

def build_epochs(start,delta,count):
    timestamps = []
    if type(start) == float:
        start = datetime.fromtimestamp(start)
    timestamp = start
    delta = timedelta(minutes=delta)
    for _ in range(count):
        timestamps.append(timestamp)
        timestamp += delta
    return timestamps
