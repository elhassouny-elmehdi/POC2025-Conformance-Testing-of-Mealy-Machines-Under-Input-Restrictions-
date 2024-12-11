from graphviz import Digraph

# Définir la classe NFA (Automate Fini Non Déterministe)
class NFA:
    def __init__(self, transitions, init_state, accept_states):
        """
        Initialise le NFA.
        :param transitions: Dictionnaire des transitions sous la forme {(\u00e9tat, entr\u00e9e): [\u00e9tats_suivants]}
        :param init_state: \u00c9tat initial de l'automate
        :param accept_states: Liste des \u00e9tats d'acceptation
        """
        self.transitions = transitions
        self.initial_state = init_state
        self.accept_states = accept_states

    def display_graph(self):
        """G\u00e9n\u00e8re et affiche un graphe du NFA en utilisant Graphviz."""
        dot = Digraph(format="png")  # Initialisation du graphe orient\u00e9

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
            label = ", ".join(labels)  # Combiner les \u00e9tiquettes des transitions
            dot.edge(state, next_state, label=label)

        # Ajouter un style distinct pour l'\u00e9tat initial
        dot.node(self.initial_state, color="red", style="filled", fillcolor="lightgrey")

        # Ajouter un style distinct pour les \u00e9tats d'acceptation
        for accept_state in self.accept_states:
            dot.node(accept_state, shape="doublecircle", color="green")

        # Afficher le graphe
        dot.render("nfa_graph", view=True)  # G\u00e9n\u00e8re un fichier PNG et l'affiche

# Exemple de transitions pour le NFA donn\u00e9
transitions = {
    ("a", "0"): ["c"],
    ("a", "1"): ["b", "c"],
    ("b", "1"): ["c"],
    ("c", "1"): ["a"],
}

# Initialiser le NFA et afficher le graphe
nfa = NFA(transitions, "a", ["c"])
nfa.display_graph()