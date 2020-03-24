"""
Test the full evolution framework
"""

import os,sys
sys.path.append(os.path.abspath('crossroads_scripts'))
from evolve_structure import get_evolved_structure
from param_estimation import get_error_for_model

import numpy as np
from scipy.io import wavfile
import scipy.signal as signal
import audio_dspy as adsp
import random

# read file
fs, x = wavfile.read('audio_files/drums.wav')
x = adsp.normalize(x)

ys = []
names = []

def add_to_tests(name, y, ys, names):
    ys.append(y)
    names.append(name)
    wavfile.write('audio_files/' + names[-1] + '.wav', fs, y)

# Gain
gain = -0.2
y1 = gain * x
add_to_tests('gain', y1, ys, names)

# Delay / Comb filter
delay_amt = 2 # samples
mix = -0.5
del_sig = np.zeros(np.shape(x))
N = len(x[:,0])
del_sig[delay_amt:,0] = x[:N-delay_amt,0]
del_sig[delay_amt:,1] = x[:N-delay_amt,1]
y2 = 0.5 * (x + del_sig * mix)
add_to_tests('delay', y2, ys, names)

# 4th-order FIR filter
b = [0.3, -0.4, 0.12, 0.2, -0.75]
y3 = np.zeros(np.shape(x))
y3[:,0] = signal.lfilter(b, [1], x[:,0])
y3[:,1] = signal.lfilter(b, [1], x[:,1])
add_to_tests('FIR_filter', y3, ys, names)

# Soft clipper
in_gain = 2.0
x_in = in_gain * np.copy(x)
x_in = np.minimum(x_in, 1)
x_in = np.maximum(x_in, -1)
y4 = x_in - np.power(x_in, 3) / 3
add_to_tests('Soft-clip', y4, ys, names)

# Weiner-Hammerstein (Currently doesn't work)
b1 = [0.3, -0.4]
x_weiner = np.zeros_like(x)
x_weiner[:,0] = signal.lfilter(b1, [1], x[:,0])
x_weiner[:,1] = signal.lfilter(b1, [1], x[:,1])

in_gain = 2.0
x_nl = in_gain * np.copy(x_weiner)
x_nl = np.minimum(x_in, 1)
x_nl = np.maximum(x_in, -1)
x_hammer = x_in - np.power(x_in, 3) / 3

b2 = [0.2, -0.75]
y5 = np.zeros_like(x)
y5[:,0] = signal.lfilter(b1, [1], x_hammer[:,0])
y5[:,1] = signal.lfilter(b1, [1], x_hammer[:,1])
# add_to_tests('Weiner-Hammerstein', y5, ys, names)

# Constants
orig_file = 'audio_files/drums.wav'
out_file = 'audio_files/evolve_struct.wav'

# Attempt to evolve all structures
for n in range(len(names)):
    print('Evolving structure for: {}'.format(names[n]))
    random.seed(0x3456)

    plugin = 'evolve_struct_' + names[n]
    model = get_evolved_structure(plugin, orig_file, out_file, 'audio_files/' + names[n] + '.wav')
    print(model)
    params,_ = model.get_params()
    err = get_error_for_model(params, model, plugin, orig_file, out_file, 'audio_files/' + names[n] + '.wav')
    assert err < 5e-5, "Final error = {}".format(err)

    print('Error: {}'.format(err))
    print('SUCCESS')


