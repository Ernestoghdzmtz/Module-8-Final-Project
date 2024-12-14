import tkinter as tk
from tkinter import ttk

def create_tabs(root, handlers):
    """Crea las pestañas de la aplicación."""
    notebook = ttk.Notebook(root)

    # Crea las pestañas
    items_tab = ttk.Frame(notebook)
    category_tab = ttk.Frame(notebook)
    transactions_tab = ttk.Frame(notebook)

    # Añade las pestañas al notebook
    notebook.add(items_tab, text="Items Management")
    notebook.add(category_tab, text="Category Management")
    notebook.add(transactions_tab, text="Transactions")

    notebook.pack(expand=1, fill="both")

    # Configura cada pestaña con el manejador correspondiente
    handlers["items_tab"](items_tab)
    handlers["category_tab"](category_tab)
    handlers["transactions_tab"](transactions_tab)
