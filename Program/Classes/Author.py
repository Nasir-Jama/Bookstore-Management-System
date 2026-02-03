from Classes.Person import Person
from typing import Optional

class Author(Person):
    def __init__(
        self,
        first_name: str,
        last_name: str,
        email_address: str,
        phone_number: str,
        author_id: Optional[int] = None
    ):
        super().__init__(first_name, last_name, email_address, phone_number)
        self.author_id = author_id

