"""
Estimate the optimal parameters for a signal processing
model to recreate the target audio
"""

import numpy as np
from scipy.io import wavfile
from gen_faust import Model
from plugin_utils import compile_plugin, test_plugin, calc_error
from tqdm import tqdm
import os
from sys import platform
from scipy.optimize import minimize

# If you don't want to use libsndfile, set this to False
USING_LIBSNDFILE=True

def optimize_model(model, name, in_wav, out_wav, des_wav, tol=1.0e-5):
    """
    Estimate parameters for a model using L-BFGS-B algorithm
    """
    params, bounds = model.get_params()
    if params == []:
        return params

    result = minimize(get_error_for_model, params, args=(model,name,in_wav,out_wav,des_wav), tol=tol,
                      bounds=bounds, options={'maxiter': 30, 'eps': 1e-06, 'ftol': 1e-11, 'iprint': 1})
    return result.x

def get_error_for_model(params, model, name, in_wav, out_wav, des_wav):
    """
    Calculate error for a model and parameters, by compiling to a faust2sndfile executable
    plugin, running audio through, and comparing the output audio with the desired
    """
    # fallback to vs version if libsndfile not available
    if platform == "win32" or USING_LIBSNDFILE == False:
        return get_error_for_model_vst(params, model, name, in_wav, out_wav, des_wav)

    model.set_params(params)
    model.write_to_file(name + '.dsp')

    # compile faust script toa faust2sndfile executable
    os.system('faust -i -a crossroads_scripts/faust_mysndfile.cpp faust_scripts/{0}.dsp -o {0}-sndfile.cpp'.format(name))
    os.system('g++ -std=c++11 {0}-sndfile.cpp -o {0}-sndfile -lsndfile'.format(name))
    os.system('./{}-sndfile {} {}'.format(name, in_wav, out_wav))
    os.system('rm {0}-sndfile; rm {0}-sndfile.cpp'.format(name))

    # read wav files
    fs, y = wavfile.read(des_wav)
    fs, y_test = wavfile.read(out_wav)

    # normalize for wav files
    y = y / 2**15 if np.max(np.abs(y)) > 10 else y
    y_test = y_test / 2**15 if np.max(np.abs(y_test)) > 10 else y_test

    return calc_error(y, y_test, fs)


def get_error_for_model_vst(params, model, name, in_wav, out_wav, des_wav):
    """
    Calculate error for a model and parameters, by compiling to a VST
    plugin, running audio through, and comparing the output audio with the desired
    """
    # compile and test plugin
    model.set_params(params)
    model.write_to_file(name + '.dsp')
    compile_plugin(name)
    test_plugin(name, in_wav, out_wav)

    # read wav files
    fs, y = wavfile.read(des_wav)
    fs, y_test = wavfile.read(out_wav)

    # normalize for wav files
    y = y / 2**15 if np.max(np.abs(y)) > 10 else y
    y_test = y_test / 2**15 if np.max(np.abs(y_test)) > 10 else y_test

    return calc_error(y, y_test, fs)


####################################################
# Old genetic algorithm code... not currently in use
def estimate_params(model, name, in_wav, out_wav, des_wav, tol=1.0e-5):
    """Use Genetic Algorithm to estimate params [DEPRECATED]"""
    N_pop = 100
    N_gens = 30
    N_survive = 2

    params, bounds = model.get_params()

    # create initial generation
    generation = []
    for n in range(N_pop):
        generation.append(init_rand_params(params, bounds))

    gen_num = 0
    converge = False
    while gen_num < N_gens:
        # test current generation
        print('Testing generation: {}'.format(gen_num))
        errors = np.zeros(N_pop)
        for n in tqdm(range(N_pop)):
            errors[n] = get_error_for_model(generation[n], model, name, in_wav, out_wav, des_wav)
        
        # sort
        aridxs = np.argsort(errors)
        errors = errors[aridxs]
        generation = [generation[i] for i in aridxs]

        # Take N_survive best
        errors = errors[:N_survive]
        generation = generation[:N_survive]

        # print('Best error: {}'.format(errors[0]))
        # print('Best params: {}'.format(generation[0]))

        print('Surviving errors: {}'.format(errors[:N_survive]))
        print('Surviving params: {}'.format(generation[:N_survive]))

        # check for correct answer
        if errors[0] <= tol:
            converge = True
            break

        # mutate off survivors
        for n in range(N_survive, N_pop):
            generation.append(mutate_params(generation[n % N_survive], bounds, gen_num, N_gens))

        gen_num += 1
    
    if converge:
        print('Converged!')
    else:
        print('Not Converged')

    print('Best error: {}'.format(errors[0]))
    print('Best params: {}'.format(generation[0]))

    # return best params
    return generation[0]


def init_rand_params(params, bounds):
    """Initialize a random set of parameters"""
    new_params = np.zeros(np.shape(params))
    for i in range(len(params)):
        stddev = bounds[i][1] - bounds[i][0]
        mean = (bounds[i][0] + bounds[i][1]) / 2
        new_params[i] = np.clip(np.random.normal(mean, stddev), bounds[i][0], bounds[i][1])

    return new_params

def mutate_params(parent_params, bounds, gen_num, N_gens):
    """Mutate on a set of parameters"""
    new_params = np.zeros(np.shape(parent_params))
    for i in range(len(parent_params)):
        stddev = (bounds[i][1] - bounds[i][0]) * (1 - (gen_num / N_gens))**gen_num
        mean = parent_params[i]
        new_params[i] = np.clip(np.random.normal(mean, stddev), bounds[i][0], bounds[i][1])

    return new_params
