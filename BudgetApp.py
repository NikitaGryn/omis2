import tkinter as tk
from tkinter import messagebox
import pickle
from User import User
from BudgetGoals import BudgetGoals
from BudgetGoals import Transactions
from Categories import Categories


class BudgetApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Управление личным бюджетом")
        self.user = None

        self.start_screen()

    def start_screen(self):
        self.clear_frame()
        tk.Label(self.root, text="Добро пожаловать!", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.root, text="Имя пользователя:").pack()
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack(pady=5)

        tk.Label(self.root, text="Пароль:").pack()
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack(pady=5)

        tk.Button(self.root, text="Войти", command=self.login).pack(pady=5)
        tk.Button(self.root, text="Регистрация", command=self.register).pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        users = self.load_users()

        if username in users and users[username].password == password:
            self.user = users[username]
            self.main_menu()
        else:
            messagebox.showerror("Ошибка", "Неверное имя пользователя или пароль")

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        users = self.load_users()

        if username in users:
            messagebox.showerror("Ошибка", "Пользователь уже существует")
        else:
            new_user = User(username, password)
            users[username] = new_user
            self.user = new_user
            self.save_users(users)
            messagebox.showinfo("Успех", "Регистрация успешна")
            self.main_menu()

    def main_menu(self):
        self.clear_frame()
        tk.Label(self.root, text=f"Добро пожаловать, {self.user.username}!", font=("Arial", 16)).pack(pady=10)

        tk.Button(self.root, text="Цели и лимиты", command=self.budget_goals_screen).pack(pady=5)
        tk.Button(self.root, text="Транзакции", command=self.transactions_screen).pack(pady=5)
        tk.Button(self.root, text="Категории", command=self.categories_screen).pack(pady=5)
        tk.Button(self.root, text="Выход", command=self.start_screen).pack(pady=5)

    def budget_goals_screen(self):
        BudgetGoals(self.root, self.user, self.main_menu, self)

    def transactions_screen(self):
        Transactions(self.root, self.user, self.main_menu, self)

    def categories_screen(self):
        Categories(self.root, self.user, self.main_menu, self)


    def load_users(self):
        try:
            with open("users.pkl", "rb") as f:
                return pickle.load(f)
        except FileNotFoundError:
            return {}

    def save_users(self, users=None):
        if users is None:
            users = self.load_users()
        users[self.user.username] = self.user

        with open("users.pkl", "wb") as f:
            pickle.dump(users, f)

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()