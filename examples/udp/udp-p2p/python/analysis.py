import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.widgets import Button
from file_loader import state, load_log_data, load_simulation_data


def process_events(message_groups):
    events = []  # event = (timestamp, from_node, to_node, message_key)

    for message_key, msg_events in message_groups.items():
        for msg_event in msg_events:
            from_node = msg_event.get('from_node')
            if from_node:
                events.append((msg_event['timestamp'], from_node, msg_event['node_id'], message_key))

    events.sort()
    return events


def filter_messages(message_groups, message_mask):
    def matches_params(t):        
        if 'message_num' in message_mask:
            if isinstance(message_mask['message_num'], list):
                message_num_match = (t[0] in message_mask['message_num'])
            else:
                message_num_match = (t[0] == message_mask['message_num'])
        else:
            message_num_match = True
        
        if 'origin_node' in message_mask:
            if isinstance(message_mask['origin_node'], list):
                origin_node_match = (t[1] in message_mask['origin_node'])
            else:
                origin_node_match = (t[1] == message_mask['origin_node'])
        else:
            origin_node_match = True
        
        if 'attest_node' in message_mask:
            if isinstance(message_mask['attest_node'], list):
                attest_node_match = (t[2] in message_mask['attest_node'])
            else:
                attest_node_match = (t[2] == message_mask['attest_node'])
        else:
            attest_node_match = True
        
        return message_num_match and origin_node_match and attest_node_match

    filtered_messages = {msg_key: msg_list for msg_key, msg_list in message_groups.items() if matches_params(msg_key)}
    return filtered_messages


def draw_graph(pos_dict, message_groups, message_mask=None):
    fig, ax = plt.subplots(figsize=(12, 8))
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.2)

    if message_mask:
        events = process_events(
            filter_messages(message_groups, message_mask)
            )
    else:
        events = process_events(message_groups)

    num_frames = len(events)
    current_frame = [0]

    def update_graph(frame):
        ax.clear()
        G = nx.DiGraph()
        G.add_nodes_from(pos_dict)
        nx.set_node_attributes(G, 'skyblue', 'color')
        current_events = events[:frame]
        
        for i, event in enumerate(current_events):
            timestamp, from_node, to_node, message_key = event
            color = 'yellow' if message_key[2] != 0 else 'blue'
            G.add_edge(from_node, to_node, color=color, weight=2)

            if i == frame - 1:
                print(f"Time: {timestamp}, {from_node} -> {to_node}, {'att' if message_key[2] != 0 else 'msg'}")
                G.nodes[from_node]['color'] = 'red'
                G.nodes[to_node]['color'] = 'green'
        
        edges = G.edges(data=True)
        colors = [e[2].get('color', 'black') for e in edges]
        weights = [e[2].get('weight', 1) for e in edges]
        node_colors = [G.nodes[node].get('color', 'skyblue') for node in G.nodes()]
        
        nx.draw(G, pos=pos_dict, ax=ax, with_labels=True, node_size=700, node_color=node_colors, font_size=15, font_weight="bold", arrows=True, edge_color=colors, width=weights)
        nx.draw_networkx_edge_labels(G, pos=pos_dict, ax=ax, edge_labels=nx.get_edge_attributes(G, 'label'), font_color='red')
        ax.set_title(f'Timestep: {frame}')

    def next_frame(event):
        if current_frame[0] < num_frames:
            current_frame[0] += 1
            update_graph(current_frame[0])
            plt.draw()

    def prev_frame(event):
        if current_frame[0] > 0:
            current_frame[0] -= 1
            update_graph(current_frame[0])
            plt.draw()

    ax_next = plt.axes([0.85, 0.05, 0.1, 0.075])
    ax_prev = plt.axes([0.7, 0.05, 0.1, 0.075])
    btn_next = Button(ax_next, 'Next')
    btn_prev = Button(ax_prev, 'Back')

    btn_next.on_clicked(next_frame)
    btn_prev.on_clicked(prev_frame)

    update_graph(0)  # Initialize the graph
    plt.show()


if __name__ == "__main__":
    import json

    # File paths
    simulation_file = '../simulation.csc'
    log_file = '../loglistener.txt'

    # Parsing files
    state['simulation_file_path'] = simulation_file
    state['log_file_path'] = log_file
    load_simulation_data(simulation_file)
    load_log_data(log_file)

    # for node_id, node_state in state['node_states'].items():
    #     # if node_id == 1:
    #         print(f"Node: {node_id}")
    #         print(json.dumps(node_state['tx'], indent=2))
    #         print()


    # for message_key, message_list in state['message_groups'].items():
    #     print(f"Message Key: {message_key}")
    #     for message in message_list:
    #         if message_key[1] == message['node_id'] and int(message['attest_node']) != 0:
    #             print(json.dumps(message, indent=2))
    #             print()

    message_mask = {
        'message_num': 0,
        'origin_node': 1,
        'attest_node': 0
    }

    draw_graph(state['node_positions'], state['message_groups'], message_mask)
