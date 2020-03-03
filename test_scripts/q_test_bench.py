import os,sys
sys.path.append(os.path.abspath('crossroads_scripts'))
from param_estimation import get_error_for_model
from  gen_faust import Model, Split, Gain, UnitDelay
from plugin_utils import calc_error
import numpy as np
import time
from scipy.io import wavfile

model = Model()
model.elements.append(Split([[Gain(), Gain()], [UnitDelay(), Gain()], [Gain(0.2)]]))
name = 'test'

# Constants
plugin = 'bench'
orig_file = 'audio_files/drums.wav'
out_file = 'audio_files/bench.wav'
N = 50
params, bounds = model.get_params()

def test_get_error(params, model, name, in_wav, out_wav, des_wav):
    model.set_params(params)
    model.write_to_file(name + '.dsp')

    os.system('faust -a modules/faust/architecture/sndfile.cpp faust_scripts/{0}.dsp -o {0}.cpp'.format(name))
    os.system('g++ {0}.cpp -o {0} -lsndfile'.format(name))
    os.system('./{} {} {}'.format(name, in_wav, out_wav))
    os.system('rm {0}; rm {0}.cpp'.format(name))

    fs, y = wavfile.read(des_wav)
    fs, y_test = wavfile.read(out_wav)

    # normalize for wav files
    y = y / 2**15 if np.max(np.abs(y)) > 10 else y
    y_test = y_test / 2**15 if np.max(np.abs(y_test)) > 10 else y_test

    return calc_error(y, y_test, fs)

# Time loop
tick = time.time()
for _ in range(N):
    # err = get_error_for_model(params, model, plugin, orig_file, out_file, 'audio_files/drums.wav')
    err = test_get_error(params, model, plugin, orig_file, out_file, 'audio_files/drums.wav')
    

time = time.time() - tick
time_per_iter = time / N

print('Time per iterations: {:.3f} seconds'.format(time_per_iter))
assert time_per_iter < 10, 'To Slow!!!'

print('SUCCESS')

