import numpy as np
from gen_faust import Model,Element,Gain,UnitDelay,Delay,CubicNL,Split,Feedback
from param_estimation import estimate_params,get_error_for_model,optimize_model
from plugin_utils import compile_plugin, test_plugin
from tqdm import tqdm
import random
import os

def get_evolved_structure(plugin,dry_file,wet_file,des_file, tol=1e-5):
    N_pop = 16
    N_gens = 5
    N_survive = 3

    res = os.system('mkdir {}'.format(plugin))
    if (res > 0):
        exit(res)

    # create initial model parents
    models = []
    
    model1 = Model()
    model1.elements.append(Gain())
    models.append(model1)

    model2 = Model()
    model2.elements.append(UnitDelay())
    models.append(model2)

    model3 = Model()
    model3.elements.append(Split([[Gain()], [UnitDelay(), Gain()]]))
    models.append(model3)

    # create initial generation
    models = create_generation(models, N_pop, N_survive)

    gen_num = 0
    converge = False
    while gen_num < N_gens:
        # test current generation
        print('Testing generation: {}'.format(gen_num))
        for n in range(N_pop):
            print(models[n])

        errors = np.zeros(N_pop)
        for n in tqdm(range(N_pop)):
            print(models[n])
            params = optimize_model(models[n],plugin,dry_file,wet_file,des_file, tol=tol)
            models[n].set_params(params)
            errors[n] = get_error_for_model(params,models[n],plugin,dry_file,wet_file,des_file)

            # if errors[n] < tol / 2: # really fast convergence
            #     print('Converged!')
            #     return models[n]

        # sort
        aridxs = np.argsort(errors)
        errors = errors[aridxs]
        models = [models[i] for i in aridxs]

        for n in range(N_survive):
            models[n].write_to_file(plugin + '.dsp')
            compile_plugin(plugin)
            os.system('cp -R faust_plugins/{} {}/gen{}_{}'.format(plugin, plugin, gen_num, n))
            os.system('cp faust_scripts/{}.dsp {}/gen{}_{}/'.format(plugin, plugin, gen_num, n))

        # Take survivors
        errors = errors[:N_survive]
        models = models[:N_survive]

        print('Surviving errors: {}'.format(errors))

        # check for correct answer
        if errors[0] <= tol:
            converge = True
            break

        # mutate off survivors
        create_generation(models, N_pop, N_survive)

        gen_num += 1

    if converge:
        print('Converged!')
    else:
        print('Not Converged')

    print('Best error: {}'.format(errors[0]))

    models[0].write_to_file(plugin + '.dsp')
    compile_plugin(plugin)
    test_plugin(plugin, dry_file, wet_file)
    os.system('cp -R faust_plugins/{} {}/gen_final'.format(plugin, plugin))
    os.system('cp faust_scripts/{}.dsp {}/gen_final/'.format(plugin, plugin))

    return models[0]


def create_generation(models, N, N_survive):
    """create a generation of models from first two in existing list"""
    while len(models) < N:
        parent1 = random.choice(models[:N_survive])
        parent2 = random.choice(models[:N_survive])
        models.append(get_mutated_model(parent1, parent2))

        # check for duplicates
        for m in models[:-1]:
            if m == models[-1]:
                print('Duplicate detected! Mutating again...')
                models.pop()
                break

    return models


mutation_strategies = ['concat_series', 'concat_parallel', 'add_gain', 'add_delay', 'add_nl', 'add_split', 'add_chain']

def get_mutated_model(parent1, parent2):
    """Create a new model by mutating existing models"""

    strategy = random.choice(mutation_strategies)
    new_model = Model()

    print('Mutating with strategy: ' + strategy)

    if strategy == 'concat_series':
        if bool(random.getrandbits(1)):
            new_model.elements = copy_elements(parent1.elements) + copy_elements(parent2.elements)
        else:
            new_model.elements = copy_elements(parent2.elements) + copy_elements(parent1.elements)

    elif strategy == 'concat_parallel':
        new_model.elements.append(Split([copy_elements(parent1.elements), copy_elements(parent2.elements)]))

    elif strategy == 'add_gain':
        parent_to_add = random.choice([parent1, parent2])
        new_model.elements = copy_elements(parent_to_add.elements)
        add_element(new_model, Gain())

    elif strategy == 'add_delay':
        parent_to_add = random.choice([parent1, parent2])
        new_model.elements = copy_elements(parent_to_add.elements)
        add_element(new_model, UnitDelay())

    elif strategy == 'add_nl':
        parent_to_add = random.choice([parent1, parent2])
        new_model.elements = copy_elements(parent_to_add.elements)
        add_element(new_model, CubicNL())

    elif strategy == 'add_split':
        parent_to_add = random.choice([parent1, parent2])
        new_model.elements = copy_elements(parent_to_add.elements)
        add_element(new_model, Split([[Gain()], [UnitDelay(), Gain()]]))

    elif strategy == 'add_chain':
        parent_to_add = random.choice([parent1, parent2])
        new_model.elements = copy_elements(parent_to_add.elements)

        split_idxs = []
        for i, e in enumerate(new_model.elements):
            if isinstance(e, Split):
                split_idxs.append(i)
        
        if split_idxs == []:
            print('No Splits to add to! Mutating again...')
            return get_mutated_model(parent1, parent2)

        split_idx = random.choice(split_idxs)
        new_model.elements[split_idx].elements.append([UnitDelay(), Gain()])


    else:
        print('Warning: unknown mutation strategy selected')
        new_model.elements.append(UnitDelay())    

    new_model.trim_model()

    return new_model


def copy_elements(elements):
    new_elements = []
    for e in elements:
        if isinstance(e, Gain):
            new_elements.append(Gain())
        elif isinstance(e, UnitDelay):
            new_elements.append(UnitDelay())
        elif isinstance(e, Delay):
            new_elements.append(Delay(e.length))
        elif isinstance(e, Split):
            chains = []
            for chain in e.elements:
                chains.append(copy_elements(chain))
            new_elements.append(Split(chains))
        elif isinstance(e, Feedback):
            fb_elements = copy_elements(e.elements)
            new_elements.append(Feedback(fb_elements))

    return new_elements

def add_element(model, element_to_add):
    chains = [model.elements]
    for e in model.elements:
        if isinstance(e, Split):
            for chain in e.elements:
                chains.append(chain)
    
    chain_to_add_to = random.choice(chains)
    chain_to_add_to.insert(random.randint(0, len(chain_to_add_to)), element_to_add)
