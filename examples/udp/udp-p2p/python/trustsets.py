import itertools
import random
import json


def create_trustsets(node_positions, fraction=2/3, allow_overlap=True):
    node_ids = list(node_positions.keys())
    total_nodes = len(node_ids)
    trustset_size = int(total_nodes * fraction)

    trustsets = set()

    if allow_overlap:
        for combination in itertools.combinations(node_ids, trustset_size):
            trustsets.add(frozenset(combination))
    else:
        random.shuffle(node_ids)
        for i in range(0, total_nodes, trustset_size):
            trustset = node_ids[i:i+trustset_size]
            if len(trustset) == trustset_size:
                trustsets.add(frozenset(trustset))
    
    # trustsets.add(frozenset([34, 2, 4]))
    return trustsets


def trustset_generator_factory(node_positions, fraction=2/3):
    def generator():
        node_ids = list(node_positions.keys())
        total_nodes = len(node_ids)
        trustset_size = int(total_nodes * fraction)

        for combination in itertools.combinations(node_ids, trustset_size):
            yield frozenset(combination)
            
    return generator



def create_malicious_parties(node_positions, num_malicious):
    node_ids = list(node_positions.keys())
    
    if num_malicious > len(node_ids):
        raise ValueError("Number of malicious nodes cannot exceed the total number of nodes")
    
    malicious_nodes = set(random.sample(node_ids, num_malicious))
    
    return malicious_nodes


def save_trustsets(trustsets, filename='trustsets.json'):
    trustsets_list = [list(trustset) for trustset in trustsets]
    with open(filename, 'w') as f:
        json.dump(trustsets_list, f)


def load_trustsets(filename='trustsets.json'):
    with open(filename, 'r') as f:
        trustsets_list = json.load(f)
    trustsets = set(frozenset(trustset) for trustset in trustsets_list)
    return trustsets
