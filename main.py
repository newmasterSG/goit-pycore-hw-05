from enum import Enum
from typing import Callable, Dict, Tuple

class Command(Enum):
    HELLO = 1
    ADD = 2
    CHANGE = 3
    PHONE = 4
    ALL = 5
    CLOSE = 6
    EXIT = 7

def input_error(func: Callable):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError as e:
            return str(e) if str(e) else "No such contact in the address book."
        except ValueError as e:
            return str(e)
        except Exception:
            return "An unexpected error occurred. Please try again."
    return inner


def parse_command(user_input: str) -> Tuple[str, ...]:
    user_input = user_input.strip()
    if not user_input:
        return ("",)

    cmd, *args = user_input.split()
    cmd = cmd.strip().upper()
    return (cmd, *args)


def _is_valid_phone(phone: str) -> bool:
    return (phone.startswith("+") and phone[1:].isdigit()) or phone.isdigit()


@input_error
def add_contact(args, contacts: Dict[str, str]) -> str:
    if len(args) != 2:
        raise ValueError("Usage: add name phone")
    name, phone = args
    if name in contacts:
        raise ValueError("Contact already exists. Use: change name phone")
    if not _is_valid_phone(phone):
        raise ValueError("The phone must contain only digits (optionally starting with '+').")
    contacts[name] = phone
    return "Contact added."


@input_error
def change_contact(args, contacts: Dict[str, str]) -> str:
    if len(args) != 2:
        raise ValueError("Usage: change name phone")
    name, phone = args
    if name not in contacts:
        raise ValueError("No such contact in the address book. Add it first with: add name phone.")
    if not _is_valid_phone(phone):
        raise ValueError("The phone must contain only digits (optionally starting with '+').")
    contacts[name] = phone
    return "Contact updated."


@input_error
def show_phone(args, contacts: Dict[str, str]) -> str:
    if len(args) != 1:
        raise ValueError("Usage: phone <name>")
    (name,) = args
    if name not in contacts:
        raise KeyError("No such contact in the address book.")
    return contacts[name]


def show_all(contacts: Dict[str, str]) -> str:
    if not contacts:
        return "No contacts yet"
    return ", ".join(f"{k} - {v}" for k, v in contacts.items())


def main() -> None:
    contacts: Dict[str, str] = {}
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command ")
        parsed = parse_command(user_input)

        if not parsed or not parsed[0]:
            print("Unknown command. Available: " + ", ".join(c.name.lower() for c in Command))
            continue

        command, *args = parsed

        if command in {Command.CLOSE.name, Command.EXIT.name}:
            break
        elif command == Command.ADD.name:
            print(add_contact(args, contacts))
        elif command == Command.PHONE.name:
            print(show_phone(args, contacts))
        elif command == Command.CHANGE.name:
            print(change_contact(args, contacts))
        elif command == Command.ALL.name:
            print(show_all(contacts))
        elif command == Command.HELLO.name:
            print("How can I help you?")
        else:
            print("Unknown command. Available: " + ", ".join(c.name.lower() for c in Command))


if __name__ == "__main__":
    main()