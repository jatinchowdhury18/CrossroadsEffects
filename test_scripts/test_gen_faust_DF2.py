import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
from gen_faust import Model,Element,Gain,Delay,Split,Feedback
from plugin_utils import compile_plugin, test_plugin

import numpy as np
from scipy.io import wavfile
import scipy.signal as signal
import audio_dspy as adsp
import matplotlib.pyplot as plt

# read file
fs, x = wavfile.read('drums.wav')
x = adsp.normalize(x)

# Design filter
b, a = adsp.design_LPF2(1000, 0.7071, fs)
y = np.zeros(np.shape(x))
y[:,0] = signal.lfilter(b, a, x[:,0])
y[:,1] = signal.lfilter(b, a, x[:,1])

# output wet file
wavfile.write('drums-wet.wav', fs, y)

# Create model
model = Model()
model.elements.append(Feedback([Split([[Gain(a[1])], [Delay(), Gain(a[2])]]), Gain(-1.0)]))
model.elements.append(Split([[Gain(b[0])], [Delay(), Gain(b[1])], [Delay(2), Gain(b[2])]]))

# Write to file and compile
model.write_to_file('test_DF2.dsp')
compile_plugin('test_DF2')

# Test
test_plugin('test_DF2', 'drums.wav', 'drums_out.wav')

fs, y_test = wavfile.read('drums_out.wav')
y_test = adsp.normalize(y_test)

err = np.abs(y - y_test)
assert(np.max(err) < 0.05)
