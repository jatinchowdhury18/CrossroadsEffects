import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
from evolve_structure import get_evolved_structure
from param_estimation import get_error_for_model

import numpy as np
from scipy.io import wavfile
import audio_dspy as adsp
import random

random.seed(0x34567890)

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

# Constants
plugin = 'evolve_struct'
orig_file = 'audio_files/drums.wav'
out_file = 'audio_files/evolve_struct.wav'

# Attempt to evolve all structures
for n in range(len(names)):
    print('Evolving structure for: {}'.format(names[n]))

    model = get_evolved_structure(plugin, orig_file, out_file, 'audio_files/' + names[n] + '.wav')
    params,_ = model.get_params()
    err = get_error_for_model(params, model, plugin, orig_file, out_file, 'audio_files/' + names[n] + '.wav')
    assert err < 5e-5, "Final error = {}".format(err)

    print('Error: {}'.format(err))
    print('SUCCESS')


