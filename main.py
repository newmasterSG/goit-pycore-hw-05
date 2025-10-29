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

@input_error
def parse_command(user_input: str) -> Tuple[str, ...]:
    user_input = user_input.strip()

    cmd, *args = user_input.split()
    cmd = cmd.strip().upper()

    return (cmd, *args)


@input_error
def add_contact(args, contacts: Dict[str, str]) -> str:
    name, phone = args
    contacts[name] = phone
    return "Contact added."


@input_error
def change_contact(args, contacts: Dict[str, str]) -> str:
    name, phone = args
    contacts[name] = phone
    return "Contact updated."


@input_error
def show_phone(args, contacts) -> str:
    (name,) = args
    return contacts[name]


def show_all(contacts: Dict[str, str]) -> str:
    if not contacts:
        return "No contacts yet"
    return ", ".join(f"{k} - {v}" for k, v in contacts.items())


def main() -> None:
    contacts = {}
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command ")
        parsed = parse_command(user_input)
    
        if parsed == "Enter the argument for the command":
            print(parsed) 
        
        else:
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