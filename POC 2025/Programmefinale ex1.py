import time
from itertools import product
from graphviz import Digraph
import matplotlib.pyplot as plt

# Classe pour la machine de Mealy
class MealyMachine:
    def __init__(self, transitions, initial_state):
        self.transitions = transitions
        self.initial_state = initial_state
        self.current_state = initial_state

    def reset(self):
        """Réinitialise l'état courant à l'état initial."""
        self.current_state = self.initial_state

    def process_input(self, input_sequence):
        """
        Traite une séquence d'entrées et retourne les sorties correspondantes,
        ainsi que l'évolution des états.
        :param input_sequence: Liste des entrées.
        :return: Tuple (liste des sorties, liste des états visités).
        """
        outputs = []
        states = [self.current_state]
        for input_symbol in input_sequence:
            if (self.current_state, input_symbol) in self.transitions:
                next_state, output = self.transitions[(self.current_state, input_symbol)]
                outputs.append(output)
                self.current_state = next_state
                states.append(next_state)
            else:
                raise ValueError(f"Transition inconnue pour ({self.current_state}, {input_symbol})")
        return outputs, states

    def display_graph(self, output_file="mealy_machine"):
        """Affiche un graphe de la machine de Mealy."""
        dot = Digraph(format="png")
        grouped_transitions = {}
        for (state, input_symbol), (next_state, output) in self.transitions.items():
            if (state, next_state) not in grouped_transitions:
                grouped_transitions[(state, next_state)] = []
            grouped_transitions[(state, next_state)].append(f"{input_symbol}/{output}")
        
        for (state, next_state), labels in grouped_transitions.items():
            dot.edge(state, next_state, label=", ".join(labels))
        dot.node(self.initial_state, color="red", style="filled", fillcolor="lightgrey")
        dot.render(output_file, view=True)

# Classe pour le NFA
class NFA:
    def __init__(self, states, alphabet, transitions, initial_state, accepting_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.initial_state = initial_state
        self.accepting_states = accepting_states

    def is_accepted(self, input_sequence):
        """
        Vérifie si une séquence est acceptée par le NFA.
        :param input_sequence: Séquence d'entrée.
        :return: True si acceptée, False sinon.
        """
        current_states = {self.initial_state}
        for input_symbol in input_sequence:
            next_states = set()
            for state in current_states:
                if (state, input_symbol) in self.transitions:
                    next_states.update(self.transitions[(state, input_symbol)])
            current_states = next_states
        return len(current_states & set(self.accepting_states)) > 0

    def display_graph(self, output_file="nfa_graph"):
        """Affiche un graphe du NFA."""
        dot = Digraph(format="png")
        grouped_transitions = {}
        for (state, input_symbol), next_states in self.transitions.items():
            for next_state in next_states:
                if (state, next_state) not in grouped_transitions:
                    grouped_transitions[(state, next_state)] = []
                grouped_transitions[(state, next_state)].append(input_symbol)
        
        for (state, next_state), labels in grouped_transitions.items():
            dot.edge(state, next_state, label=", ".join(labels))
        dot.node(self.initial_state, color="red", style="filled", fillcolor="lightgrey")
        for state in self.accepting_states:
            dot.node(state, shape="doublecircle", color="green")
        dot.render(output_file, view=True)

# Génération de tests avec et sans restrictions
def generate_tests(transitions, max_length):
    """Génère toutes les combinaisons possibles d'entrées jusqu'à une longueur donnée."""
    inputs = {key[1] for key in transitions.keys()}
    tests = []
    for length in range(1, max_length + 1):
        tests.extend(product(inputs, repeat=length))
    return [list(test) for test in tests]

def generate_restricted_tests(nfa, max_length):
    """Génère toutes les séquences acceptées par le NFA jusqu'à une longueur donnée."""
    tests = []
    for length in range(1, max_length + 1):
        for test in product(nfa.alphabet, repeat=length):
            if nfa.is_accepted(test):
                tests.append(list(test))
    return tests

# Fonction pour exécuter les tests sur une machine de Mealy
def execute_tests(mealy_machine, test_sequences):
    """
    Exécute les tests sur la machine de Mealy et retourne les résultats.
    :param mealy_machine: Instance de MealyMachine.
    :param test_sequences: Liste des séquences à tester.
    :return: Liste des résultats (entrée -> sortie, états visités).
    """
    results = []
    for sequence in test_sequences:
        mealy_machine.reset()
        try:
            outputs, states = mealy_machine.process_input(sequence)
            results.append((sequence, outputs, states))
        except ValueError as e:
            results.append((sequence, str(e), []))
    return results

# Méthodes Simple et Complexe pour k-completes
def simple_method(mealy_machine):
    """Génère des séquences couvrant toutes les transitions."""
    tests = []
    for (state, input_symbol), (next_state, output) in mealy_machine.transitions.items():
        tests.append([input_symbol])
    return tests

def complex_method(mealy_machine, max_length):
    """Génère des séquences k-complètes jusqu'à une longueur donnée."""
    inputs = {key[1] for key in mealy_machine.transitions.keys()}
    tests = []
    for length in range(1, max_length + 1):
        tests.extend(product(inputs, repeat=length))
    return [list(test) for test in tests]

# Comparaison des performances
def compare_methods(mealy_machine, nfa, max_length):
    """Compare les méthodes Simple et Complexe."""
    results = {}

    # Méthode Simple
    start_time = time.time()
    simple_tests = simple_method(mealy_machine)
    simple_results = execute_tests(mealy_machine, simple_tests)
    simple_time = time.time() - start_time

    # Méthode Complexe
    start_time = time.time()
    complex_tests = generate_restricted_tests(nfa, max_length)
    complex_results = execute_tests(mealy_machine, complex_tests)
    complex_time = time.time() - start_time

    results["simple"] = {
        "tests": simple_tests,
        "results": simple_results,
        "time": simple_time,
    }
    results["complex"] = {
        "tests": complex_tests,
        "results": complex_results,
        "time": complex_time,
    }
    return results

# Visualisation des performances
def visualize_performance(results):
    """Affiche les temps d'exécution des deux méthodes."""
    methods = ["simple", "complex"]
    times = [results[method]["time"] for method in methods]

    plt.bar(methods, times, color=['blue', 'green'])
    plt.title("Comparaison des performances des méthodes")
    plt.xlabel("Méthode")
    plt.ylabel("Temps d'exécution (s)")
    plt.show()

# Exemple d'utilisation
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
nfa_transitions = {
    ("a", "x"): ["b", "c"],
    ("a", "y"): ["b"],
    ("b", "z"): ["c"],
    ("c", "x"): ["a"], 
    ("c", "y"): ["b"],
}
nfa = NFA(["a", "b", "c"], ["x", "y", "z"], nfa_transitions, "a", ["c"])
mealy_machine = MealyMachine(mealy_transitions, "a")

# Comparer les méthodes
results = compare_methods(mealy_machine, nfa, max_length=3)

# Visualiser les performances
visualize_performance(results)

# Afficher les résultats
print("Méthode Simple:")
for test, output, states in results["simple"]["results"]:
    print(f"Entrée : {test} -> Sortie : {output}, États visités : {states}")

print("\nMéthode Complexe:")
for test, output, states in results["complex"]["results"]:
    print(f"Entrée : {test} -> Sortie : {output}, États visités : {states}")

# Afficher les graphes
mealy_machine.display_graph()
nfa.display_graph()
