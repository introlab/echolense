import os
import time
import shutil
import pyaudio
import argparse
import numpy as np
import simpleaudio as sa
from pynput import keyboard
from scipy.io import wavfile
from .utils import get_device_index
from .utils import generate_ess, fade_in

# Config
WIDTH = 2
CHUNK = 1024
RATE = 16000

N_MICS = 4
N_CHANNELS = 6
MIC_INDEXES = [1, 2, 3, 4]

REVERB_TIME = 3 * RATE
MICROPHONE_NAME = "ReSpeaker 4 Mic Array"


# Making output dir
parser = argparse.ArgumentParser()
parser.add_argument('-o', type=str, help="Output folder")
args = parser.parse_args()

if not os.path.exists('recordings'):
    os.makedirs('recordings')

output_dir = os.path.join('recordings', args.o)

if os.path.exists(output_dir):
    shutil.rmtree(output_dir)

os.makedirs(output_dir)

# Sine sweep
t0 = 0.0
t1 = 10.0
f0 = 20.0
f1 = RATE / 2.

sine_sweep, t = generate_ess(t0, t1, f0, f1, RATE)

sine_sweep_audio = sine_sweep.copy()
sine_sweep_audio *= 32767. / np.max(np.abs(sine_sweep_audio))
sine_sweep_audio = sine_sweep_audio.astype(np.int16)

# Global variables
rec_file_index = 0
should_record = False
microphone_is_active = False

audio_recording = np.zeros((1, N_MICS), dtype=np.int16)

# Functions
def microphone_callback(in_data, frame_count, *_):
    global audio_recording

    data = np.frombuffer(in_data, dtype=np.int16)
    data = data.reshape(frame_count, N_CHANNELS)
    data = data[:, MIC_INDEXES]

    if microphone_is_active:
        audio_recording = np.concatenate((audio_recording, data))

    return (in_data, pyaudio.paContinue)

def get_recording_filename():
    global f0, f1
    global output_dir
    global rec_file_index

    filename = None
    recording_files = os.listdir(output_dir)

    while filename is None or filename in recording_files:
        filename = (
            'rec_' +
            str(rec_file_index) + 
            '_f0_' +
            str(int(f0)) +
            '_f1_' +
            str(int(f1)) +
            '.wav')
        rec_file_index += 1

    return filename

def delete_last_recording_file():
    global output_dir
    global rec_file_index

    rec_file_index -= 1

    filename = (
            'rec_' +
            str(rec_file_index) + 
            '_f0_' +
            str(int(f0)) +
            '_f1_' +
            str(int(f1)) +
            '.wav')

    path = os.path.join(output_dir, filename)

    print(f'Attempting to delete file: {path}')

    if os.path.exists(path):
        os.remove(path)

def on_key_pressed(key):
    global should_record

    if key == keyboard.Key.space:
        should_record = True

    if key == keyboard.KeyCode.from_char('x'):
        delete_last_recording_file()

# Opening stream
p = pyaudio.PyAudio()
stream = p.open(
    input = True,
    rate = RATE,
    channels = N_CHANNELS,
    format = p.get_format_from_width(WIDTH),
    input_device_index= get_device_index(MICROPHONE_NAME),
    stream_callback = microphone_callback)

# Main loop
listener = keyboard.Listener(on_press=on_key_pressed)
listener.start()

try:
    while True:
        if should_record:

            audio_recording = np.zeros((1, N_MICS), dtype=np.int16)
            play_obj = sa.play_buffer(sine_sweep_audio, 1, 2, RATE)
            microphone_is_active = True

            play_obj.wait_done()
            playback_end_length = audio_recording.shape[0]
            
            while audio_recording.shape[0] < playback_end_length + REVERB_TIME:
                time.sleep(0.1)

            microphone_is_active = False

            filename = get_recording_filename()
            wavfile.write(os.path.join(output_dir, filename), RATE, audio_recording[1:, :])

            should_record = False
            print('Recording done!')
        
        time.sleep(0.1)

# Release resources
except KeyboardInterrupt:
    stream.stop_stream()
    stream.close()
    p.terminate()
