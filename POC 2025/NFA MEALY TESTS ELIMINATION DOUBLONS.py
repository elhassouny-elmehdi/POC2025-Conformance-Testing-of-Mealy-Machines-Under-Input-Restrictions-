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

# Génération de tests avec restrictions (NFA)
def generate_restricted_tests(nfa, max_length):
    """
    Génère toutes les séquences acceptées par le NFA jusqu'à une longueur donnée.
    :param nfa: Instance de NFA.
    :param max_length: Longueur maximale des séquences.
    :return: Liste des séquences acceptées.
    """
    tests = []
    for length in range(1, max_length + 1):
        for test in product(nfa.alphabet, repeat=length):
            if nfa.is_accepted(test):
                tests.append(list(test))
    return tests

# Fonction pour exécuter les tests de conformité
def test_mealy_machine_with_restrictions(mealy_machine, test_sequences):
    results = []
    for sequence in test_sequences:
        mealy_machine.reset()  # Réinitialiser la machine à l'état initial
        try:
            outputs = mealy_machine.process_input(sequence)  # Traiter la séquence d'entrée
            results.append((sequence, outputs))
        except ValueError as e:
            results.append((sequence, str(e)))  # Capturer les erreurs si les transitions manquent
    return results

# Implémentation de la méthode Simple
def generate_simple_tests(mealy_machine):
    """
    Génère des tests pour couvrir toutes les transitions possibles dans la machine de Mealy.
    :param mealy_machine: Instance de MealyMachine.
    :return: Liste des séquences couvrant toutes les transitions.
    """
    tests = []
    for (state, input_symbol), (next_state, output) in mealy_machine.transitions.items():
        tests.append([input_symbol])  # Ajouter chaque entrée unique
    return tests

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

# Génération des séquences avec restrictions
tests_with_restrictions = generate_restricted_tests(nfa, max_length=3)

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

# Génération des tests simples pour couvrir toutes les transitions
tests_simple = generate_simple_tests(mealy_machine)

# Filtrer les tests simples avec les restrictions du NFA
tests_simple_with_restrictions = [test for test in tests_simple if nfa.is_accepted(test)]

# Exécuter les tests filtrés sur la machine de Mealy
results_simple_with_restrictions = test_mealy_machine_with_restrictions(mealy_machine, tests_simple_with_restrictions)

# Éliminer les doublons dans les séquences générées avec restrictions
unique_tests_with_restrictions = []
for test in tests_simple_with_restrictions:
    if test not in unique_tests_with_restrictions:
        unique_tests_with_restrictions.append(test)

# Exécuter les tests non redondants
results_simple_unique = test_mealy_machine_with_restrictions(mealy_machine, unique_tests_with_restrictions)

# Afficher les résultats optimisés
print("Tests simples uniques générés avec restrictions :", unique_tests_with_restrictions)
for sequence, output in results_simple_unique:
    print(f"Entrée : {sequence} -> Sortie : {output}")

