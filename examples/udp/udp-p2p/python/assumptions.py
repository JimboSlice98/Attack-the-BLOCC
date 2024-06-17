import json
import networkx as nx
import textwrap
from tqdm import tqdm


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

    def contains_honest_member(path, trustset):
        return any(node in trustset and node not in malicious_nodes for node in path)

    for i in tqdm(range(len(trustset_list)), desc="Outer Trustsets"):
        for j in tqdm(range(len(trustset_list)), desc="Inner Trustsets", leave=False):
            if i != j:
                C1 = trustset_list[i]
                C2 = trustset_list[j]

                valid_path_found = False
                for c1 in tqdm(C1, desc="Nodes in C1    ", leave=False):
                    for source in tqdm(G.nodes(), desc="Source Nodes   ", leave=False):
                        if source == c1:
                            continue
                        if nx.has_path(G, source, c1):
                            for path in nx.all_simple_paths(G, source, c1):
                                if contains_honest_member(path, C2):
                                    valid_path_found = True
                                    break
                            if valid_path_found:
                                break
                    if valid_path_found:
                        break

                if not valid_path_found:
                    return False, C1, C2

    return True, None, None


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
