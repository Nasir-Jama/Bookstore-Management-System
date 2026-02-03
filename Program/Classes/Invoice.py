from datetime import datetime
from typing import Optional

from Classes.Order import Order

class Invoice:
    """
    Invoice = HOW MUCH the customer must pay.
    Created FROM an Order.
    """

    TAX_RATE = 0.07

    def __init__(
        self,
        invoice_id: int,
        order: Order,
        customer_snapshot: dict,
        book_snapshot: dict,
        unit_price: float,
        shipping_cost: float,
        discount: float = 0.0
    ):
        self.invoice_id = invoice_id
        self.order = order

        # FROZEN DATA (never changes)
        self.customer = customer_snapshot
        self.book = book_snapshot
        self.unit_price = float(unit_price)
        self.shipping_cost = float(shipping_cost)
        self.discount = float(discount)

        self.paid = False
        self.payment_method: Optional[str] = None
        self.invoice_date = datetime.now()

        if self.discount < 0:
            raise ValueError("Discount cannot be negative.")
        if self.discount > self.subtotal:
            raise ValueError("Discount cannot exceed subtotal.")

    # ---------- CALCULATIONS ----------

    @property
    def subtotal(self) -> float:
        return self.unit_price * self.order.quantity

    @property
    def tax_amount(self) -> float:
        return (self.subtotal - self.discount) * self.TAX_RATE

    @property
    def total_due(self) -> float:
        return (
            self.subtotal
            - self.discount
            + self.tax_amount
            + self.shipping_cost
        )

    # ---------- ACTIONS ----------

    def mark_as_paid(self, method: str):
        self.paid = True
        self.payment_method = method

    # ---------- DISPLAY ----------

    def __str__(self) -> str:
        status = "PAID" if self.paid else "UNPAID"

        return (
            "==================== INVOICE ====================\n"
            f"Invoice ID:      {self.invoice_id}\n"
            f"Invoice Date:    {self.invoice_date.strftime('%Y-%m-%d %H:%M')}\n"
            f"Status:          {status}\n"
            "-------------------------------------------------\n"
            f"Customer:        {self.customer['name']}\n"
            f"Email:           {self.customer['email']}\n"
            f"Phone:           {self.customer['phone']}\n"
            "-------------------------------------------------\n"
            f"Book:            {self.book['title']}\n"
            f"Author:          {self.book['author']}\n"
            f"Quantity:        {self.order.quantity}\n"
            f"Unit Price:      ${self.unit_price:.2f}\n"
            "-------------------------------------------------\n"
            f"Subtotal:        ${self.subtotal:.2f}\n"
            f"Tax:             ${self.tax_amount:.2f}\n"
            f"Shipping:        ${self.shipping_cost:.2f}\n"
            "-------------------------------------------------\n"
            f"TOTAL DUE:       ${self.total_due:.2f}\n"
            f"Payment Method:  {self.payment_method or 'N/A'}\n"
            "================================================="
        )
