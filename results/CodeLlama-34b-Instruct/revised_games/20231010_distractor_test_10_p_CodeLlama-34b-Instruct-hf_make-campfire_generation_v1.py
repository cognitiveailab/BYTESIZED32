import random

def make_campfire(materials):
    # Check if the materials are valid
    if not isinstance(materials, list):
        raise ValueError("Materials must be a list")

    # Check if the materials are empty
    if not materials:
        raise ValueError("Materials list cannot be empty")

    # Check if the materials contain only strings
    if not all(isinstance(material, str) for material in materials):
        raise ValueError("Materials list can only contain strings")

    # Check if the materials contain only valid material names
    valid_materials = ["wood", "stone", "leaves", "twigs"]
    if not all(material in valid_materials for material in materials):
        raise ValueError("Materials list can only contain valid material names")

    # Create the campfire
    campfire = {"name": "Campfire", "materials": materials}

    return campfire

# Test the function
materials = ["wood", "stone", "leaves", "twigs"]
campfire = make_campfire(materials)
print(campfire)
