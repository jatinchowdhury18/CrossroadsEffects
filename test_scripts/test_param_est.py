import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
from gen_faust import Model,Element,Gain,Delay,Split,Feedback
from param_estimation import estimate_params,get_error_for_model

import numpy as np
from scipy.io import wavfile
import scipy.signal as signal
import audio_dspy as adsp
import matplotlib.pyplot as plt

# read file
fs, x = wavfile.read('audio_files/drums.wav')
x = adsp.normalize(x)

# structures to estimate
ys = []
names = []
models = []

# Gain
gain = -0.2
y1 = gain * x
ys.append(y1)
names.append('gain')
wavfile.write('audio_files/' + names[-1] + '.wav', fs, y1)

model1 = Model()
model1.elements.append(Gain())
models.append(model1)

# Delay / Comb filter
delay_amt = 20 # samples
mix = -0.5
del_sig = np.zeros(np.shape(x))
N = len(x[:,0])
del_sig[delay_amt:,0] = x[:N-delay_amt,0]
del_sig[delay_amt:,1] = x[:N-delay_amt,1]
y2 = 0.5 * (x + del_sig * mix)
ys.append(y2)
names.append('delay')
wavfile.write('audio_files/' + names[-1] + '.wav', fs, y2)

model2 = Model()
model2.elements.append(Split([[], [Delay(), Gain()]]))
model2.elements.append(Gain())
models.append(model2)

plugin = 'param_est'
orig_file = 'audio_files/drums.wav'
out_file = 'audio_files/param_est.wav'
# Estimate all structures
for n in range(len(models)):
    print('Estimating params for: {}'.format(names[n]))
    params = estimate_params(models[n], plugin, orig_file, out_file, 'audio_files/' + names[n] + '.wav')
    models[n].set_params(params)

    err = get_error_for_model(params, models[n], plugin, orig_file, out_file, 'audio_files/' + names[n] + '.wav')
    assert err < 5.0e-2, "Final error = {}".format(err)

    print('Error: {}'.format(err))
    print('SUCCESS')
