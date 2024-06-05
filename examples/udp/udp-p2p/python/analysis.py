import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.widgets import Button
from file_loader import state, load_log_data, load_simulation_data

def create_graph(log_data, message_groups):
    G = nx.DiGraph()
    events = []

    for message_key, entries in message_groups.items():
        for entry in entries:
            from_node = entry.get('from_node')
            if from_node:
                events.append((entry['timestamp'], int(from_node), int(entry['node_id']), entry['action'], message_key))

    events.sort()
    return G, events

def draw_graph(G, pos_dict, events, message_key=None):
    fig, ax = plt.subplots(figsize=(12, 8))
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.25)  # Adjust layout to make room for buttons

    if message_key:
        events = filter_events_for_message(events, message_key)

    num_frames = len(events)
    current_frame = [0]  # Use a list to keep it mutable within nested functions

    def update_graph(frame):
        ax.clear()
        G = nx.DiGraph()
        current_events = events[:frame + 1]
        
        for event in current_events:
            timestamp, from_node, to_node, action, message_key = event
            if action == 'Rx':
                G.add_edge(from_node, to_node, color='blue', weight=2)
            elif action == 'Tx':
                G.add_edge(from_node, to_node, color='green', weight=2)
            elif action == 'Bx':
                G.add_edge(from_node, to_node, color='red', weight=2)
            elif action == 'Ax':
                G.add_edge(from_node, to_node, color='purple', weight=2)
        
        edges = G.edges(data=True)
        colors = [e[2].get('color', 'black') for e in edges]
        weights = [e[2].get('weight', 1) for e in edges]
        
        nx.draw(G, pos=pos_dict, ax=ax, with_labels=True, node_size=700, node_color="skyblue", font_size=15, font_weight="bold", arrows=True, edge_color=colors, width=weights)
        nx.draw_networkx_edge_labels(G, pos=pos_dict, ax=ax, edge_labels=nx.get_edge_attributes(G, 'label'), font_color='red')
        ax.set_title(f'Timestep: {frame}')

    def next_frame(event):
        if current_frame[0] < num_frames - 1:
            current_frame[0] += 1
            update_graph(current_frame[0])
            plt.draw()

    def prev_frame(event):
        if current_frame[0] > 0:
            current_frame[0] -= 1
            update_graph(current_frame[0])
            plt.draw()

    ax_next = plt.axes([0.81, 0.05, 0.1, 0.075])
    ax_prev = plt.axes([0.7, 0.05, 0.1, 0.075])
    btn_next = Button(ax_next, 'Next')
    btn_prev = Button(ax_prev, 'Back')

    btn_next.on_clicked(next_frame)
    btn_prev.on_clicked(prev_frame)

    update_graph(0)  # Initialize the graph
    plt.show()

def filter_events_for_message(events, message_key):
    events = [event for event in events if event[4] == message_key]
    print(events)
    return events


if __name__ == "__main__":
    import json

    # File paths
    simulation_file = '../simulation.csc'
    log_file = '../loglistener_short.txt'

    # Parsing files
    state['simulation_file_path'] = simulation_file
    state['log_file_path'] = log_file
    load_simulation_data(simulation_file)
    load_log_data(log_file)

    # Generate graph and draw
    state['G'], state['events'] = create_graph(state['log_data'], state['message_groups'])

    for node_id, node_state in state['node_states'].items():
        if node_id == 1:
            print(f"Node: {node_id}")
            print(json.dumps(node_state['rx'], indent=2))
            print()

    # # Specific message key (example: message_num='0', origin_node='1')
    # specific_message_key = ('0', '1') 
    # draw_graph(state['G'], state['mote_positions'], state['events'], specific_message_key)
