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


def check_assumption_5(G, trustsets, malicious_nodes):
    trustset_list = list(trustsets)
    valid_nodes = {}
    assumption_validity = True
    tqdm_disable = True
    
    for i in tqdm(range(len(trustset_list)), disable=tqdm_disable):
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
                    assumption_validity = False
                    
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
