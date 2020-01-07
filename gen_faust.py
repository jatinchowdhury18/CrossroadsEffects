#%%
from abc import ABC, abstractmethod
from plugin_utils import compile_plugin, test_plugin
import uuid
import random as r
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

        file.write('\nprocess = _ :')
        for p in processors:
            file.write(' ' + p + ' :')

        file.write(' _;\n')

        file.close()

class Element(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get_faust(self):
        return ''

class Gain(Element):
    def __init__(self, value):
        id = get_uuid()
        self.name = 'gain_' + id
        self.parameters = { 'gain': value }

    def get_faust(self):
        return '{} = _*{};\n'.format(self.name, self.parameters['gain'])

class Delay(Element):
    def __init__(self):
        id = get_uuid()
        self.name = 'delay_' + id

    def get_faust(self):
        return '{} = _\';\n'.format(self.name)

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
