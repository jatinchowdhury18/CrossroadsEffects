import numpy as np
from gen_faust import Model,Element,Gain,UnitDelay,Split
from param_estimation import estimate_params,get_error_for_model,optimize_model
from tqdm import tqdm
import random
import copy

def get_evolved_structure(plugin,dry_file,wet_file,des_file, tol=1e-5):
    N_pop = 6
    N_gens = 5
    N_survive = 2

    # create initial model parents
    models = []
    
    model1 = Model()
    model1.elements.append(Gain())
    models.append(model1)

    model2 = Model()
    model2.elements.append(UnitDelay())
    models.append(model2)

    # create initial generation
    models = create_generation(models, N_pop)

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

        # Take survivors
        errors = errors[:N_survive]
        models = models[:N_survive]

        print('Surviving errors: {}'.format(errors))

        # check for correct answer
        if errors[0] <= tol:
            converge = True
            break

        # mutate off survivors
        create_generation(models, N_pop)

        gen_num += 1

    if converge:
        print('Converged!')
    else:
        print('Not Converged')

    print('Best error: {}'.format(errors[0]))

    return models[0]


def create_generation(models, N):
    """create a generation of models from first two in existing list"""
    while len(models) < N:
        models.append(get_mutated_model(models[0],models[1]))

        # check for duplicates
        for m in models[:-1]:
            if m == models[-1]:
                print('Duplicate detected! Mutating again...')
                models.pop()
                break

    return models


mutation_strategies = ['concat_series', 'concat_parallel', 'add_series', 'add_parallel', 'add_to_split']

def get_mutated_model(parent1, parent2):
    """Create a new model by mutating existing models"""

    strategy = random.choice(mutation_strategies)
    new_model = Model()

    print('Mutating with strategy: ' + strategy)

    if strategy == 'concat_series':
        if bool(random.getrandbits(1)):
            new_model.elements = copy.deepcopy(parent1.elements) + copy.deepcopy(parent2.elements)
        else:
            new_model.elements = copy.deepcopy(parent2.elements) + copy.deepcopy(parent1.elements)

    elif strategy == 'concat_parallel':
        new_model.elements.append(Split([copy.deepcopy(parent1.elements), copy.deepcopy(parent2.elements)]))

    elif strategy == 'add_series':
        parent_to_add = random.choice([parent1, parent2])
        element_to_add = random.choice([Gain(), UnitDelay()])
        new_model.elements = copy.deepcopy(parent_to_add.elements)
        new_model.elements.append(element_to_add)

    elif strategy == 'add_parallel':
        parent_to_add = random.choice([parent1, parent2])
        element_to_add = random.choice([Gain(), UnitDelay()])

        start_idx = random.randint(0, len(parent_to_add.elements))
        end_idx = random.randint(start_idx, len(parent_to_add.elements))

        new_model.elements = copy.deepcopy(parent_to_add.elements[:start_idx])
        new_model.elements.append(Split([copy.deepcopy(parent_to_add.elements[start_idx:end_idx]), [element_to_add]]))
        new_model.elements += copy.deepcopy(parent_to_add.elements[end_idx:])

    elif strategy == 'add_to_split':
        parent_to_add = random.choice([parent1, parent2])
        element_to_add = random.choice([Gain(), UnitDelay()])

        split_idxs = []
        for idx, e in enumerate(parent_to_add.elements):
            if isinstance(e, Split):
                split_idxs.append(idx)
        
        if split_idxs == []:
            idx = random.randint(0, len(parent_to_add.elements))
            new_model.elements = copy.deepcopy(parent_to_add.elements[:idx])
            new_model.elements.append(Split([[], [element_to_add]]))
            new_model.elements += copy.deepcopy(parent_to_add.elements[idx:])
        else:    
            new_model.elements = copy.deepcopy(parent_to_add.elements)
            split = new_model.elements[random.choice(split_idxs)]
            add_element_to_split (split, element_to_add)

    else:
        print('Warning: unknown mutation strategy selected')
        new_model.elements.append(UnitDelay())    

    new_model.trim_model()

    return new_model


def add_element_to_split(split, element):
    chain = random.choice(split.elements)

    if chain == []:
        chain.append(element)
        return

    chain_e = random.choice(chain)
    if (isinstance(chain_e, Split)):
        add_element_to_split(chain_e, element)
        return

    split_idx = random.randint(0, len(chain))
    chain.insert(split_idx, element)
