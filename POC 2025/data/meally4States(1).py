import xml.etree.ElementTree as ET

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

# Main execution
file_path = "Mealy_Machine_4_States.xml"  # Assuming the file is in the same directory

# Parse the XML file
states, transitions = parse_mealy_machine(file_path)

# Generate the structured Mealy machine
mealy_machine = generate_mealy_structure(states, transitions)

# Display the result
import pprint
pprint.pprint(mealy_machine)
