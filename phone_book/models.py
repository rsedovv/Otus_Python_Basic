import json
import os
from .exceptions import ValidationError, FileOperationError, ContactNotFoundError


class Contact:
    def __init__(self, id, name, phone, comment):
        self.id = id
        self.name = self._validate_name(name)
        self.phone = self._validate_phone(phone)
        self.comment = comment

    @staticmethod
    def _validate_name(name):
        if not isinstance(name, str) or not name.strip():
            raise ValidationError("Имя контакта не может быть пустым")
        return name.strip()

    @staticmethod
    def _validate_phone(phone):
        if not isinstance(phone, str):
            raise ValidationError("Номер телефона должен быть строкой")

        phone = phone.strip()
        if not phone:
            raise ValidationError("Номер телефона не может быть пустым")

        cleaned_phone = ''.join(c for c in phone if c.isdigit())
        if not cleaned_phone:
            raise ValidationError("Номер телефона должен содержать только цифры")

        return cleaned_phone

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'comment': self.comment
        }


class FileHandler:
    def __init__(self, filename):
        self.filename = filename

    def load_contacts(self):
        if not os.path.exists(self.filename):
            return []

        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            raise FileOperationError(f"Ошибка загрузки файла: {e}")

    def save_contacts(self, contacts):
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump([contact.to_dict() for contact in contacts], f,
                          ensure_ascii=False, indent=2)
        except IOError as e:
            raise FileOperationError(f"Ошибка сохранения файла: {e}")


class PhoneBook:
    def __init__(self, file_handler):
        self.file_handler = file_handler
        self.contacts = []
        self.changes_unsaved = False

    def load(self):
        self.contacts = [Contact(**item) for item in self.file_handler.load_contacts()]
        self.changes_unsaved = False

    def save(self):
        self.file_handler.save_contacts(self.contacts)
        self.changes_unsaved = False

    def add_contact(self, contact):
        self.contacts.append(contact)
        self.changes_unsaved = True

    def find_by_id(self, contact_id):
        for contact in self.contacts:
            if contact.id == contact_id:
                return contact
        raise ContactNotFoundError(f"Контакт с ID {contact_id} не найден")

    def search_contacts(self, search_term):
        search_term = search_term.lower()
        results = []
        for contact in self.contacts:
            if (search_term in contact.name.lower() or
                    search_term in contact.phone or
                    (contact.comment and search_term in contact.comment.lower())):
                results.append(contact)
        return results

    def delete_contact(self, contact_id):
        contact = self.find_by_id(contact_id)
        self.contacts.remove(contact)
        self.changes_unsaved = True

    def get_next_id(self):
        return max(contact.id for contact in self.contacts) + 1 if self.contacts else 1