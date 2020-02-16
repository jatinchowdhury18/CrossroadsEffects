import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
from gen_faust import Model,Element,Gain,UnitDelay,Delay,Split,Feedback
from evolve_structure import create_generation,get_mutated_model
from plugin_utils import compile_plugin

import random
random.seed(0x2345)

def test_generation(model1, model2, num=10):
    models = []
    models.append(model1)
    models.append(model2)
    models = create_generation(models, num, 2)

    for m in models:
        print(m)
        m.write_to_file('test_evolve_gen.dsp')
        compile_plugin('test_evolve_gen', check_success=True)

    return models

def test_success(model1, model2, target_model, num=10, iters=5):
    for _ in range(iters):
        models = test_generation(model1,  model2, num)

        if any(m == target_model for m in models):
            return

    print('Unable to evolve correct structure!')
    exit(1)


print('Test basic')
model1 = Model()
model1.elements.append(Gain())
model2 = Model()
model2.elements.append(UnitDelay())

target = Model()
target.elements.append(Gain())
test_success(model1, model2, target)

print('Test Comb Filter')
model1 = Model()
model1.elements.append(Split([[], [Delay(4), Gain()]]))
model1.elements.append(Gain())
model2 = Model()
model2.elements.append(Split([[], [Delay(5), Gain()]]))

target = Model()
target.elements.append(Split([[], [Delay(5), Gain()]]))
target.elements.append(Gain())
test_success(model1, model2, target, num=15)

print('Test FIR Filter')
model1 = Model()
model1.elements.append(Split([[UnitDelay(),Gain()], [Delay(2),Gain()],
    [Delay(3),Gain()], [Delay(4),Gain()]]))
model2 = Model()
model2.elements.append(Split([[Gain()], [UnitDelay(),Gain()], [Delay(1),Gain()],
    [Delay(3),Gain()], [Delay(4),Gain()]]))

target = Model()
target.elements.append(Split([[Gain()], [UnitDelay(),Gain()], [Delay(2),Gain()],
    [Delay(3),Gain()], [Delay(4),Gain()]]))
test_success(model1, model2, target, num=15, iters=10)

print('Test Multiple Generations')
model1 = Model()
model1.elements.append(Gain())
model2 = Model()
model2.elements.append(UnitDelay())

for _ in range(10):
    models = test_generation(model1,  model2)
    model1, model2 = random.choices(models, k=2)

print('SUCCESS')
