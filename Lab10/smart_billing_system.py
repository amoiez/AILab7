import tkinter as tk
from tkinter import messagebox
from datetime import datetime

class SmartBillingSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Billing System")
        self.root.geometry("600x700")
        
        self.products = {
            "Milk": {"price": 120, "suggestion": "Bread"},
            "Bread": {"price": 100, "suggestion": "Eggs"},
            "Eggs": {"price": 200, "suggestion": "Milk"},
            "Apple": {"price": 150, "suggestion": "Banana"},
            "Banana": {"price": 100, "suggestion": "Apple"},
            "Tea": {"price": 50, "suggestion": "Sandwich"},
            "Coffee": {"price": 80, "suggestion": "Sandwich"},
            "Sandwich": {"price": 150, "suggestion": "Juice"}
        }

        self.create_widgets()

    def create_widgets(self):
        # Title
        title_label = tk.Label(self.root, text="Smart Billing System", font=("Arial", 18, "bold"), pady=10)
        title_label.pack()

        # Input Frame
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=10)

        # Labels & Entries
        tk.Label(input_frame, text="Customer Name:", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.name_entry = tk.Entry(input_frame, font=("Arial", 12))
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(input_frame, text="Contact Number:", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.contact_entry = tk.Entry(input_frame, font=("Arial", 12))
        self.contact_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(input_frame, text="Item Name:", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.item_entry = tk.Entry(input_frame, font=("Arial", 12))
        self.item_entry.grid(row=2, column=1, padx=10, pady=5)
        tk.Label(input_frame, text="(e.g., Milk, Bread, Tea, Coffee)", font=("Arial", 9)).grid(row=3, column=1, sticky="w")

        tk.Label(input_frame, text="Item Price:", font=("Arial", 12)).grid(row=4, column=0, padx=10, pady=5, sticky="e")
        self.price_entry = tk.Entry(input_frame, font=("Arial", 12))
        self.price_entry.grid(row=4, column=1, padx=10, pady=5)

        tk.Label(input_frame, text="Quantity:", font=("Arial", 12)).grid(row=5, column=0, padx=10, pady=5, sticky="e")
        self.quantity_entry = tk.Entry(input_frame, font=("Arial", 12))
        self.quantity_entry.grid(row=5, column=1, padx=10, pady=5)

        # Buttons Frame
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Generate Receipt", font=("Arial", 12, "bold"), bg="green", fg="white", command=self.generate_receipt).grid(row=0, column=0, padx=10)
        tk.Button(button_frame, text="Clear", font=("Arial", 12, "bold"), bg="orange", fg="white", command=self.clear_fields).grid(row=0, column=1, padx=10)
        tk.Button(button_frame, text="Exit", font=("Arial", 12, "bold"), bg="red", fg="white", command=self.exit_app).grid(row=0, column=2, padx=10)

        # Output Frame
        output_frame = tk.Frame(self.root)
        output_frame.pack(pady=10)
        
        self.receipt_text = tk.Text(output_frame, width=60, height=15, font=("Courier", 10))
        self.receipt_text.pack()

    def generate_receipt(self):
        # 1. Fetch user inputs
        name = self.name_entry.get().strip()
        contact = self.contact_entry.get().strip()
        item = self.item_entry.get().strip().title()
        price_str = self.price_entry.get().strip()
        quantity_str = self.quantity_entry.get().strip()

        # 2. Input Validation
        if not name or not contact or not item or not price_str or not quantity_str:
            messagebox.showerror("Validation Error", "All fields are required!")
            return

        if not contact.isdigit():
            messagebox.showerror("Validation Error", "Contact number must contain only digits!")
            return

        try:
            price = float(price_str)
            quantity = int(quantity_str)
        except ValueError:
            messagebox.showerror("Validation Error", "Price must be a number and Quantity must be an integer!")
            return

        if price <= 0 or quantity <= 0:
            messagebox.showerror("Validation Error", "Price and Quantity must be greater than zero!")
            return

        # 3. AI-Based Decision Rules & Billing Logic
        subtotal = price * quantity
        discount_percent = 0
        discount_reason = ""

        # AI Rule 1: Auto-apply discount based on rules
        if quantity >= 5:
            discount_percent = 10
            discount_reason = "10% Bulk Discount (>= 5 items)"
        elif subtotal >= 1000:
            discount_percent = 5
            discount_reason = "5% High Value Discount (>= $1000)"

        discount_amount = (subtotal * discount_percent) / 100
        tax = (subtotal - discount_amount) * 0.05 # 5% tax
        final_total = subtotal - discount_amount + tax

        # AI Rule 2: Item Suggestions
        suggestion = ""
        if item in self.products:
            suggestion = f"You bought {item}. You might also like {self.products[item]['suggestion']}!"

        # 4. Receipt Generation
        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        receipt = f"{'='*50}\n"
        receipt += f"{'SMART CAFE / GROCERY RECEIPT':^50}\n"
        receipt += f"{'='*50}\n"
        receipt += f"Date: {date_time}\n"
        receipt += f"Customer Name: {name}\n"
        receipt += f"Contact      : {contact}\n"
        receipt += f"{'-'*50}\n"
        receipt += f"Item             Price     Qty    Total\n"
        receipt += f"{item[:15]:<16} ${price:<8.2f} {quantity:<6} ${subtotal:<.2f}\n"
        receipt += f"{'-'*50}\n"
        receipt += f"Subtotal     : ${subtotal:.2f}\n"
        
        if discount_amount > 0:
            receipt += f"Discount     : -${discount_amount:.2f} ({discount_reason})\n"
        else:
            receipt += f"Discount     : $0.00\n"
            
        receipt += f"Tax (5%)     : ${tax:.2f}\n"
        receipt += f"{'-'*50}\n"
        receipt += f"Final Total  : ${final_total:.2f}\n"
        receipt += f"{'='*50}\n"
        
        if suggestion:
            receipt += f"AI Suggestion: {suggestion}\n"
            receipt += f"{'='*50}\n"
            
        receipt += f"{'Thank You for your purchase!':^50}\n"

        # Update Text Widget
        self.receipt_text.delete(1.0, tk.END)
        self.receipt_text.insert(tk.END, receipt)

    def clear_fields(self):
        self.name_entry.delete(0, tk.END)
        self.contact_entry.delete(0, tk.END)
        self.item_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)
        self.receipt_text.delete(1.0, tk.END)

    def exit_app(self):
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.root.destroy()

class RestaurantBillingSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Restaurant Billing System")
        self.root.geometry("600x700")
        
        self.menu_items = {
            "Biryani": {"price": 250, "suggestion": "Raita"},
            "Butter Chicken": {"price": 320, "suggestion": "Naan"},
            "Paneer Tikka": {"price": 280, "suggestion": "Mint Chutney"},
            "Naan": {"price": 50, "suggestion": "Butter Chicken"},
            "Raita": {"price": 80, "suggestion": "Biryani"},
            "Mango Lassi": {"price": 100, "suggestion": "Dessert"},
            "Gulab Jamun": {"price": 120, "suggestion": "Ice Cream"},
            "Ice Cream": {"price": 150, "suggestion": "Mango Lassi"}
        }

        self.create_widgets()

    def create_widgets(self):
        # Title
        title_label = tk.Label(self.root, text="Smart Restaurant Billing System", font=("Arial", 18, "bold"), pady=10)
        title_label.pack()

        # Input Frame
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=10)

        # Labels & Entries
        tk.Label(input_frame, text="Customer Name:", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.name_entry = tk.Entry(input_frame, font=("Arial", 12))
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(input_frame, text="Table Number:", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.table_entry = tk.Entry(input_frame, font=("Arial", 12))
        self.table_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(input_frame, text="Dish Name:", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.item_entry = tk.Entry(input_frame, font=("Arial", 12))
        self.item_entry.grid(row=2, column=1, padx=10, pady=5)
        tk.Label(input_frame, text="(e.g., Biryani, Butter Chicken, Naan)", font=("Arial", 9)).grid(row=3, column=1, sticky="w")

        tk.Label(input_frame, text="Dish Price:", font=("Arial", 12)).grid(row=4, column=0, padx=10, pady=5, sticky="e")
        self.price_entry = tk.Entry(input_frame, font=("Arial", 12))
        self.price_entry.grid(row=4, column=1, padx=10, pady=5)

        tk.Label(input_frame, text="Quantity:", font=("Arial", 12)).grid(row=5, column=0, padx=10, pady=5, sticky="e")
        self.quantity_entry = tk.Entry(input_frame, font=("Arial", 12))
        self.quantity_entry.grid(row=5, column=1, padx=10, pady=5)

        # Buttons Frame
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Generate Bill", font=("Arial", 12, "bold"), bg="blue", fg="white", command=self.generate_receipt).grid(row=0, column=0, padx=10)
        tk.Button(button_frame, text="Clear", font=("Arial", 12, "bold"), bg="orange", fg="white", command=self.clear_fields).grid(row=0, column=1, padx=10)
        tk.Button(button_frame, text="Exit", font=("Arial", 12, "bold"), bg="red", fg="white", command=self.exit_app).grid(row=0, column=2, padx=10)

        # Output Frame
        output_frame = tk.Frame(self.root)
        output_frame.pack(pady=10)
        
        self.receipt_text = tk.Text(output_frame, width=60, height=15, font=("Courier", 10))
        self.receipt_text.pack()

    def generate_receipt(self):
        # 1. Fetch user inputs
        name = self.name_entry.get().strip()
        table = self.table_entry.get().strip()
        item = self.item_entry.get().strip().title()
        price_str = self.price_entry.get().strip()
        quantity_str = self.quantity_entry.get().strip()

        # 2. Input Validation
        if not name or not table or not item or not price_str or not quantity_str:
            messagebox.showerror("Validation Error", "All fields are required!")
            return

        if not table.isdigit():
            messagebox.showerror("Validation Error", "Table number must contain only digits!")
            return

        try:
            price = float(price_str)
            quantity = int(quantity_str)
        except ValueError:
            messagebox.showerror("Validation Error", "Price must be a number and Quantity must be an integer!")
            return

        if price <= 0 or quantity <= 0:
            messagebox.showerror("Validation Error", "Price and Quantity must be greater than zero!")
            return

        # 3. AI-Based Decision Rules & Billing Logic
        subtotal = price * quantity
        discount_percent = 0
        discount_reason = ""

        # AI Rule 1: Auto-apply discount based on rules
        if quantity >= 4:
            discount_percent = 15
            discount_reason = "15% Group Discount (>= 4 items)"
        elif subtotal >= 1500:
            discount_percent = 10
            discount_reason = "10% High Value Discount (>= ₹1500)"
        elif subtotal >= 800:
            discount_percent = 5
            discount_reason = "5% Standard Discount (>= ₹800)"

        discount_amount = (subtotal * discount_percent) / 100
        tax = (subtotal - discount_amount) * 0.18  # 18% GST
        service_charge = (subtotal - discount_amount) * 0.05  # 5% Service Charge
        final_total = subtotal - discount_amount + tax + service_charge

        # AI Rule 2: Item Suggestions
        suggestion = ""
        if item in self.menu_items:
            suggestion = f"Great choice! With {item}, try {self.menu_items[item]['suggestion']}!"

        # 4. Receipt Generation
        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        receipt = f"{'='*50}\n"
        receipt += f"{'SMART RESTAURANT BILL':^50}\n"
        receipt += f"{'='*50}\n"
        receipt += f"Date: {date_time}\n"
        receipt += f"Customer : {name}\n"
        receipt += f"Table No : {table}\n"
        receipt += f"{'-'*50}\n"
        receipt += f"Item             Price     Qty    Total\n"
        receipt += f"{item[:15]:<16} ₹{price:<8.2f} {quantity:<6} ₹{subtotal:<.2f}\n"
        receipt += f"{'-'*50}\n"
        receipt += f"Subtotal     : ₹{subtotal:.2f}\n"
        
        if discount_amount > 0:
            receipt += f"Discount     : -₹{discount_amount:.2f} ({discount_reason})\n"
        else:
            receipt += f"Discount     : ₹0.00\n"
            
        receipt += f"GST (18%)    : ₹{tax:.2f}\n"
        receipt += f"Service Chg  : ₹{service_charge:.2f}\n"
        receipt += f"{'-'*50}\n"
        receipt += f"Final Total  : ₹{final_total:.2f}\n"
        receipt += f"{'='*50}\n"
        
        if suggestion:
            receipt += f"Suggestion: {suggestion}\n"
            receipt += f"{'='*50}\n"
            
        receipt += f"{'Thank You! Please visit again!':^50}\n"

        # Update Text Widget
        self.receipt_text.delete(1.0, tk.END)
        self.receipt_text.insert(tk.END, receipt)

    def clear_fields(self):
        self.name_entry.delete(0, tk.END)
        self.table_entry.delete(0, tk.END)
        self.item_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)
        self.receipt_text.delete(1.0, tk.END)

    def exit_app(self):
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.root.destroy()


def show_system_selection():
    """Display a menu to choose between billing systems"""
    selection_root = tk.Tk()
    selection_root.title("Choose Billing System")
    selection_root.geometry("400x200")
    
    tk.Label(selection_root, text="Select a Billing System", font=("Arial", 16, "bold"), pady=20).pack()
    
    def open_cafe():
        selection_root.destroy()
        root = tk.Tk()
        app = SmartBillingSystem(root)
        root.mainloop()
    
    def open_restaurant():
        selection_root.destroy()
        root = tk.Tk()
        app = RestaurantBillingSystem(root)
        root.mainloop()
    
    tk.Button(selection_root, text="Cafe / Grocery Billing", font=("Arial", 12, "bold"), 
              bg="#4CAF50", fg="white", width=25, command=open_cafe, pady=10).pack(pady=10)
    
    tk.Button(selection_root, text="Restaurant Billing", font=("Arial", 12, "bold"), 
              bg="#2196F3", fg="white", width=25, command=open_restaurant, pady=10).pack(pady=10)
    
    selection_root.mainloop()


if __name__ == "__main__":
    show_system_selection()
