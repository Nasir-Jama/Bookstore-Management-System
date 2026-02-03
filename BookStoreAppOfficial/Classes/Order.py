from datetime import datetime
from typing import Optional

class Order:
    """
    Order = WHAT the customer wants to buy.
    No prices. No totals. No tax.
    """

    def __init__(
        self,
        order_id: int,
        customer_id: int,
        book_id: int,
        quantity: int,
        urgent_shipping: bool,
        shipping_cost: bool
    ):

        self.order_id = order_id
        self.customer_id = customer_id
        self.book_id = book_id
        self.quantity = quantity
        self.urgent_shipping = urgent_shipping
        self.shipping_cost = shipping_cost
        self.order_date = datetime.now()

