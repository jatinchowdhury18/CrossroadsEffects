import numpy as np
from gen_faust import Model, get_error_for_model
from tqdm import tqdm

def estimate_params(model, name, in_wav, out_wav, des_wav, tol=1.0e-5):
    """Use Genetic Algorithm to estimate params"""
    N_pop = 50
    N_gens = 10
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
