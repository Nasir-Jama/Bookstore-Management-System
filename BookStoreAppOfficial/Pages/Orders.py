import tkinter as TK
from tkinter import ttk as TTK, messagebox


class Orders(TK.Frame):

    def __init__(self, parent, store):
        super().__init__(parent, bg="#F8FAFC")
        self.store = store
        self.root = self.winfo_toplevel()

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)
        self.rowconfigure(3, weight=1)

        # ================= HEADER =================
        header = TK.Frame(self, bg="#F8FAFC")
        header.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        header.columnconfigure(0, weight=1)

        TK.Label(header,text="Orders",font=("Arial", 20, "bold"),bg="#F8FAFC").grid(row=0, column=0, sticky="w")

        TK.Label(header,text="Create customer orders. Invoices are generated automatically.",font=("Arial", 12),bg="#F8FAFC").grid(row=1, column=0, sticky="w")

        # ================= SEARCH =================
        search_frame = TK.Frame(self, bg="#F8FAFC")
        search_frame.grid(row=1, column=0, sticky="ew", padx=24, pady=(0, 10))
        search_frame.columnconfigure(1, weight=1)

        TK.Label(search_frame, text="Search:", bg="#F8FAFC").grid(row=0, column=0, sticky="w")

        self.search_var = TK.StringVar()
        self.search_var.trace_add("write", lambda *_: self.refresh())

        TK.Entry(search_frame, textvariable=self.search_var).grid(row=0, column=1, sticky="ew", padx=(8, 0))

        # ================= TABLE =================
        table_container = TK.Frame(self, bg="#F8FAFC")
        table_container.grid(row=3, column=0, sticky="nsew", padx=(24, 10), pady=10)
        table_container.rowconfigure(0, weight=1)
        table_container.columnconfigure(0, weight=1)

        columns = ("Order ID", "Customer", "Book", "Quantity", "Urgent", "Order Date")

        self.table = TTK.Treeview(table_container, columns=columns, show="headings", height=25, style="Borderless.Treeview")
        self.table.grid(row=0, column=0, sticky="nsew", padx=12, pady=12)

        for col in columns:
            self.table.heading(col, text=col)
            self.table.column(col, anchor="center", width=160)

        # ================= BUTTONS =================
        buttons = TK.Frame(self, bg="#F8FAFC", width=220)
        buttons.grid(row=3, column=1, sticky="ns", padx=(0, 24), pady=10)

        self.add_btn = TTK.Button(buttons, text="Add Order", style="Side.TButton", command=self.create_order_form)
        self.add_btn.grid(sticky="ew", pady=6)

        self.refresh()

    # ================= CREATE ORDER =================

    def create_order_form(self):
        if not self.store.customers:
            messagebox.showwarning(
                "No customers",
                "You must add a customer before creating an order."
            )
            return

        if not self.store.books:
            messagebox.showwarning(
                "No books",
                "You must add a book before creating an order."
            )
            return

        form = TK.Toplevel(self, bg="#F8FAFC")
        form.title("Create Order")
        form.geometry("420x420")
        form.grab_set()

        # ----- CUSTOMER -----
        TK.Label(form, text="Customer", bg="#F8FAFC").pack(anchor="w", padx=24, pady=(16, 0))

        cust_var = TK.StringVar()
        customers = {f"{c.first_name} {c.last_name} (ID {c.customer_id})": c.customer_id for c in self.store.customers.values()}

        cust_box = TTK.Combobox(form, textvariable=cust_var, values=list(customers.keys()), state="readonly")
        cust_box.pack(fill="x", padx=24)

        # ----- BOOK -----
        TK.Label(form, text="Book", bg="#F8FAFC").pack(anchor="w", padx=24, pady=(12, 0))

        book_var = TK.StringVar()
        books = {f"{b.title} (ID {b.book_id})": b.book_id for b in self.store.books.values()}

        book_box = TTK.Combobox(form, textvariable=book_var, values=list(books.keys()),state="readonly")
        book_box.pack(fill="x", padx=24)

        # ----- QUANTITY -----
        TK.Label(form, text="Quantity", bg="#F8FAFC")\
            .pack(anchor="w", padx=24, pady=(12, 0))

        qty_entry = TK.Entry(form)
        qty_entry.pack(fill="x", padx=24)

        # ----- SHIPPING -----
        shipping_var = TK.BooleanVar()
        urgent_var = TK.BooleanVar()

        TK.Checkbutton(form, text="Add Shipping Cost", variable=shipping_var, bg="#F8FAFC").pack(anchor="w", padx=24, pady=8)

        TK.Checkbutton(form, text="Urgent Shipping", variable=urgent_var,bg="#F8FAFC").pack(anchor="w", padx=24, pady=8)

        save_btn = TK.Button(form, text="Create Order",bg="#111827", fg="white",state="disabled")
        save_btn.pack(pady=20)

        # ----- VALIDATION -----
        def validate():
            try:
                valid = (
                    cust_var.get() and
                    book_var.get() and
                    int(qty_entry.get()) > 0
                )
            except ValueError:
                valid = False

            save_btn.config(state="normal" if valid else "disabled")

        for w in (qty_entry,):
            w.bind("<KeyRelease>", lambda *_: validate())
        cust_box.bind("<<ComboboxSelected>>", lambda *_: validate())
        book_box.bind("<<ComboboxSelected>>", lambda *_: validate())

        # ----- SAVE -----
        def save():
            try:
                self.store.add_order(
                    customer_id=customers[cust_var.get()],
                    book_id=books[book_var.get()],
                    quantity=int(qty_entry.get()),
                    urgent_shipping=urgent_var.get(),
                    shipping_cost=shipping_var.get(),
                )
                self.root.event_generate("<<RefreshAll>>")
                form.destroy()

            except Exception as e:
                messagebox.showerror("Error", str(e))

        save_btn.config(command=save)
        validate()

    # ================= REFRESH (DYNAMIC SEARCH) =================

    def refresh(self):
        self.table.delete(*self.table.get_children())
        query = self.search_var.get().strip().lower()
        


        for o in self.store.orders.values():
            c = self.store.customers[o.customer_id]
            b = self.store.books[o.book_id]

            text = f"{o.order_id} {c.first_name} {c.last_name} {b.title}".lower()

            if query and query not in text:
                continue

            self.table.insert(
                "",
                TK.END,
                values=(
                    o.order_id,
                    f"{c.first_name} {c.last_name}",
                    b.title,
                    o.quantity,
                    "Yes" if o.urgent_shipping else "No",
                    o.order_date.strftime("%d/%m/%Y %H:%M"),
                )
            )
