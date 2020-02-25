import os,sys
sys.path.append(os.path.abspath('crossroads_scripts'))
from param_estimation import get_error_for_model
from  gen_faust import Model, Split, Gain
import numpy as np
import time

model = Model()
model.elements.append(Split([[Gain(), Gain()], [Gain()], [Gain()]]))
name = 'test'

# Constants
plugin = 'bench'
orig_file = 'audio_files/drums.wav'
out_file = 'audio_files/bench.wav'
N = 5
params, bounds = model.get_params()

# Time loop
tick = time.time()
for _ in range(N):
    err = get_error_for_model(params, model, plugin, orig_file, out_file, 'audio_files/drums.wav')

time = time.time() - tick
time_per_iter = time / N

print('Time per iterations: {:.3f} seconds'.format(time_per_iter))
assert time_per_iter < 10, 'To Slow!!!'

print('SUCCESS')
