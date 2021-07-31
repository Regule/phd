import json
import numpy as np
import matplotlib.pyplot as plt


# /---------------------------------------------------------------------------------------------------------\
# |                                           GENERATING DEMO SIGNALS                                       |
# \---------------------------------------------------------------------------------------------------------/
def generate_sampling(start_timestamp, end_timestamp, frequency):
    sample_count = (end_timestamp - start_timestamp) * frequency
    sampling = np.linspace(start_timestamp, end_timestamp, sample_count)
    return sampling


class Sinusoid:

    def __init__(self, amplitude, frequency, phase_shift, amplitude_shift):
        self.amplitude = amplitude
        self.frequency = frequency
        self.phase_shift = phase_shift
        self.amplitude_shift = amplitude_shift


    def generate_timeseries(self, sampling):        
        time_series = self.amplitude * np.sin(2*np.pi*self.frequency*sampling + self.phase_shift) + self.amplitude_shift
        return time_series

    @staticmethod
    def generate_random_sinusoid(amplitude, frequency, phase_shift, amplitude_shift):
        a = np.random.uniform(amplitude[0], amplitude[1])
        f = np.random.uniform(frequency[0], frequency[1])
        shift = np.random.uniform(amplitude_shift[0], amplitude_shift[1])
        phase = np.random.uniform(phase_shift[0], phase_shift[1])
        return Sinusoid(a, f, phase, shift)

    def to_json(self):
        return json.dumps(vars(self))


class Signal:

    def __init__(self, carrier, signals):
        self.carrier = carrier
        self.signals = signals

    def generate_timeseries(self, sampling):
        time_series = self.carrier.generate_timeseries(sampling)
        for signal in self.signals:
            time_series += signal.generate_timeseries(sampling)
        return time_series

    @staticmethod
    def generate_random_signal(amplitude, frequency, phase_shift, amplitude_shift, signal_count):
        carrier = Sinusoid(amplitude[1], frequency[0], 0, 0)
        signals = []
        for _ in range(signal_count):
            signals.append(Sinusoid.generate_random_sinusoid(amplitude, frequency, phase_shift, amplitude_shift))
        return Signal(carrier, signals)

    def to_json(self):
        contents = {'carrier':vars(self.carrier)}
        serialized_signals = []
        for signal in self.signals:
            serialized_signals.append(vars(signal))
        contents['signals'] = serialized_signals
        return json.dumps(contents)


# /---------------------------------------------------------------------------------------------------------\
# |                                             PLOTTING EXAMPLES                                           |
# \---------------------------------------------------------------------------------------------------------/

def get_random_data(amplitude=(1,20), frequency=(1,3000), phase_shift=(0,3), amplitude_shift=(0,3), signal_count=7):
    signal = Signal.generate_random_signal(amplitude, frequency, phase_shift, amplitude_shift, signal_count)
    sampling = generate_sampling(0, 100, 1)
    return sampling, signal.generate_timeseries(sampling)

def simple_demo():
    x, y = get_random_data()
    plt.title('Simple plot')
    plt.plot(x,y)
    plt.xlabel('Measurement')
    plt.ylabel('Signal strength')
    plt.show()

def multiple_signals():
    x1, y1 = get_random_data()
    x2, y2 = get_random_data(signal_count=0)
    x3, y3 = get_random_data(amplitude=(30,35), frequency=(400,200))

    plt.title('Multiple signals with legend')
    plt.plot(x1, y1, label='First signal')
    plt.plot(x2, y2, label='Second signal', linestyle='--', linewidth=4)
    plt.plot(x3, y3, label='Third signal')
    plt.legend(loc='upper right')
    plt.xlabel('Measurement')
    plt.ylabel('Signal strength')
    plt.show()

def multiple_plots():
    x, y = get_random_data()
    cx, cy = get_random_data(signal_count=0)

    fig = plt.figure()
    ax1 = fig.add_subplot(2, 2, 1)
    ax2 = fig.add_subplot(2, 2, 2, sharex=ax1, sharey=ax1)
    ax3 = fig.add_subplot(2, 1, 2)
    
    ax1.set_title('Signal')
    ax1.plot(x, y, label='Signal')

    ax2.set_title('Carrier')
    ax2.plot(cx, cy, label='Carrier')

    # FIXME : I NEED TO UNDESTAND THIS BLACK MAGIC 
    ps = np.abs(np.fft.fft(y))**2
    time_step = 1 / 30
    freqs = np.fft.fftfreq(y.size, time_step)
    idx = np.argsort(freqs)
    #----------------------------------------------
    ax3.set_title('Frequency spectrum')
    ax3.plot(freqs[idx], ps[idx])
    
    plt.suptitle('Mutliple plots at once')
    plt.show()
    
def main():
    simple_demo()
    multiple_signals()
    multiple_plots()

if __name__ == '__main__':
    main()
