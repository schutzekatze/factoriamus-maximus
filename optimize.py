import json
import matplotlib.pyplot as plt
import networkx as nx
import subprocess

"""
Process the raw JSON, clean up and add IDs as numbers
"""
def recipes_prep4viz(recipes_input_path, recipes_output_path):

    with open(recipes_input_path, 'r') as json_file:
        recipes = json.load(json_file)

    # Populate useful_data with the fields we need from the JSON:
    # id, name, type and recipe
    # ---
    # Open Q: is this even necessary?
    for i, recipe in enumerate(recipes, 1):
        recipe["id_number"] = i
        del recipe["wiki_link"]
        del recipe["category"]

    visualizable_recipes = recipes

    with open(recipes_output_path, 'w') as out_file:
        json.dump(visualizable_recipes, out_file)

    return visualizable_recipes


def build_graph(trimmed_recipes_json_path):

    # G = nx.frucht_graph()
    G = nx.DiGraph()

    node_labels_mapping = {}

    with open(trimmed_recipes_json_path, 'r') as json_file:
        recipes = json.load(json_file)
    
    for recipe in recipes:
        G.add_node(recipe["id"])
        node_labels_mapping[recipe["id"]] = recipe["name"]
    
    for recipe in recipes:
        for ingredient in recipe["recipe"]["ingredients"]:
            G.add_edge(ingredient["id"], recipe["id"])

    G = nx.relabel_nodes(G, node_labels_mapping)

    return G


# recipes_prep4viz("raw_recipes.json", "trimmed_recipes.json")

G = build_graph("trimmed_recipes.json")

pydot_graph = nx.drawing.nx_pydot.to_pydot(G)
pydot_graph.set_strict(False)
pydot_graph.set_concentrate(True)
pydot_graph.set_rankdir("LR")
pydot_graph.set_name("factorio")
pydot_graph.write("graph.dot", prog='dot')
subprocess.run(['dot', '-T', 'png', '-O', 'graph.dot'])

#nx.draw_shell(G)
#positions = nx.shell_layout(G)

#nx.draw_networkx_labels(G, positions)
#nx.draw_networkx_edges(G, positions, width=0.25, edge_color='grey')

#plt.show()