from itertools import product

# Classe pour la machine de Mealy
class MealyMachine:
    def __init__(self, transitions, initial_state):
        """
        Initialise une machine de Mealy.
        :param transitions: Dictionnaire des transitions { (state, input): (next_state, output) }.
        :param initial_state: État initial.
        """
        self.transitions = transitions
        self.initial_state = initial_state
        self.current_state = initial_state

    def reset(self):
        """Réinitialise l'état courant à l'état initial."""
        self.current_state = self.initial_state

    def process_input(self, input_sequence):
        """
        Traite une séquence d'entrées et retourne les sorties correspondantes.
        :param input_sequence: Liste des entrées.
        :return: Liste des sorties.
        """
        outputs = []
        for input_symbol in input_sequence:
            if (self.current_state, input_symbol) in self.transitions:
                next_state, output = self.transitions[(self.current_state, input_symbol)]
                outputs.append(output)
                self.current_state = next_state
            else:
                raise ValueError(f"Transition inconnue pour ({self.current_state}, {input_symbol})")
        return outputs

# Classe pour le NFA
class NFA:
    def __init__(self, states, alphabet, transitions, initial_state, accepting_states):
        """
        Initialise un NFA.
        :param states: Liste des états.
        :param alphabet: Alphabet des entrées.
        :param transitions: Fonction de transition {(state, input): {next_states}}.
        :param initial_state: État initial.
        :param accepting_states: Ensemble des états acceptants.
        """
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
        return len(current_states & self.accepting_states) > 0

# Génération de tests complexes (k-complètes)
def generate_complex_tests(mealy_machine, max_length):
    """
    Génère des séquences k-complètes pour couvrir toutes les combinaisons jusqu'à une longueur donnée.
    :param mealy_machine: Instance de MealyMachine.
    :param max_length: Longueur maximale des séquences.
    :return: Liste des séquences k-complètes.
    """
    # Extraire l'alphabet des entrées
    inputs = {key[1] for key in mealy_machine.transitions.keys()}
    tests = []
    for length in range(1, max_length + 1):
        tests.extend(product(inputs, repeat=length))
    return [list(test) for test in tests]

# Fonction pour exécuter les tests de conformité
def execute_tests(mealy_machine, test_sequences):
    """
    Exécute les tests sur la machine de Mealy et retourne les résultats.
    :param mealy_machine: Instance de MealyMachine.
    :param test_sequences: Liste des séquences à tester.
    :return: Liste des résultats (entrée -> sortie).
    """
    results = []
    for sequence in test_sequences:
        mealy_machine.reset()  # Réinitialiser la machine à l'état initial
        try:
            outputs = mealy_machine.process_input(sequence)  # Traiter la séquence d'entrée
            results.append((sequence, outputs))
        except ValueError as e:
            results.append((sequence, str(e)))  # Capturer les erreurs si les transitions manquent
    return results

# Définition du NFA
nfa_states = ["a", "b", "c"]
nfa_alphabet = ["x", "y", "z"]
nfa_transitions = {
    ("a", "x"): {"c"},
    ("a", "y"): {"b", "c"},
    ("b", "y"): {"c"},
    ("c", "y"): {"a"},
}
nfa_initial_state = "a"
nfa_accepting_states = {"c"}
nfa = NFA(nfa_states, nfa_alphabet, nfa_transitions, nfa_initial_state, nfa_accepting_states)

# Définition de la machine de Mealy
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
mealy_initial_state = "a"
mealy_machine = MealyMachine(mealy_transitions, mealy_initial_state)

# Génération des tests complexes (k-complètes) avec une longueur maximale de 3
complex_tests = generate_complex_tests(mealy_machine, max_length=3)

# Exécuter les tests complexes sur la machine de Mealy
results_complex = execute_tests(mealy_machine, complex_tests)

# Afficher les résultats des tests complexes
print("Tests Complexes :")
for test, output in results_complex:
    print(f"Entrée : {test} -> Sortie : {output}")
