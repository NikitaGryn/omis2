class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.transactions = []
        self.budget_goals = {}
        self.limits = {}

        self.categories = {
            "Еда": "Расход",
            "Топливо": "Расход",
            "Пассивный доход": "Доход",
            "Развлечения": "Расход",
            "Зарплата": "Доход",
            "Инвестиции": "Доход",
            "Одежда": "Расход",
            "Образование": "Расход",
            "Медицина": "Расход",
            "Подарки": "Расход"
        }