import xml.etree.ElementTree as ET
import re
from collections import defaultdict


def parse_simulation_file(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    node_positions = {}
    for node_type in root.findall(".//motetype"):
        for node in node_type.findall(".//mote"):
            position = node.find(".//interface_config/pos")
            node_id = node.find(".//interface_config/id")
            
            if position is not None and node_id is not None:
                node_id_int = int(node_id.text)
                node_positions[node_id_int] = (float(position.get('x')), float(position.get('y')))
                
    return node_positions


def parse_log_file(file_path):
    log_data = defaultdict(list)
    message_groups = defaultdict(list)
    node_states = defaultdict(lambda: {'tx': [], 'rx': [], 'bx': [], 'ax': []})

    log_pattern = re.compile(
        r'(?P<timestamp>\d+:\d+\.\d+)\tID:(?P<node_id>\d+)\t\[[A-Z]+\: Node\s*\]\s*'
        r'(?P<action>[A-Za-z]+): \'(?P<message_num>\d+)\|(?P<origin_node>\d+)\|(?P<attest_node>\d+)\''
        r'(?: from node: \'(?P<from_node>\d+)\')?'
    )
    
    with open(file_path, 'r') as file:
        for line in file:
            match = log_pattern.match(line)
            if match:
                log_entry = match.groupdict()
                log_entry['timestamp'] = float(log_entry['timestamp'].replace(':', ''))
                log_data[int(log_entry['node_id'])].append(log_entry)
                message_key = (log_entry['message_num'], log_entry['origin_node'])
                message_groups[message_key].append(log_entry)
                
                node_id = int(log_entry['node_id'])
                action = log_entry['action'].lower()
                
                if action == 'tx':
                    node_states[node_id]['tx'].append({
                        'timestamp': log_entry['timestamp'],
                        'message_num': log_entry['message_num'],
                        'attestations': []
                    })
                elif action == 'rx':
                    node_states[node_id]['rx'].append({
                        'timestamp': log_entry['timestamp'],
                        'message_num': log_entry['message_num'],
                        'origin_node': log_entry['origin_node'],
                        'attest_node': log_entry['attest_node'],
                        'from_node': log_entry.get('from_node')
                    })
                    
                    # Update attestations for corresponding tx entries
                    for tx_entry in node_states[int(log_entry['origin_node'])]['tx']:
                        if tx_entry['message_num'] == log_entry['message_num'] and node_id != int(log_entry['origin_node']):
                            attestations = tx_entry['attestations']
                            if not any(att['attest_node'] == node_id for att in attestations):
                                tx_entry['attestations'].append({
                                    'timestamp': log_entry['timestamp'],
                                    'attest_node': node_id
                                })
                elif action == 'bx':
                    node_states[node_id]['bx'].append({
                        'timestamp': log_entry['timestamp'],
                        'message_num': log_entry['message_num'],
                        'origin_node': log_entry['origin_node'],
                        'attest_node': log_entry['attest_node']
                    })
                elif action == 'ax':
                    node_states[node_id]['ax'].append({
                        'timestamp': log_entry['timestamp'],
                        'message_num': log_entry['message_num'],
                        'origin_node': log_entry['origin_node']
                    })
    
    return log_data, message_groups, node_states


"""
pos_dict
{
    mote_id_1: (x_coordinate_1, y_coordinate_1),
    mote_id_2: (x_coordinate_2, y_coordinate_2),
    # More motes...
}

log_data:
{
    1: [
        {
            'timestamp': float,  # The timestamp of the log entry
            'mote_id': str,      # The ID of the mote that logged this entry
            'action': str,       # The action type (e.g., 'Tx', 'Rx', 'Bx', 'Ax')
            'message_num': str,  # The message number
            'origin_node': str,  # The origin node that created the message
            'attest_node': str,  # The node that attested the message
            'from_node': str     # The node from which the message was received (if applicable)
        },
        # More log entries for mote 1...
    ],
    # More motes...
}

message_groups:
{
    (message_num, origin_node): [
        {
            'timestamp': float,  # The timestamp of the log entry
            'mote_id': str,      # The ID of the mote that logged this entry
            'action': str,       # The action type (e.g., 'Tx', 'Rx', 'Bx', 'Ax')
            'message_num': str,  # The message number
            'origin_node': str,  # The origin node that created the message
            'attest_node': str,  # The node that attested the message
            'from_node': str     # The node from which the message was received (if applicable)
        },
        # More log entries for this message...
    ],
    # More messages...
}

detailed_log:
{
    mote_id: [
        {
            'tx': [
                {
                    'timestamp': float,  # The timestamp of the log entry
                    'message_num': str,  # The number of the message it created
                    'attestations': [    # List of attestations received for the given message
                        {
                            'timestamp': float,  # The timestamp the attestation was received
                            'attest_node': int   # The node that attested the message
                        },
                        # more attestations from other motes
                    ]
                },
                # more messages that were created and originated from this mote_id
            ]
        },

        {
            'rx': [
                {
                    'timestamp': float,  # The timestamp of the log entry
                    'message_num': str,  # The message number
                    'origin_node': str,  # The origin node that created the message
                    'attest_node': str,  # The node that attested the message
                    'from_node': str     # The node from which the message was received (if applicable)
                },
                # More messages received by this mote_id
            ]
        },

        {
            'bx': [
                {
                    'timestamp': float,  # The timestamp of the log entry
                    'message_num': str,  # The message number
                    'origin_node': str,  # The origin node that created the message
                    'attest_node': str   # The node that attested the message
                },
                # More messages broadcast by this mote_id
            ]
        },

        {
            'ax': [
                {
                    'timestamp': float,  # The timestamp of the log entry
                    'message_num': str,  # The message number
                    'origin_node': str   # The origin node that created the message
                },
                # More messages attested by this mote_id
            ]
        }
    ],

    # more mote_ids
}
"""