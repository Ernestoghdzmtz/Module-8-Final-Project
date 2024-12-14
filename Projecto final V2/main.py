import tkinter as tk
from tkinter import ttk
from data_handler import load_data, save_data
from gui_components import create_tabs
from models import Item, Category

categories, items = load_data()

def start_items_tab(tab):
    """Configura la pestaña Items Management."""
    global tree, item_name_entry, sku_entry, category_entry, price_entry, quantity_entry, item_status_label, total_items_label

    tk.Label(tab, text="Item Management", font=("Arial", 16)).pack(pady=10)
    tk.Label(tab, text="Item Name:").pack()
    item_name_entry = tk.Entry(tab, width=30)
    item_name_entry.pack()

    tk.Label(tab, text="SKU:").pack()
    sku_entry = tk.Entry(tab, width=30)
    sku_entry.pack()

    tk.Label(tab, text="Category:").pack()
    category_entry = tk.Entry(tab, width=30)
    category_entry.pack()

    tk.Label(tab, text="Price:").pack()
    price_entry = tk.Entry(tab, width=30)
    price_entry.pack()

    tk.Label(tab, text="Quantity:").pack()
    quantity_entry = tk.Entry(tab, width=30)
    quantity_entry.pack()

    item_status_label = tk.Label(tab, text="")
    item_status_label.pack()

    # Crear el Treeview para mostrar los ítems
    columns = ("Number", "Name", "SKU", "Category", "Price", "Quantity")
    tree = ttk.Treeview(tab, columns=columns, show="headings", height=15)
    tree.pack()

    # Configurar los encabezados
    tree.heading("Number", text="#")
    tree.heading("Name", text="Item Name")
    tree.heading("SKU", text="SKU")
    tree.heading("Category", text="Category")
    tree.heading("Price", text="Price")
    tree.heading("Quantity", text="Quantity")

    # Configurar el ancho y alineación de las columnas
    tree.column("Number", width=50, anchor="center")
    tree.column("Name", width=150, anchor="center")
    tree.column("SKU", width=100, anchor="center")
    tree.column("Category", width=100, anchor="center")
    tree.column("Price", width=100, anchor="center")
    tree.column("Quantity", width=100, anchor="center")

    tk.Button(tab, text="Add Item", command=add_item).pack(pady=5)

    total_items_label = tk.Label(tab, text="Total Items: 0", font=("Arial", 12))
    total_items_label.pack()

    # Iniciar la actualización automática de la tabla
    auto_update_table()

 

def start_category_tab(tab):
    """Configura la pestaña Category Management."""
    tk.Label(tab, text="Category Management", font=("Arial", 16)).pack(pady=10)
    tk.Label(tab, text="Category Name:").pack()
    category_name_entry = tk.Entry(tab, width=30)
    category_name_entry.pack()
    tk.Button(tab, text="Add Category", command=lambda: print("Add Category clicked")).pack(pady=5)

def start_transactions_tab(tab):
    
    global transaction_sku_entry, transaction_quantity_entry, transaction_type_combo, transaction_status_label

    """Configura la pestaña Transactions."""
    tk.Label(tab, text="Transactions", font=("Arial", 16)).pack(pady=10)
    tk.Label(tab, text="SKU:").pack()
    transaction_sku_entry = tk.Entry(tab, width=30)
    transaction_sku_entry.pack()

    tk.Label(tab, text="Quantity:").pack()
    transaction_quantity_entry = tk.Entry(tab, width=30)
    transaction_quantity_entry.pack()

    tk.Label(tab, text="Transaction Type:").pack()
    transaction_type_combo = ttk.Combobox(tab, values=["Sale", "Restock"])
    transaction_type_combo.pack()
    
    tk.Button(tab, text="Record Transaction", command=record_transaction).pack(pady=5)
    transaction_status_label = tk.Label(tab, text="")
    transaction_status_label.pack()
    #tk.Button(tab, text="Record Transaction", command=lambda: print("Transaction Recorded")).pack(pady=5)

# Función para agregar un ítem al inventario
def add_item():
    """Add a new item to the inventory."""
    global items, categories

    # Recuperar los valores de los campos de entrada
    name = item_name_entry.get()
    sku = sku_entry.get()
    category_name = category_entry.get()
    price = price_entry.get()
    quantity = quantity_entry.get()

    # Validar entradas
    if not name or not sku or not category_name or not price or not quantity:
        item_status_label.config(text="All fields are required.")
        return

    try:
        price = float(price)
        quantity = int(quantity)
    except ValueError:
        item_status_label.config(text="Price must be a number and Quantity an integer.")
        return

    # Crear la categoría si no existe
    if category_name not in categories:
        categories[category_name] = Category(category_name)

    # Crear un nuevo ítem y agregarlo al inventario
    new_item = Item(name, sku, category_name, price, quantity)
    items[sku] = new_item
    categories[category_name].add_item(new_item)

    # Actualizar la etiqueta de estado y limpiar los campos de entrada
    item_status_label.config(text=f"Item '{name}' added successfully!")
    item_name_entry.delete(0, tk.END)
    sku_entry.delete(0, tk.END)
    category_entry.delete(0, tk.END)
    price_entry.delete(0, tk.END)
    quantity_entry.delete(0, tk.END)

    # Guardar los datos actualizados
    save_data()

def auto_update_table():
    """Automatically refresh the inventory display every 3 seconds."""
    # Limpiar el contenido actual de la tabla
    for row in tree.get_children():
        tree.delete(row)

    # Rellenar la tabla con los datos del inventario
    for idx, (sku, item) in enumerate(items.items(), start=1):
        tree.insert("", tk.END, values=(idx, item.name, item.sku, item.category, f"${item.price:.2f}", item.quantity))

    # Actualizar el total de ítems en la etiqueta
    total_items_label.config(text=f"Total Items: {len(items)}")

    # Programar la próxima actualización en 3 segundos
    tree.after(3000, auto_update_table)


def record_transaction():
    """Record a transaction for an item (sale or restock)."""
    global items, items_text

    # Obtener los valores de entrada
    sku = transaction_sku_entry.get()
    quantity = transaction_quantity_entry.get()
    transaction_type = transaction_type_combo.get()

    # Validar que los campos estén llenos
    if not sku or not quantity or not transaction_type:
        transaction_status_label.config(text="All fields are required.")
        return

    try:
        quantity = int(quantity)  # Validar que la cantidad sea un número entero
    except ValueError:
        transaction_status_label.config(text="Quantity must be an integer.")
        return

    # Verificar si el SKU existe en el inventario
    if sku not in items:
        transaction_status_label.config(text=f"Item with SKU '{sku}' does not exist.")
        return

    item = items[sku]  # Recuperar el ítem correspondiente

    # Manejar transacciones de venta
    if transaction_type == "Sale":
        if item.quantity < quantity:  # Validar si hay suficiente stock
            transaction_status_label.config(text=f"Not enough stock for SKU '{sku}'.")
            return
        item.update_stock(-quantity)  # Reducir el stock
        transaction_status_label.config(text=f"Sold {quantity} units of '{sku}'.")

    # Manejar transacciones de reabastecimiento
    elif transaction_type == "Restock":
        item.update_stock(quantity)  # Incrementar el stock
        transaction_status_label.config(text=f"Restocked {quantity} units of '{sku}'.")

    # Guardar los datos actualizados
    save_data()

    # Actualizar automáticamente el inventario mostrado
    items_text.delete(1.0, tk.END)
    for sku, item in items.items():
        items_text.insert(
            tk.END,
            f"Name: {item.name}, SKU: {item.sku}, Category: {item.category}, Price: ${item.price:.2f}, Quantity: {item.quantity}\n"
        )

    # Limpiar los campos de entrada
    transaction_sku_entry.delete(0, tk.END)
    transaction_quantity_entry.delete(0, tk.END)
    transaction_type_combo.set("")



def main():
    """Punto de entrada del programa."""
    root = tk.Tk()
    root.title("Inventory Management System")
    root.geometry("900x700")

    # Configura las pestañas
    create_tabs(root, {
        "items_tab": start_items_tab,
        "category_tab": start_category_tab,
        "transactions_tab": start_transactions_tab
    })

    root.mainloop()
    save_data(categories, items)

if __name__ == "__main__":
    main()
