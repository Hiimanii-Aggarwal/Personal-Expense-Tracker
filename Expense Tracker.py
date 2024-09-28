import json
import matplotlib.pyplot as plt
from collections import defaultdict
import tkinter as tk
from tkinter import messagebox, simpledialog

class ExpenseTracker:
    def __init__(self):
        self.expenses = []  # List to store expenses
        self.categories = defaultdict(list)  # Dictionary for categorization

    def add_expense(self, amount, category, date):
        expense = {"amount": amount, "category": category, "date": date}
        self.expenses.append(expense)
        self.categories[category].append(expense)
        messagebox.showinfo("Success", f"Added expense: {expense['category']} - ${expense['amount']:.2f}")

    def view_expenses(self):
        if not self.expenses:
            messagebox.showinfo("All Expenses", "No expenses recorded.")
            return
        expenses_str = "\n".join([f"{exp['date']}: {exp['category']} - ${exp['amount']:.2f}" for exp in self.expenses])
        messagebox.showinfo("All Expenses", expenses_str)

    def total_expenses(self):
        total = sum(exp['amount'] for exp in self.expenses)
        messagebox.showinfo("Total Expenses", f"Total Expenses: ${total:.2f}")

    def visualize_expenses(self):
        if not self.expenses:
            messagebox.showinfo("Visualization", "No expenses to visualize.")
            return

        categories = self.categories.keys()
        amounts = [sum(exp['amount'] for exp in self.categories[cat]) for cat in categories]

        plt.bar(categories, amounts, color='lightcoral')
        plt.xlabel('Categories')
        plt.ylabel('Amount Spent')
        plt.title('Expense Breakdown by Category')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def save_to_file(self):
        with open('expenses.json', 'w') as f:
            json.dump(self.expenses, f)
        messagebox.showinfo("Save", "Expenses saved to expenses.json")

class GUI:
    def __init__(self, root):
        self.root = root
        self.tracker = ExpenseTracker()
        self.root.title("Expense Tracker")
        self.root.geometry("400x400")  # Set window size
        self.root.configure(bg="#ffffff")  # Bright white background

        # Title Label
        title_label = tk.Label(root, text="Expense Tracker", font=("Arial", 24), bg="#ffffff", fg="#333333")
        title_label.pack(pady=20)

        # Buttons
        btn_style = {
            "font": ("Arial", 14),
            "bg": "#007BFF",  # Bright blue color
            "fg": "white",
            "activebackground": "#0056b3",  # Darker blue on click
            "height": 2,
            "width": 20
        }

        tk.Button(root, text="Add Expense", command=self.add_expense, **btn_style).pack(pady=10)
        tk.Button(root, text="View Expenses", command=self.tracker.view_expenses, **btn_style).pack(pady=10)
        tk.Button(root, text="Total Expenses", command=self.tracker.total_expenses, **btn_style).pack(pady=10)
        tk.Button(root, text="Visualize Expenses", command=self.tracker.visualize_expenses, **btn_style).pack(pady=10)
        tk.Button(root, text="Save Expenses", command=self.tracker.save_to_file, **btn_style).pack(pady=10)
        tk.Button(root, text="Exit", command=self.root.quit, **btn_style).pack(pady=10)

    def add_expense(self):
        categories = ["Food", "Transport", "Utilities", "Entertainment", "Health", "Groceries", "Education", "Others"]
        
        # Create a dropdown for category selection
        category = simpledialog.askstring("Select Category", 
            "Choose a category:\n" + "\n".join(categories) + "\n(Type the category or select 'Others' for custom)")
        
        if category not in categories and category != "Others":
            messagebox.showwarning("Invalid Category", "Please select a valid category or type 'Others' for a custom category.")
            return
        
        if category == "Others":
            category = simpledialog.askstring("Custom Category", "Please enter your custom category:")

        amount = simpledialog.askfloat("Input", "Enter the amount:")
        date = simpledialog.askstring("Input", "Enter the date (YYYY-MM-DD):")

        if amount is not None and category and date:
            self.tracker.add_expense(amount, category, date)
        else:
            messagebox.showwarning("Input Error", "Please enter valid data.")

if __name__ == "__main__":
    root = tk.Tk()
    gui = GUI(root)
    root.mainloop()
