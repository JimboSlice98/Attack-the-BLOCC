import itertools
import random


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


def create_malicious_parties(node_positions, num_malicious):
    node_ids = list(node_positions.keys())
    
    if num_malicious > len(node_ids):
        raise ValueError("Number of malicious nodes cannot exceed the total number of nodes")
    
    malicious_nodes = set(random.sample(node_ids, num_malicious))
    
    return malicious_nodes

