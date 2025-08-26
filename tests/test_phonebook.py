import pytest
from phone_book.models import Contact, PhoneBook, FileHandler
from phone_book.exceptions import ContactNotFoundError, FileOperationError, ValidationError


class TestAddContact:
    def test_add_valid_contact(self, test_phonebook):
        initial_count = len(test_phonebook.contacts)
        test_phonebook.add_contact(Contact(id=3, name="Новый", phone="789", comment=""))
        assert len(test_phonebook.contacts) == initial_count + 1

    @pytest.mark.parametrize("name,phone", [
        ("", "123"), ("   ", "123"), ("Вася", ""), ("Вася", "abc")
    ])
    def test_add_invalid_contact(self, name, phone):
        with pytest.raises(ValidationError):
            Contact(id=1, name=name, phone=phone, comment="")


class TestSearchContact:
    def test_search_by_name(self, test_phonebook):
        results = test_phonebook.search_contacts("Иван")
        assert len(results) == 1
        assert results[0].id == 1

    def test_search_by_phone(self, test_phonebook):
        results = test_phonebook.search_contacts("456")
        assert len(results) == 1
        assert results[0].id == 2

    def test_search_non_existing(self, test_phonebook):
        assert len(test_phonebook.search_contacts("Несуществующий")) == 0


class TestEditContact:
    def test_edit_contact(self, test_phonebook):
        contact = test_phonebook.find_by_id(1)
        contact.name = "Новое имя"
        contact.phone = "987"
        assert test_phonebook.find_by_id(1).name == "Новое имя"
        assert test_phonebook.find_by_id(1).phone == "987"

    def test_edit_non_existing(self, test_phonebook):
        with pytest.raises(ContactNotFoundError):
            test_phonebook.find_by_id(99)


class TestDeleteContact:
    def test_delete_contact(self, test_phonebook):
        initial_count = len(test_phonebook.contacts)
        test_phonebook.delete_contact(1)
        assert len(test_phonebook.contacts) == initial_count - 1
        with pytest.raises(ContactNotFoundError):
            test_phonebook.find_by_id(1)


class TestFileOperations:
    def test_save_and_load(self, temp_file):
        pb = PhoneBook(FileHandler(temp_file))
        pb.add_contact(Contact(id=1, name="Test", phone="123", comment=""))
        pb.save()

        new_pb = PhoneBook(FileHandler(temp_file))
        new_pb.load()
        assert len(new_pb.contacts) == 1
        assert new_pb.contacts[0].name == "Test"

    def test_load_invalid_file(self, temp_file):
        with open(temp_file, 'w') as f:
            f.write("invalid json")

        pb = PhoneBook(FileHandler(temp_file))
        with pytest.raises(FileOperationError):
            pb.load()


@pytest.mark.parametrize("phone,valid", [
    ("1234567890", True),
    ("12 34 56", True),
    ("abc", False),
    ("", False)
])
def test_phone_validation(phone, valid):
    if valid:
        Contact(id=1, name="Test", phone=phone, comment="")
    else:
        with pytest.raises(ValidationError):
            Contact(id=1, name="Test", phone=phone, comment="")