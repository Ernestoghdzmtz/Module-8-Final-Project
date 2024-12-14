class Item:
    def __init__(self, name, sku, category, price, quantity):
        self.name = name
        self.sku = sku
        self.category = category
        self.price = price
        self.quantity = quantity

    def update_stock(self, amount):
        self.quantity += amount

    def __str__(self):
        return f"{self.name} (SKU: {self.sku}, Category: {self.category}, Price: {self.price}, Quantity: {self.quantity})"


class Category:
    def __init__(self, name):
        self.name = name
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def __str__(self):
        return f"Category: {self.name}, Items: {len(self.items)}"


class Transaction:
    def __init__(self, transaction_id, sku, quantity, transaction_type):
        self.transaction_id = transaction_id
        self.sku = sku
        self.quantity = quantity
        self.transaction_type = transaction_type

    def record_transaction(self):
        return f"Transaction {self.transaction_id}: {self.transaction_type} {self.quantity} units of {self.sku}."
