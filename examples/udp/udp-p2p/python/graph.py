import networkx as nx
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches


def nodal_distance(node1, node2):
    x1, y1 = node1
    x2, y2 = node2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def create_graph(node_positions, distance_threshold):
    G = nx.Graph()
    G.add_nodes_from(node_positions)
    nx.set_node_attributes(G, node_positions, 'pos')

    for node_id_1, pos1 in node_positions.items():
        for node_id_2, pos2 in node_positions.items():
            if node_id_1 != node_id_2:
                distance = nodal_distance(pos1, pos2)
                if distance < distance_threshold:
                    G.add_edge(node_id_1, node_id_2)

    return G


def draw_node_with_colors(ax, pos, node, colors, node_size, label):
    x, y = pos[node]
    radius = node_size / 500
    if len(colors) == 2:
        circle = patches.Circle((x, y), radius=radius, edgecolor='black', facecolor=colors[0])
        wedge = patches.Wedge((x, y), radius, theta1=45, theta2=225, edgecolor='black', facecolor=colors[1])
        ax.add_patch(circle)
        ax.add_patch(wedge)
    else:
        circle = patches.Circle((x, y), radius=radius, edgecolor='black', facecolor=colors[0])
        ax.add_patch(circle)

    ax.text(x, y, str(label), fontsize=12, ha='center', va='center', color='black')


def visualize_graph(G, C1, C2, violating_source, violating_path):
    pos = nx.spring_layout(G)
    pos = nx.get_node_attributes(G, 'pos')
    node_size = 500
    fig, ax = plt.subplots(figsize=(10, 8))

    edge_colors = []
    for edge in G.edges():
        if violating_path and (edge in zip(violating_path[:-1], violating_path[1:]) or (edge[1], edge[0]) in zip(violating_path[:-1], violating_path[1:])):
            edge_colors.append('orange')
        else:
            edge_colors.append('dimgray')

    nx.draw_networkx_edges(G, pos, ax=ax, edge_color=edge_colors, width=2)

    for node in G.nodes():
        if node in C1 and node in C2:    # Overlap = two colors
            draw_node_with_colors(ax, pos, node, ['green', 'blue'], node_size, node)
        elif node in C1:                 # C1 = green
            draw_node_with_colors(ax, pos, node, ['green'], node_size, node)
        elif node in C2:                 # C2 = blue
            draw_node_with_colors(ax, pos, node, ['blue'], node_size, node)
        elif node == violating_source:   # P = red
            draw_node_with_colors(ax, pos, node, ['red'], node_size, node)
        else:                            # Default = gray
            draw_node_with_colors(ax, pos, node, ['lightgray'], node_size, node)
    
    nx.draw_networkx_labels(G, pos, ax=ax)
    ax.set_aspect('equal')

    all_x, all_y = zip(*pos.values())
    x_margin = (max(all_x) - min(all_x)) * 1
    y_margin = (max(all_y) - min(all_y)) * 0.1
    ax.set_xlim(min(all_x) - x_margin, max(all_x) + x_margin)
    ax.set_ylim(min(all_y) - y_margin, max(all_y) + y_margin)

    plt.show()
