import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
from gen_faust import Model,Element,Gain,UnitDelay,Delay,CubicNL,Split,Feedback
from param_estimation import estimate_params,get_error_for_model,optimize_model

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

def add_to_tests(model, name, y, ys, names, models):
    ys.append(y)
    names.append(name)
    wavfile.write('audio_files/' + names[-1] + '.wav', fs, y)
    models.append(model)

# Gain
gain = -0.2
y1 = gain * x

model1 = Model()
model1.elements.append(Gain())
add_to_tests(model1, 'gain', y1, ys, names, models)

# Delay / Comb filter
delay_amt = 5 # samples
mix = -0.5
del_sig = np.zeros(np.shape(x))
N = len(x[:,0])
del_sig[delay_amt:,0] = x[:N-delay_amt,0]
del_sig[delay_amt:,1] = x[:N-delay_amt,1]
y2 = 0.5 * (x + del_sig * mix)

model2 = Model()
model2.elements.append(Split([[], [Delay(5), Gain(0.9)]]))
model2.elements.append(Gain(-0.1))
add_to_tests(model2, 'delay', y2, ys, names, models)

# 4th-order FIR filter
b = [0.3, -0.4, 0.12, 0.2, -0.75]
y3 = np.zeros(np.shape(x))
y3[:,0] = signal.lfilter(b, [1], x[:,0])
y3[:,1] = signal.lfilter(b, [1], x[:,1])

model3 = Model()
model3.elements.append(Split([[Gain()], [UnitDelay(),Gain()], [Delay(2),Gain()],
    [Delay(3),Gain()], [Delay(4),Gain()]]))
add_to_tests(model3, 'FIR filter', y3, ys, names, models)

# One-pole filter
fb_gain = -0.2
y4 = np.zeros(np.shape(x))
y4[:,0] = signal.lfilter([1], [1, -fb_gain], x[:,0])
y4[:,1] = signal.lfilter([1], [1, -fb_gain], x[:,1])

model4 = Model()
model4.elements.append(Feedback([Gain()]))
add_to_tests(model4, 'One-pole', y4, ys, names, models)

# Soft-clip distortion
in_gain = 2.0
x_in = in_gain * np.copy(x)
x_in = np.minimum(x_in, 1)
x_in = np.maximum(x_in, -1)
y5 = x_in - np.power(x_in, 3) / 3

model5 = Model()
model5.elements.append(Gain())
model5.elements.append(CubicNL())
add_to_tests(model5, 'Soft-clip', y5, ys, names, models)

# Lowpass Filter
b, a = adsp.design_LPF2(1000, 0.7071, fs)
y6 = np.zeros(np.shape(x))
y6[:,0] = signal.lfilter(b, a, x[:,0])
y6[:,1] = signal.lfilter(b, a, x[:,1])

model6 = Model()
model6.elements.append(Feedback([Split([[Gain()], [UnitDelay(), Gain()]])]))
model6.elements.append(Split([[Gain()], [UnitDelay(), Gain()], [UnitDelay(), UnitDelay(), Gain()]]))
# add_to_tests(model6, 'LPF', y6, ys, names, models)

# Constants
plugin = 'param_est'
orig_file = 'audio_files/drums.wav'
out_file = 'audio_files/param_est.wav'
# Estimate all structures
for n in range(len(models)):
    print('Estimating params for: {}'.format(names[n]))
    # params = estimate_params(models[n], plugin, orig_file, out_file, 'audio_files/' + names[n] + '.wav')
    params = optimize_model(models[n], plugin, orig_file, out_file, 'audio_files/' + names[n] + '.wav', tol=1e-5)
    models[n].set_params(params)
    print(params)

    err = get_error_for_model(params, models[n], plugin, orig_file, out_file, 'audio_files/' + names[n] + '.wav')
    assert err < 5e-5, "Final error = {}".format(err)

    print('Error: {}'.format(err))

print('SUCCESS')
