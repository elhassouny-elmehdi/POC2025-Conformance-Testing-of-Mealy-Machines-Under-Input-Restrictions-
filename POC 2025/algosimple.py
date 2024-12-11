from graphviz import Digraph
import itertools

# Classe MealyMachine
class MealyMachine:
    def __init__(self, transitions, init_state):
        """
        Initialise la machine de Mealy.
        :param transitions: Dictionnaire des transitions sous la forme {(état, entrée): (état_suivant, sortie)}
        :param init_state: État initial de la machine
        """
        self.transitions = transitions
        self.initial_state = init_state

    def display_graph(self):
        """Génère et affiche un graphe de la machine de Mealy en utilisant Graphviz."""
        dot = Digraph(format="png")

        # Regrouper les transitions entre les mêmes états
        grouped_transitions = {}
        for (state, input_value), (next_state, output) in self.transitions.items():
            if (state, next_state) not in grouped_transitions:
                grouped_transitions[(state, next_state)] = []
            grouped_transitions[(state, next_state)].append(f"{input_value}/{output}")

        # Ajouter les transitions au graphe
        for (state, next_state), labels in grouped_transitions.items():
            combined_label = ", ".join(labels)
            dot.edge(state, next_state, label=combined_label)

        # Ajouter un style pour l'état initial
        dot.node(self.initial_state, color="red", style="filled", fillcolor="lightgrey")

        # Afficher le graphe
        dot.render("mealy_machine", view=True)

# Classe NFA
class NFA:
    def __init__(self, transitions, init_state, accept_states):
        """
        Initialise le NFA.
        :param transitions: Dictionnaire des transitions sous la forme {(état, entrée): [états_suivants]}
        :param init_state: État initial de l'automate
        :param accept_states: Liste des états d'acceptation
        """
        self.transitions = transitions
        self.initial_state = init_state
        self.accept_states = accept_states

    def display_graph(self):
        """Génère et affiche un graphe du NFA en utilisant Graphviz."""
        dot = Digraph(format="png")

        # Regrouper les transitions pour chaque paire (source, destination)
        grouped_transitions = {}
        for (state, input_value), next_states in self.transitions.items():
            for next_state in next_states:
                key = (state, next_state)
                if key not in grouped_transitions:
                    grouped_transitions[key] = []
                grouped_transitions[key].append(input_value)

        # Ajouter les transitions au graphe
        for (state, next_state), labels in grouped_transitions.items():
            label = ", ".join(labels)
            dot.edge(state, next_state, label=label)

        # Ajouter un style distinct pour l'état initial
        dot.node(self.initial_state, color="red", style="filled", fillcolor="lightgrey")

        # Ajouter un style distinct pour les états d'acceptation
        for accept_state in self.accept_states:
            dot.node(accept_state, shape="doublecircle", color="green")

        # Afficher le graphe
        dot.render("nfa_graph", view=True)

# Algorithme Simple
def generate_sequences(alphabet, max_depth):
    """
    Génère toutes les séquences possibles jusqu'à une profondeur max_depth.
    :param alphabet: Ensemble des symboles d'entrée.
    :param max_depth: Profondeur maximale des séquences.
    :return: Liste de toutes les séquences possibles.
    """
    sequences = []
    for depth in range(1, max_depth + 1):
        sequences.extend([''.join(seq) for seq in itertools.product(alphabet, repeat=depth)])
    return sequences

def is_sequence_accepted_by_nfa(sequence, nfa):
    """
    Vérifie si une séquence est acceptée par le NFA.
    :param sequence: Séquence d'entrée.
    :param nfa: Instance de la classe NFA.
    :return: True si la séquence est acceptée, False sinon.
    """
    current_states = {nfa.initial_state}

    for symbol in sequence:
        next_states = set()
        for state in current_states:
            next_states.update(nfa.transitions.get((state, symbol), []))
        current_states = next_states
        if not current_states:
            return False

    return any(state in nfa.accept_states for state in current_states)

def test_sequence_on_mealy(sequence, mealy_machine):
    """
    Teste une séquence sur une machine de Mealy.
    :param sequence: Séquence d'entrée.
    :param mealy_machine: Instance de la classe MealyMachine.
    :return: La sortie générée par la machine de Mealy.
    """
    current_state = mealy_machine.initial_state
    outputs = []

    for symbol in sequence:
        if (current_state, symbol) in mealy_machine.transitions:
            next_state, output = mealy_machine.transitions[(current_state, symbol)]
            outputs.append(output)
            current_state = next_state
        else:
            return None

    return outputs

def simple_algorithm(mealy_machine, nfa, max_depth):
    """
    Implémente l'algorithme simple pour générer une suite de tests.
    :param mealy_machine: Instance de la classe MealyMachine.
    :param nfa: Instance de la classe NFA.
    :param max_depth: Profondeur maximale des séquences.
    :return: Liste des séquences validées et leurs sorties.
    """
    alphabet = {symbol for (state, symbol) in mealy_machine.transitions.keys()}
    sequences = generate_sequences(alphabet, max_depth)

    valid_sequences = []
    for seq in sequences:
        if is_sequence_accepted_by_nfa(seq, nfa):
            outputs = test_sequence_on_mealy(seq, mealy_machine)
            if outputs is not None:
                valid_sequences.append((seq, outputs))

    return valid_sequences

# Exemple d'utilisation

# Transitions de la machine de Mealy
mealy_transitions = {
    ("a", "x"): ("b", 1),
    ("a", "y"): ("c", 0),
    ("a", "z"): ("c", 1),
    ("b", "x"): ("c", 1),
    ("b", "y"): ("c", 1),
    ("b", "z"): ("c", 1),
    ("c", "x"): ("a", 1),
    ("c", "y"): ("a", 1),
    ("c", "z"): ("a", 1),
}

# Initialiser la machine de Mealy
mealy_machine = MealyMachine(mealy_transitions, "a")

# Transitions du NFA
nfa_transitions = {
    ("a", "x"): ["b", "c"],
    ("a", "y"): ["b"],
    ("b", "z"): ["c"],
    ("c", "x"): ["a"],
    ("c", "y"): ["b"],
}

# Initialiser le NFA
nfa = NFA(nfa_transitions, "a", ["c"])

# Exécuter l'algorithme simple
max_depth = 2
results = simple_algorithm(mealy_machine, nfa, max_depth)

# Afficher les résultats
print("Suite de tests générée par l'algorithme simple :")
for seq, outputs in results:
    print(f"Séquence : {seq}, Sorties : {outputs}")

# Afficher les graphes
mealy_machine.display_graph()
nfa.display_graph()
