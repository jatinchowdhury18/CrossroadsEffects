#%%
import os
import subprocess

#%%
def compile_plugin(plugin):
    faust_file = 'faust_scripts/' + plugin + '.dsp'
    orig_plugin_file = 'faust_scripts/' + plugin + '.dll'
    cp_plugin_file = 'faust_plugins/' + plugin + '/' + plugin + '.dll'

    p = subprocess.Popen(['faust2w64vst.sh', faust_file],
                         stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    p.wait()
    os.system('rm -rf faust.*')

    os.system('rm -rf faust_plugins' + plugin)
    # os.system('mkdir faust_plugins/' + plugin)

    os.system('mv faust_scripts/' + plugin + '-svg faust_plugins/' + plugin + '/svgs')  
    mv_cmd = 'mv ' + orig_plugin_file + ' ' + cp_plugin_file
    os.system(mv_cmd)

compile_plugin('test')

#%%
def test_plugin(plugin):
    plugin_file = 'faust_plugins/' + plugin + '/' + plugin + '.dll'
    input_wav = 'drums.wav'
    out_wav = 'drums_out.wav'

    runner = 'd:/Documents/CCRMA/Research/AutoEffects/modules/PluginRunner/PluginRunner.exe'

    p = subprocess.Popen([runner, plugin_file, input_wav, out_wav], shell=True)
    p.wait()

test_plugin('test')

