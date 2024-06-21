import json
import networkx as nx
import textwrap
from functools import lru_cache
from collections import deque
import hashlib
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


# def check_assumption_5_nx(G, trustsets, malicious_nodes):
#     trustset_list = list(trustsets)
#     valid_nodes = {}

#     def contains_honest_member(path, trustset):
#         return any(node in trustset and node not in malicious_nodes for node in path)  # Can reverse the logic for optimisatiob

#     def cache_key(*args):
#         return hashlib.md5(json.dumps(args, sort_keys=True).encode()).hexdigest()

#     @lru_cache(maxsize=None)
#     def cached_has_path(P, target):
#         return nx.has_path(G, P, target)

#     @lru_cache(maxsize=None)
#     def cached_all_simple_paths(P, target):
#         return list(nx.all_simple_paths(G, P, target))

#     tqdm_disable = False
#     for i in tqdm(range(len(trustset_list)), disable=tqdm_disable, desc="Outer Trustsets"):
#         for j in tqdm(range(len(trustset_list)), disable=tqdm_disable, desc="Inner Trustsets", leave=True):
#             if i != j:
#                 C1 = trustset_list[i]
#                 C2 = trustset_list[j]

#                 valid_c1_found = False
#                 for c1 in tqdm(C1, disable=tqdm_disable, desc="Nodes in C1    ", leave=False):
#                     all_paths_valid = True

#                     paths = set()
#                     for P in tqdm(G.nodes(), disable=tqdm_disable, desc="Source Node    ", leave=False):               
#                         if P == c1:
#                             continue

#                         if cached_has_path(P, c1):
#                             for path in cached_all_simple_paths(P, c1):
#                                 if not contains_honest_member(path, C2):
#                                     all_paths_valid = False
#                                     break

#                                 paths.add((path[0], path[-1]))

#                             if not all_paths_valid:
#                                 break

#                     if all_paths_valid:
#                         valid_c1_found = True
#                         valid_nodes[(i, j)] = {c1: paths}
#                         break

#                 if not valid_c1_found:
#                     valid_nodes[(i, j)] = None
#                     dg(G, C1, C2)
#                     return False, valid_nodes

#     return True, valid_nodes


# def bfs_check_paths(G, P, c1, C2, malicious_nodes):

#     def contains_honest_member(node, trustset, malicious_nodes):
#         return node in trustset and node not in malicious_nodes

#     visited = set()
#     queue = deque([P])

#     while queue:
#         current_node = queue.popleft()
#         if current_node in visited:
#             continue
#         visited.add(current_node)

#         if current_node == c1:
#             continue

#         if contains_honest_member(current_node, C2, malicious_nodes):
#             continue

#         for neighbor in G.neighbors(current_node):
#             if neighbor == c1:
#                 if not contains_honest_member(current_node, C2, malicious_nodes):
#                     return False
#             elif neighbor not in visited:
#                 queue.append(neighbor)

#     return True


# def check_assumption_5_bfs(G, trustsets, malicious_nodes):
    trustset_list = list(trustsets)
    valid_nodes = {}

    tqdm_disable = True
    for i in tqdm(range(len(trustset_list)), disable=tqdm_disable, desc="Outer Trustsets"):
        for j in tqdm(range(len(trustset_list)), disable=tqdm_disable, desc="Inner Trustsets", leave=False):
            if i != j:
                C1 = trustset_list[i]
                C2 = trustset_list[j]

                print(f"C1: {C1} \nC2: {C2}")

                valid_c1_found = False
                for c1 in tqdm(C1, disable=tqdm_disable, desc="Nodes in C1    ", leave=False):
                    all_paths_valid = True

                    for P in tqdm(G.nodes(), disable=tqdm_disable, desc="Source Nodes   ", leave=False):
                        if P == c1:
                            continue

                        if not bfs_check_paths(G, P, c1, C2, malicious_nodes):
                            all_paths_valid = False
                            break

                    if all_paths_valid:
                        valid_c1_found = True
                        valid_nodes[(i, j)] = c1
                        break

                if not valid_c1_found:
                    valid_nodes[(i, j)] = None
                    dg(G, C1, C2)
                    return False, valid_nodes

    return True, valid_nodes


def check_assumption_5(G, trustsets, malicious_nodes):
    trustset_list = list(trustsets)
    valid_nodes = {}
    assumption_validity = False
    
    for i in tqdm(range(len(trustset_list)), desc="Outer Trustsets"):
        for j in range(len(trustset_list)):
            if i != j:
                C1 = trustset_list[i]
                C2 = trustset_list[j]

                valid_c1_found = False
                for c1 in C1:
                    all_neighbors_honest = True

                    if c1 in C2 and c1 not in malicious_nodes:
                        valid_c1_found = True
                        break

                    for neighbor in G.neighbors(c1):
                        if neighbor not in C2 or neighbor in malicious_nodes:
                            all_neighbors_honest = False
                            break

                    if all_neighbors_honest:
                        valid_c1_found = True
                        valid_nodes[(i, j)] = c1
                        break

                if not valid_c1_found:
                    valid_nodes[(i, j)] = None
                    dg(G, C1, C2)
                    

    return assumption_validity, valid_nodes    


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
