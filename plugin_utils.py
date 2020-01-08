#%%
import os
import subprocess
from sys import platform

#%%
def compile_plugin(plugin):
    vst_script = 'faust2faustvst'
    if platform == "linux" or platform == "linux2": # linux
        vst_ext = ".so"
    elif platform == "darwin": # OSX
        vst_ext = ".vst"
    elif platform == "win32": # windows
        vst_script = 'faust2w64vst.sh'
        vst_ext = ".dll"

    faust_file = 'faust_scripts/' + plugin + '.dsp'
    orig_plugin_file = 'faust_scripts/' + plugin + vst_ext
    cp_plugin_file = 'faust_plugins/' + plugin + '/' + plugin + vst_ext

    if platform == "linux" or platform == "linux2" or platform == "darwin":
        os.system('faust2svg ' + faust_file)

    if platform == "win32":
        p = subprocess.Popen([vst_script, faust_file],
                         stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        p.wait()
    else:
        os.system(vst_script + " " + faust_file)

    os.system('rm -rf faust.*')

    os.system('rm -rf faust_plugins/' + plugin)
    os.mkdir('faust_plugins/' + plugin)

    os.system('mv faust_scripts/' + plugin + '-svg faust_plugins/' + plugin + '/svgs')  
    mv_cmd = 'mv ' + orig_plugin_file + ' ' + cp_plugin_file
    os.system(mv_cmd)

# compile_plugin('test')

#%%
def test_plugin(plugin, in_wav, out_wav):
    if platform == "linux" or platform == "linux2":
        runner = 'modules/PluginRunner/PluginRunnerLinux'
        vst_ext = ".so"
    elif platform == "darwin": # OSX
        runner = 'modules/PluginRunner/PluginRunnerMac'
        vst_ext = ".vst"
    elif platform == "win32": # Windows
        runner = 'PluginRunner.exe'
        vst_ext = ".dll"

    plugin_file = 'faust_plugins/' + plugin + '/' + plugin + vst_ext

    if platform == "win32":
        os.system("cp -R modules/PluginRunner/" + runner + " .")
        p = subprocess.Popen([runner, plugin_file, in_wav, out_wav], shell=True)
        p.wait()
        os.system("rm -rf " + runner)
    else:
        os.system(runner + " " + plugin_file + " " + in_wav + " " + out_wav)

# test_plugin('test', 'drums.wav', 'drums_out.wav')

