import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
from gen_faust import Model,Element,Gain,Delay,Split,Feedback,optimize_model
from plugin_utils import compile_plugin, test_plugin, calc_error

import numpy as np
from scipy.io import wavfile
import scipy.signal as signal
import audio_dspy as adsp
import matplotlib.pyplot as plt

# read file
fs, x = wavfile.read('drums.wav')
x = adsp.normalize(x)

# Do delay and mix
gain = -0.2

y = gain * x

# output wet file
wavfile.write('drums-gain-wet.wav', fs, y)

# Create model
model = Model()
model.elements.append(Gain(-0.18))

# unoptimized error: ~0.016
params = optimize_model(model, 'test_gain_opt', 'drums.wav', 'drums_gain_out.wav', 'drums-gain-wet.wav', tol=1.0e-4)
model.set_params(params)

# Write to file and compile
model.write_to_file('test_gain_opt.dsp')
compile_plugin('test_gain_opt')

# Test
test_plugin('test_gain_opt', 'drums.wav', 'drums_gain_out.wav')

fs, y_test = wavfile.read('drums_gain_out.wav')
y_test = adsp.normalize(y_test)

err = calc_error(y, y_test, fs)
assert err < 5.0e-3, "Final error = {}".format(err)

print('Error: {}'.format(err))
print('SUCCESS')
