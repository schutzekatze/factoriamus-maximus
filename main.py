import json
import networkx as nx
import matplotlib.pyplot as plt

import resource as fr # Class for resource obj, containing EVERYTHING

test_resource_parents = []
test_resource_parents.append(fr.Parent("copper-plate", 5))
test_resource_parents.append(fr.Parent("firearm-magazine", 1))
test_resource_parents.append(fr.Parent("steel-plate", 1))

test_resource_children = []
test_resource_children.append(fr.Child(""))

test_resouce_recipe = fr.Recipe(3, 1, test_resource_parents, test_resource_children)
test_resource = fr.ResourceElement(2, 
                                        "piercing-rounds-magazine",
                                        "Piercing rounds magazine",
                                        "Combat",
                                        "Combat",
                                        test_resouce_recipe
                                        )


def resources_prep4viz(resources_input_path, resources_output_path):

    with open(resources_input_path, 'r') as json_file:
        resources = json.load(json_file)

    number_ids = []
    name_ids = []
    full_names = []
    resource_types = []
    resource_categories = []
    recipe_times = []
    recipe_yields = []
    recipe_ingredients = []
    resource_parents = []
    parent_children_pairs = {}

    for i, resource in enumerate(resources, 1):

        number_ids.append(i)
        name_ids.append(resource["id"])
        parent_children_pairs[resource["id"]] = []
        full_names.append(resource["name"])
        resource_types.append(resource["type"])
        resource_categories.append(resource["category"])
        recipe_times.append(resource["recipe"]["time"])
        recipe_yields.append(resource["recipe"]["yield"])
        recipe_ingredients.append(resource["recipe"]["ingredients"])

        resource_parents_set = []
        for parents in resource["recipe"]["ingredients"]:
            resource_parents_set.append(parents["id"])
        resource_parents.append(resource_parents_set)


    for i, resource in enumerate(resources):
        for parent in resource_parents[i]:
            parent_children_pairs[parent].append(resource["id"])

    resource_objects = []
    for i, resource in enumerate(resources):
        
        resource_object_parents = []
        for ingredient in recipe_ingredients[i]:
            resource_object_parents.append(fr.Parent(ingredient["id"],
                                                    ingredient["amount"]))
        
        resource_object_children = []
        for child in parent_children_pairs[resource["id"]]:
            resource_object_children.append(fr.Child(child))

        resource_object_recipe = fr.Recipe(recipe_times[i],
                                        recipe_yields[i],
                                        resource_object_parents,
                                        resource_object_children)

        resource_object = fr.ResourceElement(
            number_ids[i],
            name_ids[i],
            full_names[i],
            resource_types[i],
            resource_categories[i],
            resource_object_recipe
            )
        
        resource_objects.append(resource_object.toJSON())

    with open(resources_output_path, 'w') as out_file:
        json.dump(resource_objects, out_file)

    return resources


def build_graph(trimmed_recipes_json_path):

    # G = nx.frucht_graph()
    G = nx.Graph()

    node_labels_mapping = {}

    with open(trimmed_recipes_json_path, 'r') as json_file:
        recipes = json.load(json_file)
    
    for recipe in recipes:
        G.add_node(recipe["id"])
        node_labels_mapping[recipe["id"]] = recipe["name"]
    
    for recipe in recipes:
        for ingredient in recipe["recipe"]["ingredients"]:
            G.add_edge(recipe["id"], ingredient["id"])

    G = nx.relabel_nodes(G, node_labels_mapping)

    return G

resources_prep4viz("raw_recipes.json", "parents_children.json")

# G = build_graph("trimmed_recipes.json")

# nx.draw_kamada_kawai(G)
# positions = nx.kamada_kawai_layout(G)

# nx.draw_networkx_labels(G, positions)
# nx.draw_networkx_edges(G, positions, width=0.25, edge_color='grey')

# plt.show()