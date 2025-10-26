from enum import Enum

class Command(Enum):
    HELLO = 1
    ADD = 2
    CHANGE = 3
    PHONE = 4
    ALL = 5
    CLOSE = 6
    EXIT = 7

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Write correct command for adding contact to dictionary"
        except ValueError as e:
            return str(e)
        
    return inner

def parse_command(user_input: str):
    cmd, *args = user_input.split()
    cmd = cmd.strip().upper()
    return cmd, *args
    
@input_error
def add_contact(args, contacts):
    name, phone = args
    name = name.strip()
    phone = phone.strip()
    
    if not name:
        raise ValueError("The name must not be empty")
    
    if name in contacts.keys():
        raise ValueError('Write correct command for changing information')
    
    if not (phone.startswith('+') and phone[1:].isdigit() or phone.isdigit()):
        raise ValueError("The phone number must contain only digits (and optionally a leading ‘+’)")
    
    contacts[name] = phone
    return 'Contact added'

@input_error
def change_contact(args, contacts):
    name, phone = args
    name = name.strip()
    phone = phone.strip()
    
    contacts[name] = phone
    return 'Contact added'

@input_error
def show_phone(args, contacts):
    name, = args
    name = name.strip()
    
    return contacts[name]

def show_all(contacts):
    return ", ".join(f"{k} - {v}" for k, v in contacts.items())


def main(): 
    contacts = {}
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command ")
        command, *args = parse_command(user_input)

        if command == Command.CLOSE.name or command == Command.EXIT.name:
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
            print('How can I help you?')
        else:
            print('Write correct comamnd: ')
            for correct_command in (Command):
                print(correct_command.name.lower())




if __name__ == "__main__":
    main()