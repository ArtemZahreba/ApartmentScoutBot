import sqlite3
from datetime import datetime, timedelta


class ManagerDB:

    def __init__(self, ):
        self.file_path = 'data.db'

    def add_apartment_to_db(self, olx_id, url, price, parsing_date=None):
        db_path = self.file_path

        # Встановлюємо з'єднання з базою даних
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Якщо дата парсингу не вказана, використовуємо поточну дату
        if parsing_date is None:
            parsing_date = datetime.now().date().strftime("%Y-%m-%d %H:00")

        # Перевірка на наявність дубліката
        cursor.execute('''
        SELECT 1 FROM Apartments WHERE olx_id = ?
        ''', (olx_id,))

        if cursor.fetchone() is not None:
            # Запис з таким olx_id вже існує
            conn.close()
            return (False, "Запис з таким OLX ID вже існує.")

        # Виконання SQL-запиту для додавання нового запису
        cursor.execute('''
        INSERT INTO Apartments (olx_id, url, price, parsing_date)
        VALUES (?, ?, ?, ?)
        ''', (olx_id, url, price, parsing_date))

        # Збереження змін
        conn.commit()

        # Закриття з'єднання
        conn.close()

        return (True, (olx_id, url, price, parsing_date))

    def get_recent_apartments(self, days=7):
        db_path = self.file_path

        # Встановлюємо з'єднання з базою даних
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Обчислюємо дату 7 днів тому
        seven_days_ago = datetime.now() - timedelta(days=days)
        seven_days_ago_date = seven_days_ago.date().strftime("%Y-%m-%d %H:00")

        # Виконання SQL-запиту для вибірки записів за останні 7 днів
        cursor.execute('''
        SELECT * FROM Apartments
        WHERE parsing_date >= ?
        ''', (seven_days_ago_date,))

        # Отримання всіх результатів
        recent_apartments = cursor.fetchall()

        # Закриття з'єднання
        conn.close()

        return recent_apartments

    def check_olx_id_exists(self, olx_id) -> bool:
        db_path = self.file_path

        # Встановлюємо з'єднання з базою даних
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Виконання SQL-запиту для перевірки наявності olx_id
        cursor.execute('''
        SELECT 1 FROM Apartments WHERE olx_id = ?
        ''', (olx_id,))

        # Отримання результату
        exists = cursor.fetchone() is not None

        # Закриття з'єднання
        conn.close()

        return exists


