import xml.etree.ElementTree as ET
import re
import matplotlib.pyplot as plt


def parse_simulation_file(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    motes = []
    for motetype in root.findall(".//motetype"):
        for mote in motetype.findall(".//mote"):
            mote_info = {}
            position = mote.find(".//interface_config[org.contikios.cooja.interfaces.Position]/pos")
            mote_id = mote.find(".//interface_config[org.contikios.cooja.contikimote.interfaces.ContikiMoteID]/id")

            if position is not None and mote_id is not None:
                mote_info['id'] = int(mote_id.text)
                mote_info['x'] = float(position.get('x'))
                mote_info['y'] = float(position.get('y'))
                motes.append(mote_info)
    return motes


def parse_log_file(file_path):
    message_pattern = re.compile(r'(\d{2}:\d{2}.\d{3})\s+ID:(\d+)\s+\[INFO: App\s+\]\s+(.*)')
    messages = {}
    
    with open(file_path, 'r') as file:
        for line in file:
            match = message_pattern.match(line)
            if match:
                time, node_id, info = match.groups()
                node_id = int(node_id)
                
                if "Sending request" in info:
                    message_id = info.split()[2]
                    origin_addr = info.split()[-1]
                    message_key = f"{message_id}|{origin_addr}"
                    if message_key not in messages:
                        messages[message_key] = []
                    messages[message_key].append((time, node_id, 'send'))
                
                elif "Rx" in info:
                    parts = info.split()
                    message_key = parts[1].strip("'")
                    source_addr = parts[-1].strip("'")
                    if message_key not in messages:
                        messages[message_key] = []
                    messages[message_key].append((time, node_id, 'receive', source_addr))
                
                elif "Duplicate message received, ignoring" in info:
                    message_key = info.split()[1].strip("'")
                    if message_key not in messages:
                        messages[message_key] = []
                    messages[message_key].append((time, node_id, 'ignore'))
                
                elif "Tx: flood" in info:
                    message_key = info.split()[2].strip("'")
                    if message_key not in messages:
                        messages[message_key] = []
                    messages[message_key].append((time, node_id, 'flood'))
    
    return messages


def visualize_message_propagation(motes, messages, message_key):
    mote_positions = {mote['id']: (mote['x'], mote['y']) for mote in motes}
    print("Mote positions:", mote_positions)  # Debug print
    events = messages.get(message_key, [])
    print("Events for message key:", events)  # Debug print
    
    fig, ax = plt.subplots()
    for mote in motes:
        ax.plot(mote['x'], mote['y'], 'bo')
        ax.text(mote['x'], mote['y'], f"{mote['id']}", fontsize=12, ha='right')
    
    for event in events:
        time, node_id, action, *source = event
        print("Processing event:", event)  # Debug print
        if node_id not in mote_positions:
            print(f"Node ID {node_id} not found in mote_positions")  # Debug print
            continue
        x, y = mote_positions[node_id]
        if action == 'send':
            ax.plot(x, y, 'go')
        elif action == 'receive':
            ax.plot(x, y, 'yo')
            source_addr = source[0]
            for mote in motes:
                if mote['id'] == node_id:
                    source_x, source_y = mote_positions[node_id]
                    ax.arrow(source_x, source_y, x - source_x, y - source_y, head_width=1, head_length=1, fc='yellow', ec='yellow')
        elif action == 'flood':
            ax.plot(x, y, 'ro')
        elif action == 'ignore':
            ax.plot(x, y, 'ko')
    
    ax.set_xlabel('X Coordinate')
    ax.set_ylabel('Y Coordinate')
    ax.set_title(f'Message Propagation: {message_key}')
    plt.show()


# File paths
simulation_file = 'simulation.csc'
log_file = 'loglistener.txt'

# Parsing files
motes = parse_simulation_file(simulation_file)
print("Parsed motes:", motes)  # Debug print
# messages = parse_log_file(log_file)
# print("Parsed messages:", messages)  # Debug print

# # Visualize a specific message propagation
# message_key_to_visualize = '0|fe80::203:3:3:3'  # Replace with the desired message key
# visualize_message_propagation(motes, messages, message_key_to_visualize)
