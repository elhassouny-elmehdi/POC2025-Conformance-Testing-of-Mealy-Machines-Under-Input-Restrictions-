import xml.etree.ElementTree as ET
import graphviz
import pprint

def parse_mealy_machine(file_path):
    """
    Parse a Mealy machine XML file and return its structure.
    """
    # Parse the XML file
    tree = ET.parse(file_path)
    root = tree.getroot()

    states = {}
    transitions = []

    for state in root.findall('State'):
        state_id = state.get('id')
        states[state_id] = {}

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

def visualize_mealy_machine(states, transitions, output_file="mealy_machine"):
    """
    Visualize the Mealy machine using Graphviz.
    """
    dot = graphviz.Digraph(format="png")

    # Add states
    for state in states.keys():
        dot.node(state, state)

    # Add transitions
    for transition in transitions:
        source = transition['source']
        destination = transition['destination']
        label = f"{transition['input']}/{transition['output']}"
        dot.edge(source, destination, label=label)

    # Render the graph
    dot.render(output_file, view=True)

# Main execution
file_path = "Mealy_Machine_10_States.xml"  # Assuming the file is in the same directory

# Parse the XML file
states, transitions = parse_mealy_machine(file_path)

# Generate the structured Mealy machine
mealy_machine = generate_mealy_structure(states, transitions)

# Display the result
pprint.pprint(mealy_machine)

# Visualize the Mealy machine
visualize_mealy_machine(states, transitions, output_file="mealy_machine")
