"""
Utility functions for compiling and testing plugins
from a Python model
"""

#%%
import os
import subprocess
from sys import platform
import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt

# %%
def get_platform_specific_args():
    """
    Get correct arguments for the current platform
    """
    vst_script = 'crossroads_scripts/myfaust2faustvst'
    pipe = " > /dev/null 2>&1"
    if platform == "linux" or platform == "linux2": # linux
        runner = 'modules/PluginRunner/PluginRunnerLinux'
        vst_ext = ".so"
    elif platform == "darwin": # OSX
        runner = 'modules/PluginRunner/PluginRunnerMac'
        vst_ext = ".vst"
    elif platform == "win32": # windows
        vst_script = 'crossroads_scripts/faust2w64vst.sh'
        runner = 'modules/PluginRunner/PluginRunner.exe'
        vst_ext = ".dll"
        pipe = " > NUL"
    
    return vst_script, vst_ext, runner, pipe

#%%
def compile_plugin(plugin, check_success=False):
    """
    Compile faust script to a vst plugin.
    Faust script should be located in `faust_scripts/{plugin}.dsp`
    Resulting plugin and svg diagrams will be located in `faust_plugins/{plugin}/`
    """
    vst_script, vst_ext, _, pipe = get_platform_specific_args()

    # set up files
    faust_file = 'faust_scripts/' + plugin + '.dsp'
    orig_plugin_file = 'faust_scripts/' + plugin + vst_ext
    cp_plugin_file = 'faust_plugins/' + plugin + '/' + plugin + vst_ext

    os.system("bash " + vst_script + " " + faust_file + pipe) # run faust2vst bash script
    os.system('rm -rf faust.*') # remove faust residuals

    # clean existing plugin folder (if it exists)
    os.system('rm -rf faust_plugins/' + plugin)
    os.mkdir('faust_plugins/' + plugin)

    # move plugin and svg diagrams to folder
    res = os.system('mv faust_scripts/' + plugin + '-svg faust_plugins/' + plugin + '/svgs', )  
    mv_cmd = 'mv ' + orig_plugin_file + ' ' + cp_plugin_file
    os.system(mv_cmd)

    # if checking for succesful compilation (used for unit tests)
    if res != 0 and check_success:
        exit(res)

# compile_plugin('test')

#%%
def test_plugin(plugin, in_wav, out_wav):
    """
    Test a plugin using the PluginRunner application
    """
    _, vst_ext, runner, pipe = get_platform_specific_args()

    plugin_file = 'faust_plugins/' + plugin + '/' + plugin + vst_ext

    os.system(os.path.realpath(runner) + " " + plugin_file + " " + in_wav + " " + out_wav + pipe)

# test_plugin('test', 'drums.wav', 'drums_out.wav')

# %%
def calc_error(des_wav, out_wav, fs):
    """
    Calculate the error between two wav files,
    using a combination  of mean-squared error
    and spectrogram loss
    """
    mean_square_error = np.mean((des_wav - out_wav)**2, axis=None) # get mean squared error

    nseg = 2048 # hop size

    # sum to mono (maybe do stereo eventually...)
    des = (des_wav[:,0] + des_wav[:,1]) / 2
    out = (out_wav[:,0] + out_wav[:,1]) / 2

    # compute spectrogram error
    _, _, Z_des = signal.stft(des, fs=fs, nperseg=nseg, nfft=nseg*2)
    _, _, Z_out = signal.stft(out, fs=fs, nperseg=nseg, nfft=nseg*2)
    freq_err = np.mean(np.abs(Z_des - Z_out), axis=None)

    return mean_square_error + freq_err
