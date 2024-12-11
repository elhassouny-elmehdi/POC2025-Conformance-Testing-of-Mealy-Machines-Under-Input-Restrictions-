from graphviz import Digraph

# Définir la classe MealyMachine
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
        dot = Digraph(format="png")  # Initialisation du graphe orienté

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

        # Ajout d'un style pour l'état initial
        dot.node(self.initial_state, color="red", style="filled", fillcolor="lightgrey")

        # Afficher le graphe
        dot.render("mealy_machine", view=True)  # Génère un fichier PNG et l'affiche

# Exemple de transitions
transitions = {
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

# Initialiser la machine de Mealy et afficher le graphe
mealy_machine = MealyMachine(transitions, "a")
mealy_machine.display_graph()
