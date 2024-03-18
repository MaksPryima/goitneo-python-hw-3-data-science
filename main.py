from datetime import datetime
import json
from address_book import *
import birthdays_next_week


def input_error(func):
    """Checks if input format is correct and messages if not so"""

    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Wrong format."
        except KeyError:
            return "Contact not found."
        except IndexError:
            return "Invalid index."

    return inner


@input_error
def parse_input(user_input):
    """Defines command and arguments"""
    while not user_input:  # In case empty input was given
        user_input = input("Enter a command: ")
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def find_record(name: str, contacts: AddressBook):
    """Checks if such record in the address book"""
    for recname in contacts.data.keys():
        if name == recname.value:
            return contacts.data[recname]


@input_error
def add_contact(args, contacts: AddressBook):
    """Adds contact to contact list"""
    name = args[0]
    rec = find_record(name, contacts)
    if rec:
        return "Contact is already in list."
    contacts.add_record(Record(name))
    return "Contact added."


@input_error
def add_number(args, contacts: AddressBook):
    """Adds contact`s phone number"""
    name, phone_number = args
    rec = find_record(name, contacts)
    if rec:
        return rec.add_phone(phone_number)
    return "No such contact."


@input_error
def add_birthday(args, contacts: AddressBook):
    """Adds contact`s birthday"""
    name, day, month, year = args
    rec = find_record(name, contacts)
    if rec:
        return rec.add_birthday(int(year), int(month), int(day))
    return "No such contact."


@input_error
def show_phones(args, contacts: AddressBook):
    """Shows contact`s phone number(s) if such contact is(are) in contact list"""
    name = args[0]
    rec = find_record(name, contacts)
    if rec:
        return (
            "; ".join([phone.value for phone in rec.phones])
            if rec.phones
            else "No numbers added."
        )
    return "No such contact."


@input_error
def show_birthday(args, contacts: AddressBook):
    """Shows contact`s birthday if such contact is(are) in contact list"""
    name = args[0]
    rec = find_record(name, contacts)
    if rec:
        return (
            rec.birthday.value.strftime("%d.%m.%Y")
            if rec.birthday
            else "No birthday added."
        )
    return "No such contact."


@input_error
def change_number(args, contacts: AddressBook):
    """Changes contact`s phone number"""
    name, old, new = args
    rec = find_record(name, contacts)
    if rec:
        return rec.edit_phone(old, new)
    return "No such contact."


@input_error
def change_birthday(args, contacts: AddressBook):
    """Changes contact`s birthday"""
    name, new_day, new_month, new_year = args
    rec = find_record(name, contacts)
    if rec:
        return rec.edit_birthday(int(new_year), int(new_month), int(new_day))
    return "No such contact."


@input_error
def delete_contact(args, contacts: AddressBook):
    """Deletes contact if it is in contact list"""
    name = args[0]
    rec = find_record(name, contacts)
    if rec:
        return contacts.delete(name)
    return "No such contact."


@input_error
def delete_number(args, contacts: AddressBook):
    """Deletes contact`s number if it is in contact list"""
    name = args[0]
    phone_number = args[1]
    rec = find_record(name, contacts)
    if rec:
        return rec.delete_phone(phone_number)
    return "No such contact."


@input_error
def delete_birthday(args, contacts: AddressBook):
    """Deletes contact`s birthday if it is in contact list"""
    name = args[0]
    rec = find_record(name, contacts)
    if rec:
        return rec.delete_birthday()
    return "No such contact."


@input_error
def birthdays(contacts: AddressBook):
    """Shows if there are birthdays to celebrate next week according to the address book"""
    bdays = []
    for name, rec in contacts.items():
        if rec.birthday:
            bdays.append({"name": name.value, "birthday": rec.birthday.value})
    res = birthdays_next_week.get_birthdays_per_week(bdays)
    return res if res else "No birthdays to celebrate next week."


def save_data(contacts: AddressBook):
    """Saves all the data to .json file"""
    to_save = []
    with open("data.json", "w", encoding="utf-8") as file:
        for rec in contacts.data.values():
            to_save.append(
                {
                    "name": rec.name.value,
                    "phones": [phone.value for phone in rec.phones],
                    "birthday": (
                        rec.birthday.value.strftime("%d.%m.%Y")
                        if rec.birthday
                        else None
                    ),
                }
            )
        json.dump(to_save, file)


def load_data():
    """Loads all the data from .json file"""
    try:
        with open("data.json", "r", encoding="utf-8") as file:
            data = json.load(file)
    except json.decoder.JSONDecodeError:
        return AddressBook()
    addressbook = AddressBook()
    for person in data:
        bd = (
            datetime.strptime(person["birthday"], "%d.%m.%Y")
            if person["birthday"]
            else None
        )
        rec = Record(person["name"], Birthday(bd))
        for number in person["phones"]:
            rec.add_phone(number)
        addressbook.data[Name(person["name"])] = rec
    return addressbook


def print_contacts(contacts):
    """Prints all contacts if such in the address book"""
    to_print = contacts.contacts()
    if isinstance(to_print, str):
        print(to_print)
    else:
        for contact in to_print:
            print(contact)


def main():
    """Defines what function to run according to command"""
    contacts = load_data()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        args = None
        command, *args = parse_input(user_input)
        if command in ["close", "exit", "goodbye"]:
            save_data(contacts)
            print("Goodbye!")
            break
        if command == "hello":
            print("How can I help you?")
        elif command == "add-contact":
            print(add_contact(args, contacts))
        elif command == "add-number":
            print(add_number(args, contacts))
        elif command == "add-birthday":
            print(add_birthday(args, contacts))
        elif command == "all":
            print_contacts(contacts)
        elif command == "change-phone":
            print(change_number(args, contacts))
        elif command == "change-birthday":
            print(change_birthday(args, contacts))
        elif command == "show-phones":
            print(show_phones(args, contacts))
        elif command == "show-birthday":
            print(show_birthday(args, contacts))
        elif command == "delete-number":
            print(delete_number(args, contacts))
        elif command == "delete-contact":
            print(delete_contact(args, contacts))
        elif command == "delete-birthday":
            print(delete_birthday(args, contacts))
        elif command == "birthdays":
            for bday in birthdays(contacts):
                print(bday)
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
