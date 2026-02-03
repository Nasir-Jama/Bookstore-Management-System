import tkinter as tk


class Dashboard(tk.Frame):
    def __init__(self, parent, store):
        super().__init__(parent, bg="#F8FAFC")
        self.store = store
        self.root = self.winfo_toplevel()

        self.columnconfigure(0, weight=1)

        pad = 5
        title_text = self.__class__.__name__
        description_text = "Here’s a quick overview of your bookstore’s performance and recent activity."

        # ================= HEADER =================
        tk.Label(self,text=title_text,font=("Arial", 20, "bold"),bg="#F8FAFC",fg="#0F172A",padx=pad).grid(row=0, column=0, sticky="w")

        tk.Label(self,text=description_text,font=("Arial", 12),bg="#F8FAFC",fg="#0F172A", padx=pad,justify="left",anchor="w").grid(row=1, column=0, sticky="w")

        # ================= STATS =================
        stats_frame = tk.Frame(self, bg="#F8FAFC")
        stats_frame.grid(row=2, column=0, sticky="w", padx=24, pady=16)

        self.card_total_books = self.make_card(stats_frame, "0", "Total Books")
        self.card_total_orders = self.make_card(stats_frame, "0", "Total Orders")
        self.card_total_customers = self.make_card(stats_frame, "0", "Total Customers")
        self.card_revenue = self.make_card(stats_frame, "£0.00", "Revenue")

        # ================= LOWER =================
        lower_frame = tk.Frame(self, bg="#F8FAFC")
        lower_frame.grid(row=3, column=0, sticky="nsew", padx=24, pady=20)
        lower_frame.columnconfigure(0, weight=2)
        lower_frame.columnconfigure(1, weight=1)

        self.recent_orders_frame = tk.Frame(lower_frame,bg="#FFFFFF",highlightbackground="#E5E7EB",highlightthickness=1,height=300)
        self.recent_orders_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
        self.recent_orders_frame.pack_propagate(False)

        self.low_stock_frame = tk.Frame(lower_frame,bg="#FFFFFF",highlightbackground="#E5E7EB",highlightthickness=1,height=300)
        self.low_stock_frame.grid(row=0, column=1, sticky="nsew", padx=(12, 0))
        self.low_stock_frame.pack_propagate(False)

        self.build_recent_orders()
        self.build_low_stock()
        self.refresh()

    # ==================================================
    # CARD
    # ==================================================

    def make_card(self, parent, value, label):
        frame = tk.Frame(parent,bg="#FFFFFF",width=220,height=110,highlightbackground="#E5E7EB",highlightthickness=1)
        frame.pack(side="left", padx=8)
        frame.pack_propagate(False)

        value_label = tk.Label(frame,text=value,fg="#0F172A",bg="#FFFFFF",font=("Segoe UI", 22, "bold"))
        value_label.pack(pady=(14, 0))

        tk.Label(frame,text=label,fg="#6B7280",bg="#FFFFFF",font=("Segoe UI", 11)).pack(pady=(4, 10))

        return value_label

    # ==================================================
    # BUILD SECTIONS
    # ==================================================

    def build_recent_orders(self):
        for w in self.recent_orders_frame.winfo_children():
            w.destroy()

        tk.Label(
            self.recent_orders_frame,
            text="Recent Orders",
            bg="#FFFFFF",
            fg="#0F172A",
            font=("Segoe UI", 13, "bold")
        ).pack(anchor="w", padx=16, pady=(12, 8))

        self.recent_orders_list = tk.Frame(self.recent_orders_frame, bg="#FFFFFF")
        self.recent_orders_list.pack(fill="both", expand=True, padx=16)

    def build_low_stock(self):
        for w in self.low_stock_frame.winfo_children():
            w.destroy()

        tk.Label(
            self.low_stock_frame,
            text="Low Stock",
            bg="#FFFFFF",
            fg="#0F172A",
            font=("Segoe UI", 13, "bold")
        ).pack(anchor="w", padx=16, pady=(12, 8))

        self.low_stock_list = tk.Frame(self.low_stock_frame, bg="#FFFFFF")
        self.low_stock_list.pack(fill="both", expand=True, padx=16)

    # ==================================================
    # REFRESH (AUTO-CALLED)
    # ==================================================

    def refresh(self):
        # ----- CARDS -----
        self.card_total_books.config(text=str(len(self.store.books)))
        self.card_total_orders.config(text=str(len(self.store.orders)))
        self.card_total_customers.config(text=str(len(self.store.customers)))

        revenue = sum(
            inv.total_due
            for inv in self.store.invoices.values()
            if inv.paid
        )
        self.card_revenue.config(text=f"£{revenue:,.2f}")

        # ----- RECENT ORDERS -----
        for w in self.recent_orders_list.winfo_children():
            w.destroy()

        recent = sorted(
            self.store.orders.values(),
            key=lambda o: o.order_date,
            reverse=True
        )[:5]

        if not recent:
            tk.Label(
                self.recent_orders_list,
                text="No orders yet.",
                bg="#FFFFFF",
                fg="#6B7280"
            ).pack(anchor="w")
        else:
            for o in recent:
                c = self.store.customers[o.customer_id]
                b = self.store.books[o.book_id]
                tk.Label(
                    self.recent_orders_list,
                    text=f"#{o.order_id} • {c.first_name} {c.last_name} • {b.title}",
                    bg="#FFFFFF",
                    anchor="w"
                ).pack(anchor="w", pady=2)

        # ----- LOW STOCK -----
        for w in self.low_stock_list.winfo_children():
            w.destroy()

        low_stock = [b for b in self.store.books.values() if b.quantity <= 3]

        if not low_stock:
            tk.Label(
                self.low_stock_list,
                text="All books sufficiently stocked.",
                bg="#FFFFFF",
                fg="#6B7280"
            ).pack(anchor="w")
        else:
            for b in low_stock:
                tk.Label(
                    self.low_stock_list,
                    text=f"{b.title} — {b.quantity} left",
                    bg="#FFFFFF",
                    fg="#DC2626",
                    anchor="w"
                ).pack(anchor="w", pady=2)
