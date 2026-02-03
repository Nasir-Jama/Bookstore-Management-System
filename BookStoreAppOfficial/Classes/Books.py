from datetime import datetime
from typing import Optional


class Book:
    def __init__(
        self,
        title: str,
        author: str,
        price: float,
        quantity: int,
        book_id: Optional[int] = None
    ):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.price = price
        self.quantity = quantity
        self.__date_created = datetime.now()

    @property
    def book_id(self) -> Optional[int]:
        return self.__book_id

    @book_id.setter
    def book_id(self, value: Optional[int]) -> None:
        if value is not None and value < 0:
            raise ValueError("book_id must be a positive integer or None")
        self.__book_id = value

    @property
    def title(self) -> str:
        return self.__title

    @title.setter
    def title(self, value: str) -> None:
        if not value.strip():
            raise ValueError("title cannot be empty")
        self.__title = value

    @property
    def author(self) -> str:
        return self.__author

    @author.setter
    def author(self, value: str) -> None:
        if not value.strip():
            raise ValueError("author cannot be empty")
        self.__author = value

    @property
    def price(self) -> float:
        return self.__price

    @price.setter
    def price(self, value: float) -> None:
        if value < 0:
            raise ValueError("price cannot be negative")
        self.__price = value

    @property
    def quantity(self) -> int:
        return self.__quantity

    @quantity.setter
    def quantity(self, value: int) -> None:
        if value < 0:
            raise ValueError("quantity cannot be negative")
        self.__quantity = value

    @property
    def date_created(self) -> datetime:
        return self.__date_created
