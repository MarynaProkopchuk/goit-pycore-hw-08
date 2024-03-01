from bot_classes import AddressBook, Name, Phone, Field, Birthday, Record
import pickle

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

def input_error(func):
    def inner(*args, **kwargs):
        func_name=str(func).split(" ")[1]
        try:
            return func(*args, **kwargs)
        except ValueError:
            if func_name == "add_contact":
                return "Please write command 'add => name => phone', phone number must consist of 10 digits"
            elif func_name == "change_number":
                return "Please write command 'change => name => phone => new phone'"
            elif func_name == "add_birthday":
                return "Please write command 'add-birthday => name => birthday date', date must be in DD.MM.YYYY format"
        except AttributeError: 
               if func_name == "show_birthday":
                return "This contact doesn't have birthday date yet,\
                    \n if you want to add it write command 'add-birthday => name => birthday date'"
        except KeyError:
            if func_name == "change_number":
                return "There is no contact with this name in your list,\
                    \n if you want to add it, please write command - 'add => username => phone'"
        except IndexError:
            if func_name == "phone_username":
                return "Please write command 'phone => name'"    
    
    return inner

@input_error
def add_contact(args, book):
    name, phone = args
    name = name.capitalize()
    if name not in book:
        if name.isalpha()== True and phone.isdigit() == True:
            record = Record(name)
            book.add_record(record)
            record.add_phone(phone)
            return f"Contact {name} - {phone} added."
        else:
            return "Please write command 'add' => 'name' in letters => 'phone' in numbers'"
    else:
        return f"There is already contact with this name,\
            \n if you want to change it, please write command - 'change => username => phone'"
  
@input_error
def change_number(args, book):
    name, phone, new_phone = args
    name = name.capitalize()
    if name in book:
        record = book.find(name)
        record.edit_phone(phone,new_phone)
        return f"Contact {name} changed to {new_phone}"
    else:
        return "There is no contact with this name in your list,\
                    \n if you want to add it, please write command - 'add => username => phone'"
       
@input_error
def phone_username(args, book):
    name = args
    name = name[0].capitalize()
    if name in book:
        record = book.find(name)
        return f"{record}"
    else:
        return "There is no contact with this name in your list,\
                    \n if you want to add it, please write command - 'add => username => phone'" 


def show_all_conacts(book):             
    for record in book.data.values():
        print(record)


@input_error
def add_birthday(args, book): 
    name, birthday = args
    name = name.capitalize()
    if name in book:
        record = book.find(name)
        record.add_birthday(birthday)
        return f"Contact {name} - birthday: {birthday}"
    else:
        return "There is no contact with this name in your list" 

@input_error                       
def show_birthday(args, book):
    name = args
    name = name[0].capitalize()
    if name in book:
        record = book.find(name)
        return f"Contact {name} birthday: {record.birthday.value}"
    else:
        return "There is no contact with this name in your list" 


def birthdays(book):        
        birthdays=book.get_upcoming_birthdays()
        lst = ""
        for birthday in birthdays:
            for key, value in birthday.items():
                lst+= key + " - " + value + "\n"
        return f"{lst}\n Don't forgrt to congratulate!"

def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook() 

    
def main():
    book = load_data()
    print("Welcome to the assistant bot!\
          \n    say 'Hello'")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            save_data(book)
            print("Good bye!")
            break
        elif command == "hello":
            print(" Command 'add' - to add contact\
                  \n Command 'change' - to change phone in contact\
                  \n Command 'phone' - to find contact \
                  \n Command 'all' - to show all contacts \
                  \n Command 'add-birthday' - to add birthday to contact \
                  \n Command 'show-birthday' - to find birthday date of contact \
                  \n Command 'birthdays' - to show upcoming birthdays \
                  \n Command 'exit' or 'close' - to leave\
                  \n How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_number(args, book))
        elif command == "phone":
            print(phone_username(args, book))
        elif command == "all":
            print("Your contacts list:")
            show_all_conacts(book)
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
           print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(book))
        else:
            print("Invalid command.") 
    return book       
               

if __name__ == "__main__":
    main()
    

