import pytest
from phone_book.models import Contact, PhoneBook, FileHandler

@pytest.fixture
def temp_file(tmp_path):
    file = tmp_path / "test_contacts.json"
    file.write_text("[]")
    return str(file)

@pytest.fixture
def test_phonebook(temp_file):
    handler = FileHandler(temp_file)
    pb = PhoneBook(handler)
    pb.add_contact(Contact(id=1, name="Иван", phone="123", comment="Друг"))
    pb.add_contact(Contact(id=2, name="Петр", phone="456", comment="Работа"))
    return pb