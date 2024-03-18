from collections import UserDict
import re
from datetime import datetime


def is_correct(*args):
    """Checks if given number is ten digits or date is valid"""
    if len(args) == 3:
        try:
            year, month, day = args
            return (
                datetime(1900, 1, 1)
                < datetime(int(year), int(month), int(day))
                < datetime.today()
            )
        except ValueError:
            return False
    return re.fullmatch(r"\d{10}", args[0])

def validate_phone(number):
    """Checks if given number is ten digits"""
    return re.fullmatch(r"\d{10}", number)

def validate_email(value):
    pattern = r'^[\w\.-]+@[\w\.-]{2,}\.\w{2,}$'
    return re.match(pattern, value) is not None

class Field:
    """Represents a contact name or a phone number"""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    """Represents a contact`s name"""

    def __str__(self):
        return str(self.value)

class Phone(Field):
    """Represents a contact`s phone number"""

    def __init__(self, value):
        if validate_phone(value):
            self.value = value
        else:
            raise ValueError("Invalid email format")

    def __str__(self):
        return str(self.value)
    
class Email(Field):
    """Represents a contact's email"""

    def __init__(self, value):
        if validate_email(value):
            self.value = value
        else:
            raise ValueError("Invalid email format")

    def __str__(self):
        return str(self.value)
    
    
class Birthday(Field):
    """Represents a contact`s birthday"""

    def __str__(self):
        return str(self.value)


class Record:
    """Represents a contact that is going to be added"""

    def __init__(self, name: str, birthday: Birthday = None):
        self.name = Name(name)
        self.phones = []
        self.birthday = birthday

    def add_phone(self, number: str):
        """Adds the number to the record"""
        if is_correct(number):
            if number in (phone.value for phone in self.phones):
                return "Number already exists."
            else:
                self.phones.append(Phone(number))
                return "Number added."
        else:
            return "Wrong format."

    def delete_phone(self, number: str):
        """Deletes the number from the record"""
        for phone in self.phones:
            if phone.value == number:
                del self.phones[self.phones.index(phone)]
                return "Number deleted."
        return "No such number."

    def find_phone(self, number_to_find: str):
        """Finds the phone number in the record"""
        phones_found = list(
            filter(lambda phone: number_to_find in phone.value, self.phones)
        )
        if phones_found:
            return f"Phones found: {', '.join(phone.value for phone in phones_found)}"
        else:
            return "No such numbers."

    def edit_phone(self, current_number: str, new_number: str):
        """Changes the phone number if such is in the record"""
        if is_correct(new_number):
            for phone in self.phones:
                if phone.value == current_number:
                    phone.value = new_number
                    return "Number changed."
            return "No such number."
        else:
            return "Wrong format."

    def add_birthday(self, year: int, month: int, day: int):
        """Adds the birthday to the record"""
        if is_correct(year, month, day):
            if self.birthday:
                return "Birthday is already setted."
            else:
                self.birthday = Birthday(datetime(year, month, day))
                return "Birthday added."
        else:
            return "Wrong format."

    def edit_birthday(self, new_year: int, new_month: int, new_day: int):
        """Changes the birthday if such is in the record"""
        if is_correct(new_year, new_month, new_day):
            if self.birthday:
                self.birthday.value = datetime(new_year, new_month, new_day)
                return "Birthday changed."
            else:
                return "No birthday setted."
        else:
            return "Wrong format."

    def delete_birthday(self):
        """Deletes the birthday from the record"""
        if self.birthday:
            self.birthday = None
            return "Birthday deleted."
        else:
            return "No birthday setted."

    def __str__(self):
        if self.phones:
            phones = f"; phones: {', '.join(p.value for p in self.phones)}"
        else:
            phones = "; no phones added"
        if self.birthday:
            bd = f"; birthday is at {str(self.birthday.value.strftime('%d.%m.%Y'))}"
        else:
            bd = "; no birthday added"
        return f"Contact name: {self.name.value}" + phones + bd


class AddressBook(UserDict):
    """Represents an address book filled with contacts"""

    def add_record(self, rec: Record):
        """Adds contact to the address book"""
        self.data[rec.name] = rec
        return "Contact added."

    def find(self, name: str):
        """Finds contact in the address book"""
        for contact in self.data:
            if name == contact.value:
                return self.data[contact]
        return "No such contact."

    def delete(self, name: str):
        """Deletes contact from the address book"""
        for contact in self.data:
            if name == contact.value:
                del self.data[contact]
                return "Contact deleted."
        return "No such contact."

    def contacts(self):
        """Prints all contacts from the address book"""
        if self.data:
            return self.data.values()
        return "No contacts."
