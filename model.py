import sqlite3
from datetime import datetime

class DBSQL_Manager:

    def __init__(self):
        self._connection = sqlite3.connect("users.db")
        self._cursor = self._connection.cursor()

        self._initialize()

    def _initialize(self):
        self._cursor.execute("""
            CREATE TABLE IF NOT EXISTS Users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                
                login    TEXT NOT NULL,
                password   INTEGER NOT NULL
            );
        """)
        self._cursor.execute("""
            CREATE TABLE IF NOT EXISTS Expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_user INTEGER NOT NULL,
                category    TEXT NOT NULL,
                amount   INTEGER NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY (id_user) REFERENCES Users (id)
            );
        """)
        self._cursor.execute("""
            CREATE TABLE IF NOT EXISTS Income (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_user INTEGER NOT NULL,
                category    TEXT NOT NULL,
                amount   INTEGER NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY (id_user) REFERENCES Users (id)
            );
        """)
        self._cursor.execute("""
            CREATE TABLE IF NOT EXISTS Goals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_user INTEGER NOT NULL,
                description TEXT NOT NULL,
                amount INTEGER NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY (id_user) REFERENCES Users (id)
            );
        """)

    def add_user(self, user):
        id = user.id
        login = user.login
        password = user.password

        self._cursor.execute(f"""
    INSERT INTO Users(id, login, password) VALUES
        (?, ?, ?)                             
    """,
                             (id, login, password)
                             )
        self._connection.commit()

    def check_login(self, login):
        self._cursor.execute("SELECT * FROM Users WHERE login=?", (login, ))

        if self._cursor.fetchone():
            return True
        return False
    

    def check_id(self, id):
        self._cursor.execute("SELECT * FROM Users WHERE id=?", (id, ))

        if self._cursor.fetchone():
            return True
        return False
    
    def add_income(self, id_user, amount, category):
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
        self._cursor.execute('''
            INSERT INTO Income (id_user, category, amount, created_at)
            VALUES (?, ?, ?, ?)
        ''', (id_user, category, amount, created_at))
        self._connection.commit()

    def add_expense(self, id_user, amount, category):
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
        self._cursor.execute('''
            INSERT INTO Expenses (id_user, category, amount, created_at)
            VALUES (?, ?, ?, ?)
        ''', (id_user, category, amount, created_at))
        self._connection.commit()

    def set_goal(self, id_user, amount, description):
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
        self._cursor.execute('''
            INSERT INTO Goals (id_user, description, amount, created_at)
            VALUES (?, ?, ?, ?)
        ''', (id_user, description, amount, created_at))
        self._connection.commit()

    def view_incomes(self, id_user, period, category=None):
        if category is None:

            self._cursor.execute('''
                SELECT category, amount, created_at FROM Income 
                WHERE created_at >= ? AND id_user = ?
                ''', (period, id_user, ))
        else:
            self._cursor.execute('''
                SELECT category, amount, created_at FROM Income 
                WHERE created_at >= ? AND id_user = ? AND category = ?
                ''', (period, id_user, category, ))
        rows = self._cursor.fetchall()
        self._connection.commit()
        return rows
    
    def view_expenses(self, id_user, period, category=None):
        if category is None:

            self._cursor.execute('''
                SELECT category, amount, created_at FROM Expenses 
                WHERE created_at >= ? AND id_user = ?
                ''', (period, id_user, ))
        else:
            self._cursor.execute('''
                SELECT category, amount, created_at FROM Expenses 
                WHERE created_at >= ? AND id_user = ? AND category = ?
                ''', (period, id_user, category, ))
        rows = self._cursor.fetchall()
        self._connection.commit()
        return rows

    def get_sum_incomes(self, id_user):
        self._cursor.execute('''
                SELECT SUM(amount) FROM Income 
                WHERE id_user = ?
                ''', (id_user, ))
        rows = self._cursor.fetchone()
        self._connection.commit()
        return rows
    
    def get_sum_expenses(self, id_user):
        self._cursor.execute('''
                SELECT SUM(amount) FROM Expenses 
                WHERE id_user = ?
                ''', (id_user, ))
        rows = self._cursor.fetchone()
        self._connection.commit()
        return rows
    
    def get_goal(self, id_user):
        self._cursor.execute('''
                SELECT amount, description FROM Goals 
                WHERE id_user = ?
                ''', (id_user, ))
        rows = self._cursor.fetchone()
        self._connection.commit()
        return rows
    
    def delete_goal(self, id_user):
        self._cursor.execute('''
                DELETE FROM Goals 
                WHERE id_user = ?
                
                ''', (id_user, ))

        self._connection.commit()

    def get_expense_structure(self, id_user):
        self._cursor.execute('''
            SELECT category, SUM(amount) FROM Expenses
            WHERE id_user = ?
            GROUP BY category
            ORDER BY SUM(amount) DESC
        ''', (id_user, ))
        category_data = self._cursor.fetchall()
        return category_data
    
    def get_incomes_structure(self, id_user):
        self._cursor.execute('''
            SELECT category, SUM(amount) FROM Income
            WHERE id_user = ?
            GROUP BY category
            ORDER BY SUM(amount) DESC
        ''', (id_user, ))
        category_data = self._cursor.fetchall()
        return category_data

class User:

    def __init__(self, id: int, login: str, password: str):
        self.__id = id
        self.__login = login
        self.__password = password

    @property
    def login(self):
        return self.__login

    @property
    def id(self):
        return self.__id

    @property
    def password(self):
        return self.__password
