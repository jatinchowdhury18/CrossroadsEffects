"""
Test model utilities including equality and trimming
"""

import os,sys
sys.path.append(os.path.abspath('crossroads_scripts'))
from gen_faust import *

##########################################
print('Testing Model Equality: types')
model1 = Model()
model1.elements.append(Gain())
model2 = Model()
model2.elements.append(Delay())
assert (model1 == model2) == False, 'Type equality incorrect!'

##########################################
print('Testing Model Equality: gain values')
# False example
model1 = Model()
model1.elements.append(Gain(1.0))
model2 = Model()
model2.elements.append(Gain(2.0))
assert (model1 == model2) == False, 'Gain equality incorrect!'
# True example
model1 = Model()
model1.elements.append(Gain(2.0))
model2 = Model()
model2.elements.append(Gain(2.0))
assert (model1 == model2) == True, 'Gain equality incorrect!'

##########################################
print('Testing Model Equality: unit delays')
model1 = Model()
model1.elements.append(UnitDelay())
model2 = Model()
model2.elements.append(UnitDelay())
assert (model1 == model2) == True, 'Unit Delay equality incorrect!'

##########################################
print('Testing Model Equality: delays')
# False example
model1 = Model()
model1.elements.append(Delay(10))
model2 = Model()
model2.elements.append(Delay(20))
assert (model1 == model2) == False, 'Delay equality incorrect!'
# True example
model1 = Model()
model1.elements.append(Delay(20))
model2 = Model()
model2.elements.append(Delay(20))
assert (model1 == model2) == True, 'Delay equality incorrect!'

##########################################
print('Testing Model Equality: split (# chains)')
model1 = Model()
model1.elements.append(Split([[]]))
model2 = Model()
model2.elements.append(Split([[], []]))
assert (model1 == model2) == False, 'Split (# chains) equality incorrect!'

##########################################
print('Testing Model Equality: split (# elements in chain)')
model1 = Model()
model1.elements.append(Split([[], [Gain()]]))
model2 = Model()
model2.elements.append(Split([[], []]))
assert (model1 == model2) == False, 'Split (# elements in chain) equality incorrect!'

##########################################
print('Testing Model Equality: split (elements)')
# False example: wrong type
model1 = Model()
model1.elements.append(Split([[], [Gain()]]))
model2 = Model()
model2.elements.append(Split([[], [Delay()]]))
assert (model1 == model2) == False, 'Split (elements) equality incorrect!'
# False example: wrong values
model1 = Model()
model1.elements.append(Split([[], [Gain(1.0)]]))
model2 = Model()
model2.elements.append(Split([[], [Gain(2.0)]]))
assert (model1 == model2) == False, 'Split (elements) equality incorrect!'
# True example
model1 = Model()
model1.elements.append(Split([[], [Delay(), Gain()]]))
model2 = Model()
model2.elements.append(Split([[], [Delay(), Gain()]]))
assert (model1 == model2) == True, 'Split (elements) equality incorrect!'

##########################################
print('Testing Model Equality: split (recursive)')
# False example
model1 = Model()
model1.elements.append(Split([[], [Gain(), Split([[], [Gain()]])]]))
model2 = Model()
model2.elements.append(Split([[], [Gain(), Split([[Gain()], [Gain()]])]]))
assert (model1 == model2) == False, 'Split (elements) equality incorrect!'
# True example
model1 = Model()
model1.elements.append(Split([[], [Gain(), Split([[Delay()], [Gain()]])]]))
model2 = Model()
model2.elements.append(Split([[], [Gain(), Split([[Delay()], [Gain()]])]]))
assert (model1 == model2) == True, 'Split (elements) equality incorrect!'

##########################################
print('Testing Model Equality: feedback (# elements)')
model1 = Model()
model1.elements.append(Feedback([UnitDelay()]))
model2 = Model()
model2.elements.append(Feedback([UnitDelay(), Gain()]))
assert (model1 == model2) == False, 'Feedback (# elements) equality incorrect!'

##########################################
print('Testing Model Equality: feedback (elements)')
# False example: types
model1 = Model()
model1.elements.append(Feedback([UnitDelay()]))
model2 = Model()
model2.elements.append(Feedback([Gain()]))
assert (model1 == model2) == False, 'Feedback (elements) equality incorrect!'

# False example: values
model1 = Model()
model1.elements.append(Feedback([Gain(1.0)]))
model2 = Model()
model2.elements.append(Feedback([Gain(2.0)]))
assert (model1 == model2) == False, 'Feedback (elements) equality incorrect!'

# True example
model1 = Model()
model1.elements.append(Feedback([Delay(2), Gain(2.0)]))
model2 = Model()
model2.elements.append(Feedback([Delay(2), Gain(2.0)]))
assert (model1 == model2) == True, 'Feedback (elements) equality incorrect!'

##########################################
print('Testing Model Equality: feedback (recursive)')
# False example
model1 = Model()
model1.elements.append(Feedback([UnitDelay(), Feedback([Gain()])]))
model2 = Model()
model2.elements.append(Feedback([UnitDelay(), Feedback([])]))
assert (model1 == model2) == False, 'Feedback (recursive) equality incorrect!'

# True example
model1 = Model()
model1.elements.append(Feedback([UnitDelay(), Feedback([UnitDelay()])]))
model2 = Model()
model2.elements.append(Feedback([UnitDelay(), Feedback([UnitDelay()])]))
assert (model1 == model2) == True, 'Feedback (recursive) equality incorrect!'

##########################################
print('Testing Model Trim: do nothing')
model1 = Model()
model1.elements.append(Gain(0.5))
model1.elements.append(Delay(10))
model1.trim_model()
model2 = Model()
model2.elements.append(Gain(0.5))
model2.elements.append(Delay(10))
assert model1 == model2, 'Trim (do nothing) incorrect!'

##########################################
print('Testing Model Trim: gain')
model1 = Model()
model1.elements.append(Gain(0.5))
model1.elements.append(Gain(2.0))
model1.trim_model()
model2 = Model()
model2.elements.append(Gain(1.0))
assert model1 == model2, 'Trim (gain) incorrect!'

##########################################
print('Testing Model Trim: delays')
# UnitDelay->UnitDelay
model1 = Model()
model1.elements.append(UnitDelay())
model1.elements.append(UnitDelay())
model1.trim_model()
model2 = Model()
model2.elements.append(Delay(2))
assert model1 == model2, 'Trim (delays) incorrect!'

# Delay->Delay
model1 = Model()
model1.elements.append(Delay(10))
model1.elements.append(Delay(90))
model1.trim_model()
model2 = Model()
model2.elements.append(Delay(100))
assert model1 == model2, 'Trim (delays) incorrect!'

# UnitDelay->Delay
model1 = Model()
model1.elements.append(UnitDelay())
model1.elements.append(Delay(9))
model1.trim_model()
model2 = Model()
model2.elements.append(Delay(10))
assert model1 == model2, 'Trim (delays) incorrect!'

# Delay->UnitDelay
model1 = Model()
model1.elements.append(Delay(9))
model1.elements.append(UnitDelay())
model1.trim_model()
model2 = Model()
model2.elements.append(Delay(10))
assert model1 == model2, 'Trim (delays) incorrect!'

##########################################
print('Testing Model Trim: split')
model1 = Model()
model1.elements.append(Delay(9))
model1.elements.append(Split([[Gain(2.0)], [Gain(0.5), Gain(2.0), Delay(2), Gain(3.0), UnitDelay(), Delay(2)]]))
model1.trim_model()
model2 = Model()
model2.elements.append(Delay(8))
model2.elements.append(UnitDelay())
model2.elements.append(Split([[Gain(4.0), Gain(0.5)], [Gain(1.0), UnitDelay(), UnitDelay(), Gain(1.5), Gain(2.0), Delay(3)]]))
model2.trim_model()
assert model1 == model2, 'Trim (split) incorrect!'

##########################################
print('Testing Model Trim: feedback')
model1 = Model()
model1.elements.append(Delay(9))
model1.elements.append(Feedback([Gain(0.5), Gain(2.0), Delay(2), Gain(3.0), UnitDelay(), Delay(2)]))
model1.trim_model()
model2 = Model()
model2.elements.append(Delay(8))
model2.elements.append(UnitDelay())
model2.elements.append(Feedback([Gain(1.0), UnitDelay(), UnitDelay(), Gain(1.5), Gain(2.0), Delay(3)]))
model2.trim_model()
assert model1 == model2, 'Trim (feedback) incorrect!'

print('SUCCESS')
