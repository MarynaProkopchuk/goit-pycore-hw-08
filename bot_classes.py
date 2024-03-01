from collections import UserDict
from datetime import datetime, timedelta
class Field:
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, name):
        super().__init__(name)

class Phone(Field):
    def __init__(self, phone):
        if len(phone)==10 and phone.isdigit() == True:        
            super().__init__(phone)
        else:
            raise ValueError ("phone number must consist of 10 digits") 

class Birthday(Field):
    def __init__(self, birthday):
        try:
            self.birthday = datetime.strptime(birthday, "%d.%m.%Y").date()
            super().__init__(birthday)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, phone, new_phone):
            if phone in [p.value for p in self.phones]: 
                self.remove_phone(phone)
                self.add_phone(new_phone)
            else:
                raise ValueError ("the phone is not in the list")

    def find_phone(self,phone):
        for p in self.phones:
            if p.value==phone:
                return p
            
    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)
    
    def __str__(self):
        if self.birthday !=None:
            return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday.value}"
        else:
            return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"
     
class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record
 
    def find(self, name):
        return self.data.get(name)
    
    def delete(self, name):
        return self.data.pop(name)
       
    def get_upcoming_birthdays(self):
        self.birthdays = []
        for record in self.data.values():
            if record.birthday !=None:
                self.birthdays.append({"name":record.name.value, "birthday": record.birthday.value})
        today=datetime.today().date()
        birthday = []
        for user in self.birthdays:
            birth_date = datetime.strptime(((user["birthday"])[:6] + str(today.year)), "%d.%m.%Y").date()
            week_day = birth_date.weekday()
            if 0<(birth_date-today).days<7:
                if week_day<5:
                    birthday.append({user['name']:birth_date.strftime("%d.%m.%Y")})
                elif week_day==5:
                    birth_date=(birth_date+timedelta(days=2))
                    birthday.append({user['name']:birth_date.strftime("%d.%m.%Y")})
                else:
                    birth_date=(birth_date+timedelta(days=1))
                    birthday.append({user['name']:birth_date.strftime("%d.%m.%Y")})
        return birthday

