import os
import pyaudio
import librosa
import numpy as np
from ctypes import *
import scipy.signal as sg
import matplotlib.pyplot as plt

# To remove messages from ALSA
ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)
def py_error_handler(filename, line, function, err, fmt):
    pass

c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)

asound = cdll.LoadLibrary('libasound.so')
asound.snd_lib_error_set_handler(c_error_handler)


def list_mics():
    p = pyaudio.PyAudio()

    for idx in range(p.get_device_count()):
        device = p.get_device_info_by_index(idx)

        print('Name: ', device['name'],
            '- Max number of channels: ', device['maxInputChannels'])


def get_device_index(name):
    p = pyaudio.PyAudio()

    for i in range(p.get_device_count()):
        dev = p.get_device_info_by_index(i)

        if name in dev['name']:
            return i
        
def make_sine_sweep(t0, t1, f0, f1, fs):
    t = np.arange(int(t0 * fs), int(t1 * fs)) / fs
    chirp = sg.chirp(t, f0=f0, f1=f1, t1=t1, method='logarithmic').astype(np.float32)

    return chirp, t

def generate_ess(t0, t1, f0, f1, fs):
    t = np.arange(int(t0 * fs), int(t1 * fs)) / fs
    
    ln_f1_f0 = np.log(float(f1) / float(f0))
    K = (2. * np.pi * float(f0) * float(t1)) / ln_f1_f0
    
    ess = np.sin(K * (np.exp((ln_f1_f0 * t) / t1) - 1.0)).astype(np.float32)

    return ess, t

def ess_inverse_filter(t0, t1, f0, f1, fs):
    # Source: https://dsp.stackexchange.com/questions/41696/calculating-the-inverse-filter-for-the-exponential-sine-sweep-method
    ess, t = generate_ess(t0, t1, f0, f1, fs)
    R = np.log(float(f1) / float(f0))
    k = np.exp((t * R) / t1)

    f = np.flip(ess) / k

    return f

def fade_in(signal, duration):
    fade_in_curve = np.linspace(0., 1.0, duration)
    out = signal.copy()
    out[:duration] = fade_in_curve * out[:duration]

    return out

def audio2float32(audio):
    if audio.dtype == np.int16:
        audio = audio.astype(np.float32, order='C') / 32768.0

    elif audio.dtype == np.int32:
        audio = audio.astype(np.float32, order='C') / 2147483648.0

    elif audio.dtype == np.uint8:
        audio = (audio.astype(np.float32, order='C') - 127.) / 128.

    return audio

def show_rir(rir, fs=16000, channel = 0, freq_domain=True):
    if freq_domain:
        fig, ax = plt.subplots()

        R = np.abs(librosa.stft(rir[:, channel]))
        img = librosa.display.specshow(librosa.amplitude_to_db(R, ref=np.max), sr=fs, y_axis='linear', x_axis='time', ax=ax)

        ax.set_title('Impulse response')
        fig.colorbar(img, ax=ax, format="%+2.0f dB")
        plt.show()
    
    else:
        plt.figure()
        plt.plot(rir[:, channel])
        plt.show()


def save_rir_in_pdf(pdf_file, title, rir, fs=16000, channel = 0):
    fig, ax = plt.subplots()

    R = np.abs(librosa.stft(rir[:, channel]))
    img = librosa.display.specshow(librosa.amplitude_to_db(R, ref=np.max), sr=fs, y_axis='linear', x_axis='time', ax=ax)

    ax.set_title(title)
    fig.colorbar(img, ax=ax, format="%+2.0f dB")
    
    fig.savefig(pdf_file, format='pdf')
    plt.close()