import json
import networkx as nx
import textwrap
from functools import lru_cache
import concurrent.futures
import hashlib
import subprocess
from tqdm import tqdm
from graph import visualize_graph as dg


def check_assumption_1(node_positions, trustsets):
    for trustset in trustsets:
        if not trustset.issubset(node_positions.keys()):
            missing_nodes = trustset - node_positions.keys()
            error_message = textwrap.indent(textwrap.dedent(f"""
                Not all members of all trustsets are graph nodes.

                Nodes {missing_nodes} in trustset {trustset} are not in simulation.
            """), ' ' * 4)
            return False, error_message

    return True, None


def check_assumption_2(trustsets, malicious_nodes):
    for trustset in trustsets:
        if trustset.issubset(malicious_nodes):
            error_message = textwrap.indent(textwrap.dedent(f"""
                There is at least one pure malicious trustset.

                Trustset {trustset} has no honest nodes.
                Malicious nodes: {malicious_nodes}
            """), ' ' * 4)
            return False, error_message

    return True, None


def check_assumption_3(trustsets, malicious_nodes):
    for trustset in trustsets:
        if trustset.isdisjoint(malicious_nodes):
            return True, None

    error_message = textwrap.indent(textwrap.dedent(f"""
        There is no pure honest trustset.

        Malicious nodes: {malicious_nodes}
    """), ' ' * 4)
    return False, error_message


def check_assumption_4(node_states, trustsets, malicious_nodes, t_rep):
    honest_nodes = set(node_states.keys()) - malicious_nodes
    fully_honest_nodes = set().union(*{trustset for trustset in trustsets if trustset.isdisjoint(malicious_nodes)})

    for node in honest_nodes:
        messages = node_states[node]['tx']
        for message in messages:
            attestations = message['attestations']
            if not any(attestation['attest_node'] in fully_honest_nodes for attestation in attestations):
                json_message = json.dumps(message, indent=2)
                json_message_indented = textwrap.indent(json_message, ' ' * 4)
                error_message = "\n" + textwrap.indent(textwrap.dedent(f"""
                    Not every honest node is connected to at least one pure honest trustset.

                    Node {node} did not receive any attestations from a pure honest trustset for message {message['message_num']}.
                    Fully honest nodes: {fully_honest_nodes}
                    Malicious nodes: {malicious_nodes}
                """).strip(), ' ' * 4) + f"\n{json_message_indented}\n"
                return False, error_message

    return True, None


def check_assumption_5(G, trustsets, malicious_nodes):
    trustset_list = list(trustsets)
    valid_nodes = {}

    def contains_honest_member(path, trustset):
        return any(node in trustset and node not in malicious_nodes for node in path)  # Can reverse the logic for optimisatiob

    def cache_key(*args):
        return hashlib.md5(json.dumps(args, sort_keys=True).encode()).hexdigest()

    @lru_cache(maxsize=None)
    def cached_has_path(source, target):
        return nx.has_path(G, source, target)

    @lru_cache(maxsize=None)
    def cached_all_simple_paths(source, target):
        return list(nx.all_simple_paths(G, source, target))

    tqdm_disable = False
    for i in tqdm(range(len(trustset_list)), disable=tqdm_disable, desc="Outer Trustsets"):
        for j in tqdm(range(len(trustset_list)), disable=tqdm_disable, desc="Inner Trustsets", leave=True):
            if i != j:
                C1 = trustset_list[i]
                C2 = trustset_list[j]

                valid_node_found = False  # Rename to valid c1
                for c1 in tqdm(C1, disable=tqdm_disable, desc="Nodes in C1    ", leave=False):
                    all_paths_valid = True

                    paths = set()
                    for P in tqdm(G.nodes(), disable=tqdm_disable, desc="Source Node    ", leave=False):               
                        if P == c1:
                            continue

                        if cached_has_path(P, c1):
                            for path in cached_all_simple_paths(P, c1):
                                if not contains_honest_member(path, C2):
                                    all_paths_valid = False
                                    break

                                paths.add((path[0], path[-1]))

                            if not all_paths_valid:
                                break

                    if all_paths_valid:
                        valid_node_found = True
                        valid_nodes[(i, j)] = {c1: paths}
                        break

                if not valid_node_found:
                    valid_nodes[(i, j)] = None
                    dg(G, C1, C2)
                    return False, valid_nodes

    return True, valid_nodes


def check_assumption_5_cpp(G, trustsets, malicious_nodes):
    # subprocess.run(['./c++/clean_build.sh'], check=True)
    
    data_path = "c++/data.json"
    executable_path = "c++/build/Assumption5"
    
    data = {
        "nodes": list(G.nodes),
        "edges": list(G.edges),
        "trustsets": [list(ts) for ts in trustsets],
        "malicious_nodes": list(malicious_nodes)
    }

    with open(data_path, 'w') as f:
        json.dump(data, f)

    process = subprocess.Popen([executable_path, data_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    for stdout_line in iter(process.stdout.readline, ""):
        print(stdout_line.strip())
    process.stdout.close()
    
    stderr = process.communicate()[1]
    if stderr:
        print(stderr)
    
    with open("c++/valid_nodes.json", 'r') as f:
        valid_nodes_cpp = json.load(f)

    valid_nodes = {}
    for i, outer_dict in valid_nodes_cpp.items():
        i = int(i)
        for j, inner_dict in outer_dict.items():
            j = int(j)
            for c1, paths in inner_dict.items():
                c1 = int(c1)
                if (i, j) not in valid_nodes:
                    valid_nodes[(i, j)] = {}
                valid_nodes[(i, j)][c1] = set((path[0], path[1]) for path in paths)

    return None, valid_nodes


def check_assumption_6(node_states, trustsets, malicious_nodes, t_rep):
    honest_nodes = set(node_states.keys()) - malicious_nodes

    for node in malicious_nodes:
        messages = node_states[node]['tx']
        for message in messages:
            attestations = message['attestations']
            for trustset in trustsets:
                if not any(attestation['attest_node'] in (trustset & honest_nodes) for attestation in attestations):
                    json_message = json.dumps(message, indent=2)
                    json_message_indented = textwrap.indent(json_message, ' ' * 4)
                    error_message = "\n" + textwrap.indent(textwrap.dedent(f"""
                        Not every malicious node is connected to at least one honest node from each trustset.

                        Malicious node {node} did not receive any attestations from honest nodes in trustset {trustset} for message {message['message_num']}.
                    """).strip(), ' ' * 4) + f"\n{json_message_indented}\n"
                    return False, error_message

    return True, None
