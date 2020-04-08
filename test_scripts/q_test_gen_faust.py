"""
Test that the system can correctly generate Faust code
for a biquad filter and compile it to a plugin
"""

import os,sys
sys.path.append(os.path.abspath('crossroads_scripts'))
from gen_faust import Model,Element,Gain,UnitDelay,Delay,CubicNL,Split,Feedback,FB2
from plugin_utils import compile_plugin, test_plugin, calc_error
from param_estimation import get_error_for_model

import numpy as np
from scipy.io import wavfile
import scipy.signal as signal
import audio_dspy as adsp
import matplotlib.pyplot as plt
import time

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

# Two pole
pole_mag = 0.2
pole_angle = 1.0 # works up to ~1.8

root1 = pole_mag * np.exp(+1j * pole_angle)
root2 = pole_mag * np.exp(-1j * pole_angle)
poly = np.poly((root1, root2))

yTP = np.zeros(np.shape(x))
yTP[:,0] = signal.lfilter([1], [1, poly[1], poly[2]], x[:,0])
yTP[:,1] = signal.lfilter([1], [1, poly[1], poly[2]], x[:,1])

modelTP = Model()
fb = FB2()
fb.pole_mag = pole_mag
fb.pole_angle = pole_angle
modelTP.elements.append(fb)
add_to_tests(modelTP, 'Two-pole-test', yTP, ys, names, models)

# Lowpass filter
b, a = adsp.design_LPF2(1000, 0.7071, fs)
yLPF = np.zeros(np.shape(x))
yLPF[:,0] = signal.lfilter(b, a, x[:,0])
yLPF[:,1] = signal.lfilter(b, a, x[:,1])

modelLPF = Model('DF2_Test')
modelLPF.elements.append(Feedback([Split([[Gain(a[1])], [UnitDelay(), Gain(a[2])]]), Gain(-1.0)]))
modelLPF.elements.append(Split([[Gain(b[0])], [UnitDelay(), Gain(b[1])], [UnitDelay(), UnitDelay(), Gain(b[2])]]))
add_to_tests(modelLPF, 'test_DF2', yLPF, ys, names, models)

for n in range(len(models)):
    print(f'Generating Faust for: {names[n]}')
    print(models[n])
    
    # Write to file and compile
    models[n].write_to_file(f'{names[n]}.dsp')
    compile_plugin(f'{names[n]}')

    # Test
    test_plugin(f'{names[n]}', 'audio_files/drums.wav', f'audio_files/{names[n]}.wav')

    fs, y_test = wavfile.read(f'audio_files/{names[n]}.wav')
    y_test = y_test / 2**15 if np.max(np.abs(y_test)) > 10 else y_test

    err = calc_error(ys[n], y_test, fs)
    assert err < 1.0e-4, 'Error: {}'.format(err)

    print('Error: {}'.format(err))
print('SUCCESS')

get_time = False
if get_time:
    tic = time.time()
    params, _ = model.get_params()
    # get_error_for_model(params, model, 'test_DF2', 'drums.wav', 'drums_out.wav', 'drums-wet.wav')
    compile_plugin('test_DF2')
    print('Took {} seconds to run.'.format(time.time() - tic))
