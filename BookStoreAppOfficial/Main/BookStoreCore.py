from Classes.Customer import Customer
from Classes.Author import Author
from Classes.Books import Book
from Classes.Order import Order
from Classes.Invoice import Invoice

class Store:
    """
    Central manager for all bookstore data.
    - Orders = buying intent
    - Invoices = billing (created AFTER orders)
    """

    def __init__(self):
        # Core storage
        self.__books: dict[int, Book] = {}
        self.__authors: dict[int, Author] = {}
        self.__customers: dict[int, Customer] = {}
        self.__orders: dict[int, Order] = {}
        self.__invoices: dict[int, Invoice] = {}

        # ID counters
        self.__ids = {
            "book": 0,
            "author": 0,
            "customer": 0,
            "order": 0,
            "invoice": 0,
        }

    # ---------- Properties ----------

    @property
    def books(self) -> dict[int, Book]:
        return self.__books

    @property
    def authors(self) -> dict[int, Author]:
        return self.__authors

    @property
    def customers(self) -> dict[int, Customer]:
        return self.__customers

    @property
    def orders(self) -> dict[int, Order]:
        return self.__orders

    @property
    def invoices(self) -> dict[int, Invoice]:
        return self.__invoices
    
    @property
    def _ids(self): 
        return self.__ids

    # ============================================================
    #                           HELPERS
    # ============================================================

    def _next_id(self, key: str) -> int:
        value = self._ids[key]
        self._ids[key] += 1
        return value

    def _calculate_shipping(self, urgent: bool, shipping_costs: bool, quantity: int) -> float:
        """
        Centralized shipping rule.
        Invoice will freeze this value at creation time.
        """

        urgent_fee = 7.50 if urgent else 0.0
        shipping = 5 if shipping_costs else 0.0
        per_item = 0.50 * max(0, quantity - 1)
        return shipping + urgent_fee + per_item

    # ============================================================
    #                           AUTHORS
    # ============================================================

    def add_author(self,first_name: str,last_name: str,email_address: str,phone_number: str) -> Author:
        author_id = self._next_id("author")
        author = Author(first_name, last_name, email_address, phone_number, author_id)
        self.authors[author_id] = author
        return author

    def find_author(self, author_id: int) -> Author | None:
        return self.authors.get(int(author_id))

    def edit_author(self,author_id: int,first_name: str,last_name: str,email_address: str,phone_number: str):
        if author_id not in self.authors:
            raise ValueError("Author not found")

        a = self.authors[author_id]
        a.first_name = first_name
        a.last_name = last_name
        a.email_address = email_address
        a.phone_number = phone_number

    def delete_author(self, author_id: int) -> bool:
        if author_id not in self.authors:
            raise ValueError("Author not found")
        del self.authors[author_id]
        return True

    # ============================================================
    #                           BOOKS
    # ============================================================

    def add_book(self,title: str,author_id: int,price: float,quantity: int) -> Book:
        author = self.find_author(author_id)
        if not author:
            raise ValueError("Author not found")

        book_id = self._next_id("book")
        author_name = f"{author.first_name} {author.last_name}"
        book = Book(title, author_name, float(price), int(quantity), book_id)
        self.books[book_id] = book
        return book

    def find_book(self, book_id: int) -> Book | None:
        return self.books.get(int(book_id))

    def list_books(self) -> list[Book]:
        return list(self.books.values())

    def find_books_by_author(self, author_id: int) -> list[Book]:
        author = self.find_author(author_id)
        if not author:
            raise ValueError("Author not found")

        full_name = f"{author.first_name} {author.last_name}"
        return [b for b in self.books.values() if b.author == full_name]

    def delete_book(self, book_id: int) -> bool:
        if book_id not in self.books:
            raise ValueError("Book not found")
        del self.books[book_id]
        return True

    # ============================================================
    #                           CUSTOMERS
    # ============================================================

    def add_customer(self,first_name: str,last_name: str,email_address: str,phone_number: str) -> Customer:
        customer_id = self._next_id("customer")
        customer = Customer(first_name, last_name, email_address, phone_number, customer_id)
        self.customers[customer_id] = customer
        return customer

    def edit_customer(self,customer_id: int,first_name: str,last_name: str,email_address: str,phone_number: str):
        if customer_id not in self.customers:
            raise ValueError("Customer not found")

        c = self.customers[customer_id]
        c.first_name = first_name
        c.last_name = last_name
        c.email_address = email_address
        c.phone_number = phone_number

    def delete_customer(self, customer_id: int) -> bool:
        if customer_id not in self.customers:
            raise ValueError("Customer not found")
        del self.customers[customer_id]
        return True

    # ============================================================
    #                           ORDERS
    # ============================================================

    def add_order(self,customer_id: int,book_id: int,quantity: int,urgent_shipping: bool, shipping_cost: bool) -> Order:
        if customer_id not in self.customers:
            raise ValueError("Customer not found")

        book = self.find_book(book_id)
        if not book:
            raise ValueError("Book not found")

        qty = int(quantity)
        if qty <= 0:
            raise ValueError("Quantity must be greater than zero.")
        if book.quantity < qty:
            raise ValueError("Not enough stock.")

        # Inventory update happens at ORDER time
        book.quantity -= qty

        order_id = self._next_id("order")
        order = Order(order_id, customer_id, book_id, qty, urgent_shipping, shipping_cost)
        self.orders[order_id] = order

        # ---------- AUTO-CREATE INVOICE ----------
        self._create_invoice_from_order(order)

        return order

    def find_order(self, order_id: int) -> Order | None:
        return self.orders.get(int(order_id))

    def list_orders(self) -> list[Order]:
        return list(self.orders.values())

    def find_orders_by_customer(self, customer_id: int) -> list[Order]:
        return [o for o in self.orders.values() if o.customer_id == customer_id]

    # ============================================================
    #                           INVOICES
    # ============================================================

    def _create_invoice_from_order(self, order: Order) -> Invoice:
        customer = self.customers[order.customer_id]
        book = self.books[order.book_id]

        invoice_id = self._next_id("invoice")

        customer_snapshot = {
            "customer_id": customer.customer_id,
            "name": f"{customer.first_name} {customer.last_name}",
            "email": customer.email_address,
            "phone": customer.phone_number,
        }

        book_snapshot = {
            "book_id": book.book_id,
            "title": book.title,
            "author": book.author,
        }

        shipping_cost = self._calculate_shipping(order.urgent_shipping, order.shipping_cost, order.quantity)

        invoice = Invoice(
            invoice_id=invoice_id,
            order=order,
            customer_snapshot=customer_snapshot,
            book_snapshot=book_snapshot,
            unit_price=book.price,      # price frozen here
            shipping_cost=shipping_cost # shipping frozen here
        )

        self.invoices[invoice_id] = invoice
        return invoice

    def find_invoice(self, invoice_id: int) -> Invoice | None:
        return self.invoices.get(int(invoice_id))

    def delete_invoice(self, invoice_id: int) -> bool:
        invoice = self.find_invoice(invoice_id)
        if not invoice:
            raise ValueError("Invoice not found")

        if invoice.paid:
            raise ValueError("Cannot delete a PAID invoice.")

        del self.invoices[invoice_id]
        return True
