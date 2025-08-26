from .exceptions import ValidationError

class ContactView:
    @staticmethod
    def input_field(field_name, default=""):
        while True:
            value = input(f"{field_name}{f' ({default})' if default else ''}: ").strip()
            if value:
                return value
            if default:
                return default
            print("Поле не может быть пустым!")

    @staticmethod
    def input_phone(default=""):
        while True:
            phone = ContactView.input_field("Телефон", default)
            if phone.isdigit():
                return phone
            print("Телефон должен содержать только цифры!")

    @staticmethod
    def get_contact_data():
        print("\n--- Создание контакта ---")
        return {
            'name': ContactView.input_field("Имя"),
            'phone': ContactView.input_phone(),
            'comment': ContactView.input_field("Комментарий")
        }

    @staticmethod
    def show_contact(contact):
        print(f"ID: {contact.id}")
        print(f"Имя: {contact.name}")
        print(f"Имя: {contact.phone}")
        print(f"Комментарий: {contact.comment}\n")

    @staticmethod
    def show_contacts(contacts):
        print("\n--- Все контакты ---")
        for contact in contacts:
            ContactView.show_contact(contact)

    @staticmethod
    def show_search_results(contacts):
        if contacts:
            print("\n--- Результаты поиска ---")
            for contact in contacts:
                print(f"ID: {contact.id}, Имя: {contact.name}, Телефон: {contact.phone}")
        else:
            print("Контакты не найдены")

    @staticmethod
    def input_contact_id():
        while True:
            try:
                return int(input("Введите ID контакта: "))
            except ValueError:
                print("Некорректный ID. Попробуйте снова.")

    @staticmethod
    def input_search_term():
        return input("Введите поисковый запрос: ").lower()