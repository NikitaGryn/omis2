import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar
from tkinter import ttk


class BudgetGoals:
    def __init__(self, root, user, back_callback, app):
        self.root = root
        self.user = user
        self.back_callback = back_callback
        self.app = app
        self.show_screen()

    def show_screen(self):
        self.clear_frame()
        tk.Label(self.root, text="Цели и лимиты", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.root, text="Выберите категорию:").pack()
        self.category_combo = ttk.Combobox(self.root, values=list(self.user.categories.keys()))
        self.category_combo.pack(pady=5)

        tk.Label(self.root, text="Введите сумму (цель или лимит):").pack()
        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.pack(pady=5)

        tk.Button(self.root, text="Добавить цель или лимит", command=self.add_goal_or_limit).pack(pady=5)

        self.goals_table = ttk.Treeview(self.root, columns=("Категория", "Сумма", "Статус"), show="headings")
        self.goals_table.heading("Категория", text="Категория")
        self.goals_table.heading("Сумма", text="Сумма")
        self.goals_table.heading("Статус", text="Статус")

        self.goals_table.column("Категория", width=150)
        self.goals_table.column("Сумма", width=100)
        self.goals_table.column("Статус", width=150)

        self.goals_table.pack(pady=10)
        self.update_goals_table()

        tk.Button(self.root, text="Назад", command=self.back_callback).pack(pady=5)

    def add_goal_or_limit(self):
        category = self.category_combo.get()
        amount = self.amount_entry.get()

        if not category or not amount:
            messagebox.showerror("Ошибка", "Заполните все поля!")
            return

        try:
            amount = float(amount)
            if amount <= 0:
                messagebox.showerror("Ошибка", "Сумма должна быть больше нуля!")
                return
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректную сумму!")
            return

        if category not in self.user.budget_goals:
            self.user.budget_goals[category] = {"amount": amount, "spent": 0}

        self.app.save_users()
        self.update_goals_table()

    def update_goals_table(self):
        # Очищаем таблицу
        for row in self.goals_table.get_children():
            self.goals_table.delete(row)

        for category, goal in self.user.budget_goals.items():
            spent = goal["spent"]
            remaining = goal["amount"] - spent
            status = "Выполнено" if remaining <= 0 else f"Осталось {remaining}"

            color = "green" if remaining <= 0 else "red"
            self.goals_table.insert(
                "",
                "end",
                values=(category, goal["amount"], status),
                tags=(color,)
            )

        self.goals_table.tag_configure("green", background="lightgreen")
        self.goals_table.tag_configure("red", background="lightcoral")

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()



class Transactions(BudgetGoals):
    def __init__(self, root, user, back_callback, app):
        self.root = root
        self.user = user
        self.back_callback = back_callback
        self.app = app
        self.categories = user.categories
        self.show_screen()

    def show_screen(self):
        self.clear_frame()

        tk.Label(self.root, text="Транзакции", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.root, text="Введите сумму:").pack()
        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.pack(pady=5)

        tk.Label(self.root, text="Выберите категорию:").pack()
        self.category_combo = ttk.Combobox(self.root, values=list(self.categories.keys()))
        self.category_combo.pack(pady=5)

        tk.Label(self.root, text="Выберите дату:").pack()
        self.calendar = Calendar(self.root, date_pattern="yyyy-mm-dd")
        self.calendar.pack(pady=10)

        tk.Button(self.root, text="Добавить транзакцию", command=self.add_transaction).pack(pady=5)

        self.transactions_table = ttk.Treeview(self.root, columns=("Дата", "Категория", "Сумма", "Тип"), show="headings")
        self.transactions_table.heading("Дата", text="Дата")
        self.transactions_table.heading("Категория", text="Категория")
        self.transactions_table.heading("Сумма", text="Сумма")
        self.transactions_table.heading("Тип", text="Тип")

        self.transactions_table.column("Дата", width=100)
        self.transactions_table.column("Категория", width=150)
        self.transactions_table.column("Сумма", width=100)
        self.transactions_table.column("Тип", width=100)

        self.transactions_table.pack(pady=10)

        self.update_transactions_table()

        tk.Button(self.root, text="Назад", command=self.back_callback).pack(pady=5)

    def add_transaction(self):
        amount = self.amount_entry.get()
        category = self.category_combo.get()
        date = self.calendar.get_date()

        if not amount or not category:
            messagebox.showerror("Ошибка", "Заполните все поля!")
            return

        try:
            amount = float(amount)
            if amount <= 0:
                messagebox.showerror("Ошибка", "Сумма должна быть больше нуля!")
                return
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректную сумму!")
            return

        transaction_type = self.categories.get(category)

        transaction = {
            "amount": amount,
            "category": category,
            "type": transaction_type,
            "date": date
        }

        self.user.transactions.append(transaction)

        if transaction_type == "Расход" and category in self.user.budget_goals:
            self.user.budget_goals[category]["spent"] += amount

        if transaction_type == "Доход" and category in self.user.budget_goals:
            self.user.budget_goals[category]["spent"] -= amount

        messagebox.showinfo("Успех", "Транзакция добавлена!")

        self.app.save_users()

        self.amount_entry.delete(0, tk.END)
        self.category_combo.set("")

        self.update_transactions_table()
        self.update_goals_table()


    def update_transactions_table(self):
        for row in self.transactions_table.get_children():
            self.transactions_table.delete(row)

        for transaction in self.user.transactions:
            color = "green" if transaction["type"] == "Доход" else "red"
            self.transactions_table.insert(
                "",
                "end",
                values=(transaction["date"], transaction["category"], transaction["amount"], transaction["type"]),
                tags=(color,)
            )

        self.transactions_table.tag_configure("green", background="lightgreen")
        self.transactions_table.tag_configure("red", background="lightcoral")

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()