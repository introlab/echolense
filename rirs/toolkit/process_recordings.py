import os
import shutil
import numpy as np
from tqdm import tqdm
from pathlib import Path
from scipy.io import wavfile
from scipy.signal import fftconvolve
from matplotlib.backends.backend_pdf import PdfPages

from .utils import show_rir
from .utils import generate_ess
from .utils import audio2float32
from .utils import ess_inverse_filter
from .utils import save_rir_in_pdf

BEFORE_PEAK = 192
AFTER_PEAK = 16000
# Sine sweep
t0 = 0.0
t1 = 10.0
fs = 16000
f0 = 20.0
f1 = fs / 2.

f = ess_inverse_filter(t0, t1, f0, f1, fs)

recordings_dir = Path('recordings')
files = list(recordings_dir.rglob('*.wav'))
files.sort()

if os.path.exists('processings'):
    shutil.rmtree('processings')

os.makedirs('processings')

pdf_file = PdfPages(os.path.join('processings', 'rirs.pdf'))

for file in tqdm(files, 'Processing files'):
    
    file_dir = os.path.basename(os.path.dirname(file))
    output_dir = os.path.join('processings', file_dir)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_file = os.path.basename(file).replace('.wav', '.npy')
    output_path = os.path.join(output_dir, output_file)
    
    fs, audio = wavfile.read(files[0])
    audio = audio2float32(audio)

    multichannel_rir = None

    for channel in range(audio.shape[1]):
        rir = fftconvolve(audio[:, channel], f, mode='full')[:, None]

        if multichannel_rir is None:
            multichannel_rir = rir
        else:
            multichannel_rir = np.concatenate((multichannel_rir, rir), axis=1)

    np.save(output_path, multichannel_rir)
    save_rir_in_pdf(pdf_file, output_path, multichannel_rir)

pdf_file.close()