import xml.etree.ElementTree as ET

def parse_mealy_machine(file_path):
    """
    Parse a Mealy machine XML file and return its structure.
    """
    # Parse the XML file
    tree = ET.parse(file_path)
    root = tree.getroot()

    states = {}
    transitions = []

    for state in root.findall('state'):
        state_id = state.get('id')
        states[state_id] = {}

        for transition in state.findall('transition'):
            destination = transition.get('to')
            inputs = transition.get('input').split(", ")
            output = transition.get('output')

            for input_symbol in inputs:
                transitions.append({
                    'source': state_id,
                    'destination': destination,
                    'input': input_symbol,
                    'output': output
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

# Main execution
file_path = "mealy_machine.xml"  # Assuming the file is in the same directory

# Parse the XML file
states, transitions = parse_mealy_machine(file_path)

# Generate the structured Mealy machine
mealy_machine = generate_mealy_structure(states, transitions)

# Display the result
import pprint
pprint.pprint(mealy_machine)