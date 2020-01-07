#%%
import os
import subprocess
from sys import platform

#%%
def compile_plugin(plugin):
    faust_file = 'faust_scripts/' + plugin + '.dsp'
    orig_plugin_file = 'faust_scripts/' + plugin + '.dll'
    cp_plugin_file = 'faust_plugins/' + plugin + '/' + plugin + '.dll'

    vst_script = 'faust2faustvst'
    if platform == "linux" or platform == "linux2": # linux
        vst_script = 'faust2faustvst'
    elif platform == "darwin": # OSX
        vst_script = 'faust2faustvst'
    elif platform == "win32": # Windows
        vst_script = 'faust2w64vst.sh'

    p = subprocess.Popen([vst_script, faust_file],
                         stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    p.wait()
    os.system('rm -rf faust.*')

    os.system('rm -rf faust_plugins/' + plugin)
    os.mkdir('faust_plugins/' + plugin)

    os.system('mv faust_scripts/' + plugin + '-svg faust_plugins/' + plugin + '/svgs')  
    mv_cmd = 'mv ' + orig_plugin_file + ' ' + cp_plugin_file
    os.system(mv_cmd)

# compile_plugin('test')

#%%
def test_plugin(plugin, in_wav, out_wav):
    plugin_file = 'faust_plugins/' + plugin + '/' + plugin + '.dll'

    runner = 'd:/Documents/CCRMA/Research/AutoEffects/modules/PluginRunner/PluginRunner.exe'

    p = subprocess.Popen([runner, plugin_file, in_wav, out_wav], shell=True)
    p.wait()

# test_plugin('test', 'drums.wav', 'drums_out.wav')

