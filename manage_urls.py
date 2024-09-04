import json


class ManagerURL:

    def __init__(self, ):
        self.file_path = 'urls.json'

    def add_url_to_json(self, name, url):
        file_path = self.file_path

        try:
            # Завантажуємо існуючі дані з JSON файлу
            with open(file_path, "r", encoding='utf-8') as json_file:
                data = json.load(json_file)
        except FileNotFoundError:
            # Якщо файл не існує, створюємо порожній словник
            data = {}

        # Перевіряємо, чи є дублікат URL
        if url in data.values():
            return (False, f"URL '{url}' вже існує в файлі під іншим ім'ям.")

        # Додаємо новий URL
        data[name] = url

        # Записуємо оновлені дані назад у файл
        with open(file_path, "w") as json_file:
            json.dump(data, json_file, indent=4)

        return (True, f"URL '{url}' додано під ім'ям '{name}'.")

    def get_list_url(self) -> list:
        file_path = self.file_path

        try:
            # Завантажуємо існуючі дані з JSON файлу
            with open(file_path, "r", encoding='utf-8') as json_file:
                data = json.load(json_file)
        except FileNotFoundError:
            # Якщо файл не існує, повертаємо порожній список
            print(f"Файл '{file_path}' не знайдено.")
            return []

        # Повертаємо список URL-адрес
        return list(data.values())

    def get_district_name(self) -> str:
        file_path = self.file_path

        try:
            # Завантажуємо існуючі дані з JSON файлу
            with open(file_path, "r", encoding='utf-8') as json_file:
                data = json.load(json_file)
        except FileNotFoundError:
            # Якщо файл не існує, повертаємо порожній рядок
            print(f"Файл '{file_path}' не знайдено.")
            return ""

        # Повертаємо рядок з назвами URL-адрес, розділеними комами
        return ", ".join(data.keys())

