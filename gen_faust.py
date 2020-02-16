#%%
from abc import ABC, abstractmethod
from plugin_utils import compile_plugin, test_plugin
import uuid
import numpy as np
import matplotlib.pyplot as plt

# %%
def get_uuid():
    return uuid.uuid4().hex[:8]

def trim_elements(elements):
    for idx, e in enumerate(elements):
        if idx == 0:
            continue

        # concatenate gain elements
        if isinstance(e, Gain) and isinstance(elements[idx-1], Gain):
            e.gain *= elements[idx-1].gain
            elements.pop(idx-1)

        # concatenate Unit delays
        elif isinstance(e, UnitDelay) and isinstance(elements[idx-1], UnitDelay):
            elements.insert(idx+1, Delay(2))
            elements.pop(idx)
            elements.pop(idx-1)
            
        # concatenate Delays
        elif isinstance(e, Delay) and isinstance(elements[idx-1], Delay):
            e.length += elements[idx-1].length
            elements.pop(idx-1)

        # concatenate Delay -> Unit Delay
        elif isinstance(e, UnitDelay) and isinstance(elements[idx-1], Delay):
            elements.insert(idx+1, Delay(elements[idx-1].length+1))
            elements.pop(idx)
            elements.pop(idx-1)

        # concatenate UnitDelay -> Delay
        elif isinstance(e, Delay) and isinstance(elements[idx-1], UnitDelay):
            e.length += 1
            elements.pop(idx-1)

#%%
class Model:
    def __init__(self, name=None):
        self.elements = []
        self.name = name

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

    def __str__(self):
        string = '{}: '.format(self.name if self.name is not None else 'Model')
        for e in self.elements:
            string += e.__str__() + ', '
        return string[:-2]

    def __eq__(self, other):
        if len(self.elements) != len(other.elements):
            return False

        for i, e in enumerate(self.elements):
            if type(e) is not type(other.elements[i]):
                return False
            if e != other.elements[i]:
                return False
        return True

    def trim_model(self):
        trim_elements(self.elements)
        for e in self.elements:
            if isinstance(e, Split):
                for chain in e.elements:
                    trim_elements(chain)
                e.update_faust()

            elif isinstance(e, Feedback):
                trim_elements(e.elements)
                e.update_faust()

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

    def get_params(self, params, bounds):
        pass

    def set_params(self, params, idx):
        return idx

class Gain(Element):
    def __init__(self, value=1.0):
        id = get_uuid()
        self.name = 'gain_' + id
        self.gain = value

    def __str__(self):
        return 'Gain({})'.format(self.gain)

    def __eq__(self, other):
        return self.gain == other.gain

    def get_faust(self):
        return '{} = _*{};\n'.format(self.name, self.gain)

    def get_params(self, params, bounds):
        params.append(self.gain)
        bounds.append((-10, 10))

    def set_params(self, params, idx):
        self.gain = params[idx]
        return idx + 1

class UnitDelay(Element):
    def __init__(self):
        id = get_uuid()
        self.name = 'unit_delay_' + id

    def __str__(self):
        return 'UnitDelay'

    def __eq__(self, other):
        return True

    def get_faust(self):
        return '{} = @(1);\n'.format(self.name)

class Delay(Element):
    def __init__(self, length=0):
        id = get_uuid()
        self.name = 'delay_' + id
        self.length = length

    def __str__(self):
        return 'Delay({})'.format(self.length)

    def __eq__(self, other):
        return self.length == other.length

    def get_faust(self):
        return '{} = @({});\n'.format(self.name, int(self.length))

class CubicNL(Element):
    def __init__(self):
        id = get_uuid()
        self.name = 'cubic_' + id

    def __str__(self):
        return 'CubicNL'

    def __eq__(self, other):
        return True

    def get_faust(self):
        return '{} = min(1) : max(-1) : cubic with{{ cubic(x) = x - x*x*x/3; }};\n'.format(self.name)

class Split(Element):
    def __init__(self, elements):
        id = get_uuid()
        self.name = 'split_' + id
        self.elements = elements
        self.update_faust()        

    def update_faust(self):
        self.faust = '_ <: '
        for chain in self.elements:
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

    def __str__(self):
        string = 'Split: ['
        for chain in self.elements:
            if chain == []:
                string += '[], '
                continue

            string += '['
            for e in chain:
                string += e.__str__() + ', '
            string = string[:-2] + '], '
        return string[:-2] + ']'

    def __eq__(self, other):
        if len(self.elements) != len(other.elements):
            return False
        
        for idx, chain in enumerate(self.elements):
            other_chain = other.elements[idx]
            if len(chain) != len(other_chain):
                return False
            
            for i, e in enumerate(chain):
                other_e = other_chain[i]
                if type(e) is not type(other_e):
                    return False
                if e != other_e:
                    return False
        
        return True

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
        self.update_faust()

    def update_faust(self):
        self.faust = '+~'
        if len(self.elements) == 0:
            self.faust += '(_*0)'
        else:
            self.faust += '('
            for e in self.elements:
                self.faust += e.name + ' : '
            self.faust = self.faust[:-3]
            self.faust += ')'

    def __str__(self):
        string = 'Feedback: ['
        for e in self.elements:
            string += e.__str__() + ', '
        return string[:-2] + ']'

    def __eq__(self, other):
        if len(self.elements) != len(other.elements):
            return False
            
        for i, e in enumerate(self.elements):
            other_e = other.elements[i]
            if type(e) is not type(other_e):
                return False
            if e != other_e:
                return False
        
        return True

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


#%%
# model = Model()

# # Simple example
# model.elements.append(Delay(4))
# model.elements.append(Delay(5))
# print(model)
# model.trim_model()
# print(model)
# model.elements.append(Gain(0.5))
# model.elements.append(Delay())

# # FIR example
# model.elements.append(Split([[], [Gain(0.5), Delay()], [Gain(-0.2)]]))

# # IIR example
# model.elements.append(Feedback([Gain(0.5), Delay()]))
# print(model)

#%%
# compile_plugin('test_gen')
# test_plugin('test_gen', 'drums.wav', 'drums_out.wav')
