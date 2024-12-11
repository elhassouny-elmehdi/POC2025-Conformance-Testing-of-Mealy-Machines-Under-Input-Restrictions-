from graphviz import Digraph# Automate NFA
def display_nfa():
    dot = Digraph(format="png")
    dot.attr(rankdir="LR")  # Disposer les états horizontalement

    # Ajouter les états
    dot.node("a", shape="circle", style="filled", fillcolor="lightblue", color="red")  # Initial
    dot.node("b", shape="circle", style="filled", fillcolor="lightblue")
    dot.node("c", shape="doublecircle", style="filled", fillcolor="lightblue", color="green")  # Acceptant

    # Ajouter les transitions
    dot.edge("a", "b", label="1")
    dot.edge("a", "c", label="0, 1")
    dot.edge("b", "c", label="1")
    dot.edge("c", "a", label="1")

    # Sauvegarder et afficher
    dot.render("nfa", view=True)

display_nfa()
