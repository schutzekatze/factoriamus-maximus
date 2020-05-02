from typing import List
import json

class Child:
    id: str

    def __init__(self, id: str) -> None:
        self.id = id


class Parent:
    id: str
    amount: float

    def __init__(self, id: str, amount: float) -> None:
        self.id = id
        self.amount = amount


class Recipe:
    time: float
    recipe_yield: float
    parents: List[Parent]
    children: List[Child]

    def __init__(self, time: float, recipe_yield: float, parents: List[Parent], children: List[Child]) -> None:
        self.time = time
        self.recipe_yield = recipe_yield
        self.parents = parents
        self.children = children


class ResourceElement:
    number_id: int
    name_id: str
    full_name: str
    type: str
    category: str
    recipe: Recipe

    def __init__(self, number_id: int, name_id: str, full_name: str, type: str, category: str, recipe: Recipe) -> None:
        self.number_id = number_id
        self.name_id = name_id
        self.full_name = full_name
        self.type = type
        self.category = category
        self.recipe = recipe

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)