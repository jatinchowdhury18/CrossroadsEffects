#%%
from abc import ABC, abstractmethod
from plugin_utils import compile_plugin, test_plugin, calc_error
import uuid
import random as r
from scipy.optimize import minimize
from scipy.io import wavfile
import audio_dspy as adsp
import numpy as np
import matplotlib.pyplot as plt
r.seed()

# %%
def get_uuid():
    return uuid.uuid4().hex[:8]

#%%
class Model:
    def __init__(self):
        self.elements = []

    def write_to_file(self, file):
        file = open('faust_scripts/'+file, 'w')
        file.write('import(\"stdfaust.lib\");\n\n')

        processors = []
        for e in self.elements:
            processors.append(e.name)
            file.write(e.get_faust())

        process_string = '\nprocess = _,_ :'
        for p in processors:
            process_string += ' ' + p + ',' + p + ' :'
        process_string += ' _,_;\n'
        file.write(process_string)

        file.close()

    def get_params(self):
        """Returns an array of parameters"""
        params = []
        bounds = []

        for e in self.elements:
            e.get_params(params, bounds)

        return params, bounds

    def set_params(self, params):
        idx = 0
        for e in self.elements:
            idx = e.set_params(params, idx)

class Element(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get_faust(self):
        return ''

    @abstractmethod
    def get_params(self, params, bounds):
        pass

    @abstractmethod
    def set_params(self, params, idx):
        return idx

class Gain(Element):
    def __init__(self, value=0):
        id = get_uuid()
        self.name = 'gain_' + id
        self.gain = value

    def get_faust(self):
        return '{} = _*{};\n'.format(self.name, self.gain)

    def get_params(self, params, bounds):
        params.append(self.gain)
        bounds.append((-10, 10))

    def set_params(self, params, idx):
        self.gain = params[idx]
        return idx + 1

class Delay(Element):
    def __init__(self, length=0):
        id = get_uuid()
        self.name = 'delay_' + id
        self.length = length

    def get_faust(self):
        return '{} = @({});\n'.format(self.name, int(self.length*100))

    def get_params(self, params, bounds):
        params.append(self.length)
        bounds.append((0, 1))

    def set_params(self, params, idx):
        self.length = params[idx]
        return idx + 1

class Split(Element):
    def __init__(self, elements):
        id = get_uuid()
        self.name = 'split_' + id
        self.elements = elements

        self.faust = '_ <: '
        for chain in elements:
            if len(chain) == 0:
                self.faust += '_'
            else:
                self.faust += '('
                for e in chain:
                    self.faust += e.name + ' : '
                self.faust = self.faust[:-3]
                self.faust += ')'    
            self.faust += ', '
        
        self.faust = self.faust[:-2]
        self.faust += ' :> _'

    def get_faust(self):
        string = ''
        for chain in self.elements:
            for e in chain:
                string += e.get_faust()

        string += '{} = {};\n\n'.format(self.name, self.faust)
        return string

    def get_params(self, params, bounds):
        for chain in self.elements:
            for e in chain:
                e.get_params(params, bounds)

    def set_params(self, params, idx):
        for chain in self.elements:
            for e in chain:
                idx = e.set_params(params, idx)
        return idx

class Feedback(Element):
    def __init__(self, elements):
        id = get_uuid()
        self.name = 'fb_' + id
        self.elements = elements

        self.faust = '+~'
        if len(elements) == 0:
            self.faust += '(_*0)'
        else:
            self.faust += '('
            for e in elements:
                self.faust += e.name + ' : '
            self.faust = self.faust[:-3]
            self.faust += ')'

    def get_faust(self):
        string = ''
        for e in self.elements:
            string += e.get_faust()

        string += '{} = {};\n\n'.format(self.name, self.faust)
        return string

    def get_params(self, params, bounds):
        for e in self.elements:
            e.get_params(params, bounds)

    def set_params(self, params, idx):
        for e in self.elements:
            idx = e.set_params(params, idx)
        return idx
    
def optimize_model(model, name, in_wav, out_wav, des_wav, tol=1.0e-4):
    params, bounds = model.get_params()
    result = minimize(get_error_for_model, params, args=(model, name, in_wav, out_wav, des_wav),
                      bounds=bounds, options={'maxiter': 100, 'gtol': 1.0e-6, 'ftol': 5.0e-9,'eps': 5.0e-6, 'disp': True, 'iprint': 101}, tol=tol)

    print(result.message)
    return result.x

def get_error_for_model(params, model, name, in_wav, out_wav, des_wav):
    model.set_params(params)
    model.write_to_file(name + '.dsp')
    compile_plugin(name)

    test_plugin(name, in_wav, out_wav)

    fs, y = wavfile.read(des_wav)
    fs, y_test = wavfile.read(out_wav)

    # normalize for wav files
    y = y / 2**15 if np.max(np.abs(y)) > 10 else y
    y_test = y_test / 2**15 if np.max(np.abs(y_test)) > 10 else y_test

    return calc_error(y, y_test, fs)


#%%
# model = Model()

# Simple example
# model.elements.append(Gain(0.5))
# model.elements.append(Delay())

# FIR example
# model.elements.append(Split([[], [Gain(0.5), Delay()], [Gain(-0.2)]]))

# IIR example
# model.elements.append(Feedback([Gain(0.5), Delay()]))

# %%
def get_element(arg, split_recursion=0, fb_recursion=0):
    if (split_recursion > 3): # and (arg == 2):
        arg = 0
    
    if (fb_recursion > 3): # and (arg == 3):
        arg = 0

    if arg == 0: # gain
        return Gain(r.uniform(-1.0, 1.0))

    elif arg == 1: # delay
        return Delay()

    elif arg == 2: # split
        spr = split_recursion + 1
        num_chains = r.randint(1, 5)
        elements = []
        for _ in range(num_chains):
            chain = []
            num_elements = r.randint(0, 5)
            for _ in range(num_elements):
                chain.append(get_element(r.randint(0, 3), split_recursion=spr, fb_recursion=fb_recursion))
            elements.append(chain)
        return Split(elements)

    elif arg == 3: # feedback
        elements = []
        num_elements = r.randint(0, 5)
        fbr = fb_recursion + 1
        for _ in range(num_elements):
            elements.append(get_element(r.randint(0, 3), split_recursion=split_recursion, fb_recursion=fbr))
        return Feedback(elements)


def gen_random_model():
    model = Model()
    num_elements = r.randint(1, 4)

    for _ in range(num_elements):
        model.elements.append(get_element(r.randint(0, 3)))
    
    return model

# model = gen_random_model()
# model.write_to_file('test_gen.dsp')

#%%
# compile_plugin('test_gen')
# test_plugin('test_gen', 'drums.wav', 'drums_out.wav')
