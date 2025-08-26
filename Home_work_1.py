import json
import os


# Класс для работы с контактами
class PhoneBook:
    def __init__(self, filename='contacts.json'):
        self.filename = filename
        self.contacts = []
        self.changes_unsaved = False
        self.load()

    def load(self):
        """Загрузить контакты из файла"""
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as f:
                self.contacts = json.load(f)
        self.changes_unsaved = False

    def save(self):
        """Сохранить контакты в файл"""
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.contacts, f, ensure_ascii=False, indent=2)
        self.changes_unsaved = False

    def show_all(self):
        """Показать все контакты"""
        print("\n--- Все контакты ---")
        for contact in self.contacts:
            print(f"ID: {contact['id']}")
            print(f"Имя: {contact['name']}")
            print(f"Телефон: {contact['phone']}")
            print(f"Комментарий: {contact['comment']}\n")

    def create_contact(self):
        """Создать новый контакт"""
        print("\n--- Создание контакта ---")
        contact = {
            'id': self._get_next_id(),
            'name': self._input_field("Имя"),
            'phone': self._input_phone(),
            'comment': self._input_field("Комментарий")
        }
        self.contacts.append(contact)
        self.changes_unsaved = True
        print("Контакт успешно создан!")

    def find_contact(self):
        """Поиск контакта"""
        print("\n--- Поиск контакта ---")
        search_term = input("Введите поисковый запрос: ").lower()
        results = []
        for contact in self.contacts:
            if (search_term in contact['name'].lower() or
                    search_term in contact['phone'] or
                    search_term in contact['comment'].lower()):
                results.append(contact)

        if results:
            print("\n--- Результаты поиска ---")
            for contact in results:
                print(f"ID: {contact['id']}, Имя: {contact['name']}, Телефон: {contact['phone']}")
        else:
            print("Контакты не найдены")

    def edit_contact(self):
        """Редактировать контакт"""
        contact = self._find_by_id()
        if contact:
            print("\n--- Редактирование контакта ---")
            contact['name'] = self._input_field("Имя", contact['name'])
            contact['phone'] = self._input_phone(contact['phone'])
            contact['comment'] = self._input_field("Комментарий", contact['comment'])
            self.changes_unsaved = True
            print("Контакт обновлен!")

    def delete_contact(self):
        """Удалить контакт"""
        contact = self._find_by_id()
        if contact:
            self.contacts.remove(contact)
            self.changes_unsaved = True
            print("Контакт удален!")

    def _get_next_id(self):
        """Получить следующий ID"""
        if self.contacts:
            return max(c['id'] for c in self.contacts) + 1
        return 1

    def _find_by_id(self):
        """Найти контакт по ID"""
        try:
            contact_id = int(input("Введите ID контакта: "))
            for contact in self.contacts:
                if contact['id'] == contact_id:
                    return contact
            print("Контакт с таким ID не найден")
        except ValueError:
            print("Некорректный ID")
        return None

    def _input_field(self, field_name, default=""):
        """Ввод поля с валидацией"""
        while True:
            value = input(f"{field_name}{f' ({default})' if default else ''}: ").strip()
            if value:
                return value
            if default:
                return default
            print("Поле не может быть пустым!")

    def _input_phone(self, default=""):
        """Ввод телефона с валидацией"""
        while True:
            phone = self._input_field("Телефон", default)
            if phone.isdigit():
                return phone
            print("Телефон должен содержать только цифры!")


# Основное меню
def main():
    phone_book = PhoneBook()

    while True:
        print("\n--- Телефонный справочник ---")
        print("1. Открыть файл")
        print("2. Сохранить файл")
        print("3. Показать все контакты")
        print("4. Создать контакт")
        print("5. Найти контакт")
        print("6. Изменить контакт")
        print("7. Удалить контакт")
        print("8. Выход")

        choice = input("Выберите действие: ")

        if choice == '1':
            phone_book.load()
        elif choice == '2':
            phone_book.save()
        elif choice == '3':
            phone_book.show_all()
        elif choice == '4':
            phone_book.create_contact()
        elif choice == '5':
            phone_book.find_contact()
        elif choice == '6':
            phone_book.edit_contact()
        elif choice == '7':
            phone_book.delete_contact()
        elif choice == '8':
            if phone_book.changes_unsaved:
                save = input("Есть несохраненные изменения. Сохранить? (y/n): ").lower()
                if save == 'y':
                    phone_book.save()
            break
        else:
            print("Некорректный ввод")


if __name__ == "__main__":
    main()