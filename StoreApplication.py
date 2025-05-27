import tkinter as tk
from tkinter import ttk, messagebox

class StoreApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("Store - Product List")

        self.cash_register = 0.0
        self.products = [
            {"name": "Whiteboard Marker", "price": 1.50, "stock": 85},
            {"name": "Whiteboard Eraser", "price": 5.0, "stock": 45},
            {"name": "Black Pen", "price": 1.50, "stock": 100},
            {"name": "Blue Pen", "price": 1.50, "stock": 100},
            {"name": "Red Pen", "price": 1.50, "stock": 100}    
               ]

        self.tree = ttk.Treeview(self.root, columns=("Name", "Price", "Stock"), show="headings")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Price", text="Price")
        self.tree.heading("Stock", text="Stock")
        self.tree.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

        self.load_products()

        self.view_button = tk.Button(self.root, text="View", command=self.view_product)
        self.view_button.grid(row=1, column=0, padx=10, pady=10)

        self.cash_label = tk.Label(self.root, text=f"Cash Register: $ {self.cash_register:.2f}")
        self.cash_label.grid(row=1, column=1, padx=10, pady=10)

    def load_products(self):
        for product in self.products:
            self.tree.insert("", tk.END, values=(product["name"], f"${product['price']:.2f}", product["stock"]))

    def view_product(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showerror("Error", "No product selected.")
            return

        product_details = self.tree.item(selected_item, "values")
        product_name = product_details[0]

        for product in self.products:
            if product["name"] == product_name:
                self.show_product_window(product)
                break

    def show_product_window(self, product):
        product_window = tk.Toplevel(self.root)
        product_window.title(f"Product Details - {product['name']}")

        tk.Label(product_window, text=f"Product Name: {product['name']}").grid(row=0, column=0, padx=10, pady=10)
        tk.Label(product_window, text=f"Price: $ {product['price']:.2f}").grid(row=1, column=0, padx=10, pady=10)
        tk.Label(product_window, text=f"Stock: {product['stock']}").grid(row=2, column=0, padx=10, pady=10)

        # Quantity to sell
        tk.Label(product_window, text="Quantity to sell:").grid(row=3, column=0, padx=10, pady=10)
        quantity_entry = tk.Entry(product_window)
        quantity_entry.grid(row=3, column=1, padx=10, pady=10)

        # Sell button
        sell_button = tk.Button(product_window, text="Sell", command=lambda: self.sell_product(product, quantity_entry, product_window))
        sell_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    def sell_product(self, product, quantity_entry, window):
        try:
            quantity = int(quantity_entry.get())
            if quantity <= 0:
                raise ValueError("Invalid quantity.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return

        if quantity > product["stock"]:
            messagebox.showerror("Error", "Not enough stock.")
        else:
            product["stock"] -= quantity
            self.cash_register += product["price"] * quantity
            messagebox.showinfo("Success", f"Sold {quantity} {product['name']} for ${product['price'] * quantity:.2f}")
            self.update_table()
            self.cash_label.config(text=f"Cash Register: $ {self.cash_register:.2f}")
            window.destroy()

    def update_table(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        self.load_products()

if __name__ == "__main__":
    root = tk.Tk()
    app = StoreApplication(root)
    root.mainloop()
    
    
