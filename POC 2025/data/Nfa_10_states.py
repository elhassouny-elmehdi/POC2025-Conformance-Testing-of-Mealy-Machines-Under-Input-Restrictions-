import xml.etree.ElementTree as ET
import pprint
import json
import graphviz

def parse_nfa(file_path):
    """
    Parse an NFA XML file and return its structure.
    """
    try:
        # Parse the XML file
        tree = ET.parse(file_path)
        root = tree.getroot()

        # Extract states
        states = {}
        for state in root.find('States').findall('State'):
            state_id = state.get('id')
            is_start = state.get('isStart', 'false') == 'true'
            is_accept = state.get('isAccept', 'false') == 'true'
            states[state_id] = {
                'isStart': is_start,
                'isAccept': is_accept
            }

        # Extract transitions
        transitions = []
        for transition in root.find('Transitions').findall('Transition'):
            src = transition.get('src')
            dest = transition.get('dest')
            symbols = transition.get('symbol').split(',')  # Handle multiple symbols
            for symbol in symbols:
                transitions.append({
                    'src': src,
                    'dest': dest,
                    'symbol': symbol
                })

        return states, transitions

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return {}, []
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
        return {}, []

def generate_nfa_structure(states, transitions):
    """
    Generate a dictionary structure for the NFA.
    """
    start_states = [k for k, v in states.items() if v['isStart']]
    accept_states = [k for k, v in states.items() if v['isAccept']]

    result = {
        "states": list(states.keys()),
        "start-states": start_states,
        "accept-states": accept_states,
        "alphabet": list(set(t['symbol'] for t in transitions)),
        "transition-function": {
            state: {symbol: [] for symbol in set(t['symbol'] for t in transitions)}
            for state in states.keys()
        }
    }

    # Populate the transition function
    for t in transitions:
        result['transition-function'][t['src']][t['symbol']].append(t['dest'])

    return result

def visualize_nfa(states, transitions, output_file="nfa_machine"):
    """
    Visualize the NFA using Graphviz.
    """
    dot = graphviz.Digraph(format="png")

    # Add states
    for state, attributes in states.items():
        if attributes['isStart'] and attributes['isAccept']:
            dot.node(state, state, shape="doublecircle", style="filled", color="lightblue")
        elif attributes['isStart']:
            dot.node(state, state, shape="circle", style="filled", color="lightgreen")
        elif attributes['isAccept']:
            dot.node(state, state, shape="doublecircle")
        else:
            dot.node(state, state, shape="circle")

    # Add transitions
    for transition in transitions:
        src = transition['src']
        dest = transition['dest']
        label = transition['symbol']
        dot.edge(src, dest, label=label)

    # Render the graph
    dot.render(output_file, view=True)

# Main execution
file_path = "nfa_10_states.xml"  # Assuming the file is in the same directory

# Parse the XML file
states, transitions = parse_nfa(file_path)

if states and transitions:  # Proceed only if parsing was successful
    # Generate the structured NFA
    nfa = generate_nfa_structure(states, transitions)

    # Display the result
    pprint.pprint(nfa)

    # Visualize the NFA
    visualize_nfa(states, transitions, output_file="nfa_machine")

    # Save to JSON
    with open("nfa_10_states.json", "w") as f:
        json.dump(nfa, f, indent=4)
        print("NFA saved to 'nfa_10_states.json'")
