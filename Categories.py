import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar
from tkinter import ttk
import datetime


class Categories:
    def __init__(self, root, user, back_callback, app):
        self.root = root
        self.user = user
        self.back_callback = back_callback
        self.app = app
        self.show_screen()

    def show_screen(self):
        self.clear_frame()

        tk.Label(self.root, text="Категории", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.root, text="Выберите категорию:").pack()
        self.category_combo = ttk.Combobox(self.root, values=list(self.user.categories.keys()))
        self.category_combo.pack(pady=5)

        tk.Label(self.root, text="Добавить новую категорию:").pack()
        self.new_category_entry = tk.Entry(self.root)
        self.new_category_entry.pack(pady=5)

        tk.Button(self.root, text="Добавить категорию", command=self.add_new_category).pack(pady=5)

        tk.Label(self.root, text="Выберите дату от:").pack()
        self.start_date_calendar = Calendar(self.root, date_pattern="yyyy-mm-dd")
        self.start_date_calendar.pack(pady=5)

        tk.Label(self.root, text="Выберите дату до:").pack()
        self.end_date_calendar = Calendar(self.root, date_pattern="yyyy-mm-dd")
        self.end_date_calendar.pack(pady=5)

        tk.Button(self.root, text="Применить фильтр", command=self.filter_transactions).pack(pady=10)

        tk.Button(self.root, text="Назад", command=self.back_callback).pack(pady=5)

    def add_new_category(self):
        new_category = self.new_category_entry.get()

        if not new_category:
            messagebox.showerror("Ошибка", "Введите название новой категории!")
            return

        if new_category in self.user.categories:
            messagebox.showerror("Ошибка", "Категория уже существует!")
            return

        self.user.categories[new_category] = "Расход"

        self.new_category_entry.delete(0, tk.END)

        self.app.save_users()

        self.category_combo["values"] = list(self.user.categories.keys())

        messagebox.showinfo("Успех", f"Категория '{new_category}' добавлена!")

    def filter_transactions(self):
        selected_category = self.category_combo.get()
        start_date = self.start_date_calendar.get_date()
        end_date = self.end_date_calendar.get_date()

        try:
            start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
            end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректные даты!")
            return

        filtered_transactions = []
        for transaction in self.user.transactions:
            transaction_date = datetime.datetime.strptime(transaction["date"], "%Y-%m-%d")
            if (transaction["category"] == selected_category and
                start_date <= transaction_date <= end_date):
                filtered_transactions.append(transaction)

        self.show_filtered_transactions(filtered_transactions)

    def show_filtered_transactions(self, transactions):
        if hasattr(self, 'transactions_table'):
            self.transactions_table.destroy()

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

        for transaction in transactions:
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