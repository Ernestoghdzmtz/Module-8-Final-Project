import os
import json
from models import Item, Category

# Define the directory and filename for storing the JSON file
DATA_DIR = "D:\\Copia Ernesto06262019\\Documents\\Ivy Tech\\4 Software Development using Pyt\\Module 6\\Projecto Final\\Projecto final V2"  # Change this to your desired folder
JSON_FILE = os.path.join(DATA_DIR, "inventory.json")

# Asegúrate de que el directorio exista
os.makedirs(DATA_DIR, exist_ok=True)

def save_data(categories, items):
    """Guarda las categorías e ítems en un archivo JSON."""
    data = {
        "categories": {name: [item.sku for item in category.items] for name, category in categories.items()},
        "items": {sku: {
            "name": item.name,
            "category": item.category,
            "price": item.price,
            "quantity": item.quantity
        } for sku, item in items.items()}
    }
    with open(JSON_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_data():
    """Carga las categorías e ítems desde un archivo JSON."""
    categories = {}
    items = {}
    try:
        with open(JSON_FILE, "r") as f:
            data = json.load(f)
        for name, item_skus in data["categories"].items():
            category = Category(name)
            categories[name] = category
            for sku in item_skus:
                if sku in data["items"]:
                    item_data = data["items"][sku]
                    item = Item(
                        name=item_data["name"],
                        sku=sku,
                        category=item_data["category"],
                        price=item_data["price"],
                        quantity=item_data["quantity"]
                    )
                    items[sku] = item
                    category.add_item(item)
    except FileNotFoundError:
        print(f"{JSON_FILE} not found. Starting with an empty inventory.")
    return categories, items