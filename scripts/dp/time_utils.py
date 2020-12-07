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

def date_str_to_timestamp(date_str):
    return datetime.strptime(date_str,'%Y-%m-%d').timestamp()


def epoch_to_str(epoch):
    return epoch.strftime(EPOCH_STR_FORMAT)


def build_timestamps(start, end, delta):
    timestamps = []
    timestamp = start
    delta = timedelta(minutes=delta)
    while timestamp < end:
        timestamps.append(timestamp)
        timestamp += delta
    timestamps = np.asarray(list(map(lambda x: x.timestamp(), timestamps)))
    return timestamps
