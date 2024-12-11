from graphviz import Digraph

# Machine de Mealy
def display_mealy_machine():
    dot = Digraph(format="png")
    dot.attr(rankdir="LR")  # Disposer les états horizontalement

    # Ajouter les états
    dot.node("s", shape="circle", style="filled", fillcolor="lightblue")
    dot.node("t", shape="circle", style="filled", fillcolor="lightblue")

    # Ajouter les transitions
    dot.edge("s", "t", label="0/1, 1/1")
    dot.edge("t", "s", label="0/0, 1/1")

    # Sauvegarder et afficher
    dot.render("mealy_machine", view=True)

display_mealy_machine()
