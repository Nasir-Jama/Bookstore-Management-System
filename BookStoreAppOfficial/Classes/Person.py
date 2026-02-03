from datetime import datetime

class Person:
    def __init__(self, first_name: str, last_name: str, email_address: str, phone_number: str):
        self.first_name = first_name
        self.last_name = last_name
        self.email_address = email_address
        self.phone_number = phone_number
        self.__date_created = datetime.now()

    @property
    def first_name(self) -> str:
        return self.__first_name

    @first_name.setter
    def first_name(self, value: str):
        value = (value or "").strip()
        if len(value) < 2:
            raise ValueError("First name must be at least 2 characters.")
        self.__first_name = value

    @property
    def last_name(self) -> str:
        return self.__last_name

    @last_name.setter
    def last_name(self, value: str):
        value = (value or "").strip()
        if len(value) < 2:
            raise ValueError("Last name must be at least 2 characters.")
        self.__last_name = value

    @property
    def email_address(self) -> str:
        return self.__email_address

    @email_address.setter
    def email_address(self, value: str):
        value = (value or "").strip()
        if "@" not in value or "." not in value:
            raise ValueError("Invalid email address.")
        self.__email_address = value

    @property
    def phone_number(self) -> str:
        return self.__phone_number

    @phone_number.setter
    def phone_number(self, value: str):
        value = (value or "").strip()
        if not value.isdigit() or len(value) < 10:
            raise ValueError("Invalid phone number.")
        self.__phone_number = value

    @property
    def date_created(self) -> datetime:
        return self.__date_created
