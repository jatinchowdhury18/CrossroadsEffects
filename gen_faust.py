#%%
from abc import ABC, abstractmethod
from plugin_utils import compile_plugin, test_plugin
import uuid

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
            file.write(' ' + p + ' : ')

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
        id = uuid.uuid4().hex[:4]
        self.name = 'gain_' + id
        self.parameters = { 'gain': value }

    def get_faust(self):
        return '{} = _*{};\n'.format(self.name, self.parameters['gain'])

class Delay(Element):
    def __init__(self):
        id = uuid.uuid4().hex[:4]
        self.name = 'delay_' + id

    def get_faust(self):
        return '{} = _\';\n'.format(self.name)

class Split(Element):
    def __init__(self, elements):
        id = uuid.uuid4().hex[:4]
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

        string += '{} = {};\n'.format(self.name, self.faust)
        return string

class Feedback(Element):
    def __init__(self, elements):
        id = uuid.uuid4().hex[:4]
        self.name = 'fb_' + id
        self.elements = elements

        self.faust = '+~('
        for e in elements:
            self.faust += e.name + ' : '
        self.faust = self.faust[:-3]
        self.faust += ')'

    def get_faust(self):
        string = ''
        for e in self.elements:
            string += e.get_faust()

        string += '{} = {};\n'.format(self.name, self.faust)
        return string
    

#%%
model = Model()

# Simple example
# model.elements.append(Gain(0.5))
# model.elements.append(Delay())

# FIR example
# model.elements.append(Split([[], [Gain(0.5), Delay()], [Gain(-0.2)]]))

# IIR example
model.elements.append(Feedback([Gain(0.5), Delay()]))

model.write_to_file('test_gen.dsp')

#%%
compile_plugin('test_gen')