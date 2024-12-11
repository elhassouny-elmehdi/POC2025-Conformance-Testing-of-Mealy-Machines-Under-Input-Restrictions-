from graphviz import Digraph

# Produit de la Mealy machine et du NFA
def display_product_automaton():
    dot = Digraph(format="png")
    dot.attr(rankdir="LR")  # Disposer les états horizontalement

    # Ajouter les états
    states = ["s,a", "s,b", "s,c", "t,a", "t,b", "t,c"]
    for state in states:
        if state == "s,a":  # État initial
            dot.node(state, shape="circle", style="filled", fillcolor="lightblue", color="red")
        else:
            dot.node(state, shape="circle", style="filled", fillcolor="lightblue")

    # Ajouter les transitions
    transitions = {
        "s,a": [("t,b", "1/1"), ("t,c", "0/1"), ("t,c", "1/1")],
        "s,b": [("t,c", "1/1")],
        "s,c": [("t,a", "1/1")],
        "t,a": [("s,b", "1/1"), ("s,c", "0/1"), ("s,c", "1/1")],
        "t,b": [("s,c", "1/1")],
        "t,c": [("s,a", "1/1")]
    }

    # Regrouper les transitions entre les mêmes états
    grouped_transitions = {}
    for state, edges in transitions.items():
        for next_state, label in edges:
            if (state, next_state) not in grouped_transitions:
                grouped_transitions[(state, next_state)] = []
            grouped_transitions[(state, next_state)].append(label)

    for (state, next_state), labels in grouped_transitions.items():
        combined_label = ", ".join(labels)
        dot.edge(state, next_state, label=combined_label)

    # Sauvegarder et afficher
    dot.render("product_automaton", view=True)

display_product_automaton()