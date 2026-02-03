from Classes.Person import Person
from typing import Optional

class Customer(Person):
    def __init__(
        self,
        first_name: str,
        last_name: str,
        email_address: str,
        phone_number: str,
        customer_id: Optional[int] = None
    ):
        super().__init__(first_name, last_name, email_address, phone_number)
        self.customer_id = customer_id
