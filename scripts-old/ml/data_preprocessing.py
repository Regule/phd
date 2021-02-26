import numpy as np
import json

# NOT A PROPER SCIKIT-LEARN TRANSFORMER !!!
class Differentiator:

    def __init__(self, start_point=0.0, end_point=0.0):
        self.start_point = start_point
        self.end_point = end_point


    def fit(self, time_series):
        self.end_point = time_series[-1]
        self.start_point = time_series[0]

    def transform(self, time_series):
        return np.diff(time_series)

    def fit_transform(self, time_series):
        self.fit(time_series)
        return self.transform(time_series)

    def reverse_transform(self, time_series, append_mode=False):
        time_series = np.insert(time_series, 0,
                                self.end_point if append_mode else self.start_point,
                                axis=0)
        return np.cumsum(time_series)


# NOT A PROPER SCIKIT-LEARN TRANSFORMER !!!
class MeanShifter:

    def __init__(self, mean=0.0):
        self.mean = mean

    def fit(self, time_series):
        self.mean = np.mean(time_series)

    def transform(self, time_series):
        return time_series - self.mean

    def fit_transform(self, time_series):
        self.fit(time_series)
        return self.transform(time_series)

    def reverse_transform(self, time_series):
        return time_series + self.mean


# NOT A PROPER SCIKIT-LEARN TRANSFORMER !!!
class CustomScaler:

    def __init__(self, scale=1.0):
        self.scale = scale

    def fit(self, time_series):
        self.scale = self.scale = 1.0/max(np.max(time_series), 0.0-np.min(time_series))

    def transform(self, time_series):
        return time_series * self.scale

    def fit_transform(self, time_series):
        self.fit(time_series)
        return self.transform(time_series)

    def reverse_transform(self, time_series):
        return time_series / self.scale
    

# NOT A PROPER SCIKIT-LEARN TRANSFORMER !!!
class TimeReferenceShifter:

    def __init__(self, t_zero=0, delta_t=1):
        self.t_zero = t_zero
        self.t_end = t_zero
        self.delta_t = delta_t

    def fit(self, time_series):
        self.t_zero = time_series[0]
        self.t_end = time_series[-1]
        self.delta_t = time_series[1]-time_series[0]

    def transform(self, time_series):
        return np.arange(time_series.shape[0])

    def fit_transform(self, time_series):
        self.fit(time_series)
        return self.transform(time_series)

    def reverse_transform(self, time_series):
        return time_series*self.delta_t+self.t_zero


# NOT A PROPER SCIKIT-LEARN TRANSFORMER !!!
# DIFFERENTIATOR MUST BE FITTED FOR NEW DATA
class DataPreprocessor:

    def __init__(self, t_zero=0, delta_t=1, mean=0.0, scale=1.0):
        self.timeframe_shifter = TimeReferenceShifter(t_zero, delta_t)
        self.mean_shifter = MeanShifter(mean)
        self.scaler = CustomScaler(scale)
        self.differentiator = Differentiator()


    def fit(self, x, y):
        self.timeframe_shifter.fit(x)
        y = self.differentiator.fit_transform(y)
        y = self.mean_shifter.fit_transform(y)
        self.scaler.fit(y)

    def fit_differentiator(self, y):
        self.differentiator.fit(y)

    def transform_timeframe(self, timeframe):
        timeframe = self.timeframe_shifter.transform(timeframe)
        return timeframe.reshape(-1,1)
        
    def transform(self, x, y):
        x = self.timeframe_shifter.transform(x)
        y = self.differentiator.transform(y)
        x = x[1:]
        y = self.mean_shifter.transform(y)
        y = self.scaler.transform(y)
        x = x.reshape(-1,1)
        y = y.reshape(-1,1)
        return x, y

    def reverse_transform(self, x, y):
        x = x.flatten()
        y = y.flatten()
        y = self.scaler.reverse_transform(y)
        y = self.mean_shifter.reverse_transform(y)
        x = np.insert(x, 0, 0, axis=0)
        y = self.differentiator.reverse_transform(y)
        x = self.timeframe_shifter.reverse_transform(x)
        return x, y

    def fit_transform(self, x, y):
        self.fit(x, y)
        return self.transform(x, y)

    def to_json(self, filename):
        params = {'t_zero':self.timeframe_shifter.t_zero,
                  'delta_t':self.timeframe_shifter.delta_t,
                  'mean':self.mean_shifter.mean,
                  'scale':self.scaler.scale}
        with open(filename, 'w') as json_file:
            json.dump(params, json_file)

    @staticmethod
    def load_json(filename):
        config = None
        with open(filename, 'r') as json_file:
            config = json.load(json_file)
        return DataPreprocessor(**config)    

    def __str__(self):
        params = {'t_zero':self.timeframe_shifter.t_zero,
                  'delta_t':self.timeframe_shifter.delta_t,
                  'mean':self.mean_shifter.mean,
                  'scale':self.scaler.scale,
                  'start_point': self.differentiator.start_point,
                  'end_point': self.differentiator.end_point}
        return str(params)


def build_windowed_data(time_series, window_size):
    windows = []
    outputs = []
    step = 0
    while step + window_size < time_series.shape[0]:
        windows.append(time_series[step:step+window_size])
        outputs.append(time_series[step+window_size])
        step += 1
    return np.asarray(windows), np.asarray(outputs)
