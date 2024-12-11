import time
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

# Génération de tests simples
def generate_simple_tests(mealy_machine):
    """
    Génère des séquences pour couvrir toutes les transitions possibles de la machine de Mealy.
    :param mealy_machine: Instance de MealyMachine.
    :return: Liste des séquences couvrant toutes les transitions.
    """
    tests = []
    for (state, input_symbol), (next_state, output) in mealy_machine.transitions.items():
        tests.append([input_symbol])  # Ajouter une séquence avec l'entrée unique
    return tests

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

# Validation des méthodes Simple et Complexe
def validate_methods(mealy_machine, max_complex_length):
    """
    Compare les performances des méthodes Simple et Complexe sur la machine de Mealy.
    :param mealy_machine: Instance de MealyMachine.
    :param max_complex_length: Longueur maximale pour les tests complexes.
    :return: Résultats des performances et couverture.
    """
    results = {}

    # Méthode Simple
    start_time = time.time()
    simple_tests = generate_simple_tests(mealy_machine)
    simple_results = execute_tests(mealy_machine, simple_tests)
    simple_time = time.time() - start_time

    # Méthode Complexe
    start_time = time.time()
    complex_tests = generate_complex_tests(mealy_machine, max_complex_length)
    complex_results = execute_tests(mealy_machine, complex_tests)
    complex_time = time.time() - start_time

    # Résumé des performances
    results["simple"] = {
        "tests_generated": len(simple_tests),
        "execution_time": simple_time,
        "transitions_covered": len(simple_tests),  # Méthode simple couvre chaque transition une fois
    }
    results["complex"] = {
        "tests_generated": len(complex_tests),
        "execution_time": complex_time,
        "transitions_covered": len(complex_results),
    }

    # Affichage des résultats
    print("\n=== Validation des Méthodes ===")
    print(f"Simple : {results['simple']}")
    print(f"Complexe : {results['complex']}\n")
    
    return results

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

# Validation sur la machine de Mealy avec k = 3
validation_results = validate_methods(mealy_machine, max_complex_length=3)

# Afficher les détails des résultats
print("Tests Simples (Méthode Simple) :")
for test, output in execute_tests(mealy_machine, generate_simple_tests(mealy_machine)):
    print(f"Entrée : {test} -> Sortie : {output}")

print("\nTests Complexes (Méthode Complexe) :")
for test, output in execute_tests(mealy_machine, generate_complex_tests(mealy_machine, max_length=3)):
    print(f"Entrée : {test} -> Sortie : {output}")
