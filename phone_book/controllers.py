from .exceptions import ContactNotFoundError, ValidationError, FileOperationError
from .models import PhoneBook, Contact, FileHandler
from .views import ContactView


class PhoneBookController:
    def __init__(self, filename='contacts.json'):
        self.file_handler = FileHandler(filename)
        self.phone_book = PhoneBook(self.file_handler)
        self.view = ContactView()

    def run(self):
        while True:
            self.show_menu()
            choice = input("Выберите действие: ")
            try:
                if choice == '1':
                    self.load_file()
                elif choice == '2':
                    self.save_file()
                elif choice == '3':
                    self.show_all_contacts()
                elif choice == '4':
                    self.create_contact()
                elif choice == '5':
                    self.find_contacts()
                elif choice == '6':
                    self.edit_contact()
                elif choice == '7':
                    self.delete_contact()
                elif choice == '8':
                    self.exit()
                    break
                else:
                    print("Некорректный ввод")
            except (ContactNotFoundError, ValidationError, FileOperationError) as e:
                print(f"Ошибка: {e}")

    def show_menu(self):
        print("\n--- Телефонный справочник ---")
        print("1. Открыть файл")
        print("2. Сохранить файл")
        print("3. Показать все контакты")
        print("4. Создать контакт")
        print("5. Найти контакт")
        print("6. Изменить контакт")
        print("7. Удалить контакт")
        print("8. Выход")

    def load_file(self):
        self.phone_book.load()
        print("Файл успешно загружен")

    def save_file(self):
        self.phone_book.save()
        print("Файл успешно сохранен")

    def show_all_contacts(self):
        self.view.show_contacts(self.phone_book.contacts)

    def create_contact(self):
        contact_data = self.view.get_contact_data()
        contact = Contact(
            id=self.phone_book.get_next_id(),
            **contact_data
        )
        self.phone_book.add_contact(contact)
        print("Контакт успешно создан!")

    def find_contacts(self):
        search_term = self.view.input_search_term()
        results = self.phone_book.search_contacts(search_term)
        self.view.show_search_results(results)

    def edit_contact(self):
        contact_id = self.view.input_contact_id()
        contact = self.phone_book.find_by_id(contact_id)

        print("\n--- Редактирование контакта ---")
        updated_data = {
            'name': self.view.input_field("Имя", contact.name),
            'phone': self.view.input_phone(contact.phone),
            'comment': self.view.input_field("Комментарий", contact.comment)
        }

        contact.name = updated_data['name']
        contact.phone = updated_data['phone']
        contact.comment = updated_data['comment']

        self.phone_book.changes_unsaved = True
        print("Контакт обновлен!")

    def delete_contact(self):
        contact_id = self.view.input_contact_id()
        self.phone_book.delete_contact(contact_id)
        print("Контакт удален!")

    def exit(self):
        if self.phone_book.changes_unsaved:
            save = input("Есть несохраненные изменения. Сохранить? (y/n): ").lower()
            if save == 'y':
                self.phone_book.save()