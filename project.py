import sqlite3
from bs4 import BeautifulSoup
import requests


class DatabaseHandler:
    def __init__(self,name="web_search.db"):
        self.connection = sqlite3.connect(name)
        self.create_table()

    def create_table(self):
        sites = """
        CREATE TABLE IF NOT EXISTS websites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT UNIQUE
        )
        """
        self.connection.execute(sites)
        self.connection.commit()

    def add_website(self, url):
        self.connection.execute("INSERT INTO websites (url) VALUES (?)", (url,))
        self.connection.commit()

    def get_websites(self):
        return [row[0] for row in self.connection.execute("SELECT url FROM websites")]

    def clear_websites(self):
        self.connection.execute("DELETE FROM websites")
        self.connection.commit()


class WebParser:
    def parse_website(self, url, keyword):
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            content = soup.get_text().lower()
            return content.count(keyword.lower())
        except Exception as e:
            print(f"Не удалось обработать сайт {url}: {e}")
            return 0


class UserInterface:
    def __init__(self, db_handler, web_parser):
        self.db_handler = db_handler
        self.web_parser = web_parser

    def display_menu(self):
        print("\n--- Меню ---")
        print("1. Добавить сайт")
        print("2. Очистить базу данных")
        print("3. Выполнить поиск")
        print("4. Выйти")

    def add_website(self):
        url = input("Введите URL сайта: ")
        self.db_handler.add_website(url)
        print(f"Сайт '{url}' добавлен в базу данных.")

    def clear_database(self):
        self.db_handler.clear_websites()
        print("База данных очищена.")

    def perform_search(self):
        keyword = input("Введите ключевое слово для поиска: ")
        websites = self.db_handler.get_websites()
        if not websites:
            print("База данных пуста. Добавьте сайты для поиска.")
            return

        results = {}
        for url in websites:
            print(f"Обработка сайта: {url}...")
            count = self.web_parser.parse_website(url, keyword)
            results[url] = count

        sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)
        print("\nРезультаты поиска:")
        for url, count in sorted_results:
            print(f"{url}: {count} совпадений")


def run():
    db_handler = DatabaseHandler()
    web_parser = WebParser()
    ui = UserInterface(db_handler, web_parser)

    while True:
        ui.display_menu()
        choice = input("Выберите действие: ")
        if choice == "1":
            ui.add_website()
        elif choice == "2":
            ui.clear_database()
        elif choice == "3":
            ui.perform_search()
        elif choice == "4":
            print("Выход из программы.")
            break
        else:
            print("Неверный ввод. Попробуйте снова.")


if __name__ == "__main__":
    run()

#некоторую часть кода я искал из интернета