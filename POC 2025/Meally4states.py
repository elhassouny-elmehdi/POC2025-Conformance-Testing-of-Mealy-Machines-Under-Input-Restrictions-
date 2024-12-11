import xml.etree.ElementTree as ET
from graphviz import Digraph
import pprint

def parse_mealy_machine(file_path):
    """
    Parse a Mealy machine XML file and return its structure.
    """
    # Parse the XML file
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Extract states
    states = {}
    for state in root.findall('State'):
        state_id = state.get('id')
        is_initial = state.get('initial', 'false') == 'true'
        states[state_id] = {'name': state.get('name'), 'initial': is_initial}

    # Extract transitions
    transitions = []
    for transition in root.findall('Transition'):
        source = transition.get('source')
        destination = transition.get('destination')
        label = transition.get('label')
        input_symbol, output_symbol = label.split('/')
        transitions.append({
            'source': source,
            'destination': destination,
            'input': input_symbol,
            'output': output_symbol
        })

    return states, transitions

def generate_mealy_structure(states, transitions):
    """
    Generate a dictionary structure for the Mealy machine.
    """
    result = {
        "states": list(states.keys()),
        "initial-state": [k for k, v in states.items() if v['initial']][0],
        "input-alphabet": list(set(t['input'] for t in transitions)),
        "output-alphabet": list(set(t['output'] for t in transitions)),
        "transition-function": {
            state: {t['input']: t['destination'] for t in transitions if t['source'] == state}
            for state in states.keys()
        },
        "output-function": {
            state: {t['input']: t['output'] for t in transitions if t['source'] == state}
            for state in states.keys()
        }
    }
    return result

def display_mealy_graph(mealy_machine):
    """
    Generate and display a graph of the Mealy machine using Graphviz.
    """
    dot = Digraph(format="png")

    # Regrouper les transitions entre les mêmes états
    grouped_transitions = {}
    for state, transitions in mealy_machine["transition-function"].items():
        for input_symbol, next_state in transitions.items():
            output_symbol = mealy_machine["output-function"][state][input_symbol]
            if (state, next_state) not in grouped_transitions:
                grouped_transitions[(state, next_state)] = []
            grouped_transitions[(state, next_state)].append(f"{input_symbol}/{output_symbol}")

    # Ajouter les nœuds (états) au graphe
    for state in mealy_machine["states"]:
        if state == mealy_machine["initial-state"]:
            dot.node(state, color="red", style="filled", fillcolor="lightgrey")
        else:
            dot.node(state)

    # Ajouter les arêtes (transitions) regroupées au graphe
    for (state, next_state), labels in grouped_transitions.items():
        combined_label = ", ".join(labels)
        dot.edge(state, next_state, label=combined_label)

    # Render the graph
    dot.render("mealy_machine_graph", view=True)

# Main execution
file_path = "Mealy_Machine_4_States.xml"  # Assuming the file is in the same directory

# Parse the XML file
states, transitions = parse_mealy_machine(file_path)

# Generate the structured Mealy machine
mealy_machine = generate_mealy_structure(states, transitions)

# Display the result
pprint.pprint(mealy_machine)

# Display the Mealy machine graph
display_mealy_graph(mealy_machine)
