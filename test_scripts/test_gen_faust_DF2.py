import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
from gen_faust import Model,Element,Gain,Delay,Split,Feedback
from plugin_utils import compile_plugin, test_plugin

# Create model
model = Model()
model.elements.append(Feedback([Delay(), Split([[Gain(0.5)], [Delay(), Gain(0.8)]])]))
model.elements.append(Split([[Gain(0.2)], [Delay(), Split([[Gain(0.2)], [Delay(), Gain(-0.1)]])]]))

# Write to file and compile
model.write_to_file('test_DF2.dsp')
compile_plugin('test_DF2')

# Test
test_plugin('test_gen', 'drums.wav', 'drums_out.wav')
