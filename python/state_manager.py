import textwrap
import json
import time
import matplotlib.pyplot as plt
from file_parser import parse_simulation_file, parse_log_file
from trustsets import trustset_generator_factory, create_malicious_parties
from graph import create_graph, visualize_graph, visualize_graph_3D, visualize_graph_3D_with_click, find_node_with_honest_neighbors
from assumptions import *


class State:
    def __init__(self):
        self.simulation_file_path = None
        self.log_file_path = None

        self.node_positions = None
        self.log_data = None
        self.message_groups = None
        self.node_states = None

        self.trustset_fraction = 2/3
        self.trustset_generator_factory = None
        self.malicious_nodes = None
        self.connectivity_graph = None

  
    def load_log_data(self, file_path):
        print("Loading log data")
        self.log_file_path = file_path
        self.log_data, self.message_groups, self.node_states = parse_log_file(
            file_path=file_path
        )
    

    def load_simulation_data(self, file_path):
        print("Loading simulation data")
        self.simulation_file_path = file_path
        self.node_positions = parse_simulation_file(
            file_path=file_path
        )

    
    def generate_trustsets(self, fraction=2/3):
        print("Generating trustsets")
        self.trustset_generator_factory = trustset_generator_factory(
            node_positions=self.node_positions, 
            fraction=fraction            
        )

    
    def num_nodes(self):
        return len(self.node_positions)

    
    def create_malicious_parties(self, num_malicious):
        print("Assigning malicious nodes")
        self.malicious_nodes = create_malicious_parties(
            node_positions=self.node_positions, 
            num_malicious=num_malicious
        )

    
    def create_graph(self):
        print("Creating connectivity graph")
        self.connectivity_graph = create_graph(
            node_positions=self.node_positions,
            malicious_nodes = self.malicious_nodes,
            distance_threshold=14
        )

    
    def check_assumption_1(self):
        result, error_message = check_assumption_1(
            node_positions=self.node_positions,
            trustset_generator=self.trustset_generator_factory()
        )
        print(f"Assumption 1: {result}")
        
        if not result:
            print(error_message)
        return result
    

    def check_assumption_2(self):
        result, error_message = check_assumption_2(
            trustset_generator=self.trustset_generator_factory(),
            malicious_nodes=self.malicious_nodes            
        )
        print(f"Assumption 2: {result}")
        
        if not result:
            print(error_message)
        return result
    

    def check_assumption_3(self):
        result, error_message = check_assumption_3(
            trustset_generator=self.trustset_generator_factory(),
            malicious_nodes=self.malicious_nodes         
        )
        print(f"Assumption 3: {result}")
        
        if not result:
            print(error_message)
        return result
    

    def check_assumption_4(self):
        result, error_message = check_assumption_4(
            node_states=self.node_states,
            trustset_generator=self.trustset_generator_factory(),
            malicious_nodes=self.malicious_nodes,
            t_rep=5
        )
        print(f"Assumption 4: {result}")
        
        if not result:
            print(error_message)
        return result
    

    def check_assumption_5(self):
        result, valid_nodes = check_assumption_5(
            G=self.connectivity_graph,
            trustset_generator_factory=self.trustset_generator_factory,
            malicious_nodes=self.malicious_nodes
        )
        print(f"Assumption 5: {result}")


    def check_assumption_6(self):
        result, error_message = check_assumption_6(
            node_states=self.node_states,
            trustset_generator_factory=self.trustset_generator_factory,
            malicious_nodes=self.malicious_nodes,
            t_rep=5
        )
        print(f"Assumption 6: {result}")
        
        if not result:
            print(error_message)
        return result


    def check_assumptions(self):
        print(textwrap.dedent(f"""
            ===================================================================
            Honest nodes: {set(self.node_positions.keys()) - self.malicious_nodes}
            Malicious nodes: {self.malicious_nodes}
            ===================================================================
        """))

        self.check_assumption_1()
        self.check_assumption_2()
        self.check_assumption_3()
        self.check_assumption_4()        
        self.check_assumption_5()
        self.check_assumption_6()


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from state_manager import State
    from graph import visualize_graph

    simulation_file = '../simulation-z-large.csc'
    log_file = '../loglistener-new.txt'

    state = State()
    state.load_simulation_data(simulation_file)
    state.load_log_data(log_file)

    max_malicious = state.num_nodes() // 3

    state.generate_trustsets(fraction=2/3)
    state.create_malicious_parties(num_malicious=max_malicious)

    state.create_graph()
    
    visualize_graph_3D(state.connectivity_graph, {}, {})
    # print(find_node_with_honest_neighbors(state.connectivity_graph, state.malicious_nodes))
    # visualize_graph_3D_with_click(state.connectivity_graph, {}, {})
    # visualize_graph(state.connectivity_graph, {}, {})
    
    state.check_assumptions()
