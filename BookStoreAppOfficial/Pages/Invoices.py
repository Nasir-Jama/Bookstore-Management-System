import tkinter as TK
from tkinter import ttk as TTK, messagebox


class Invoices(TK.Frame):

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

        TK.Label(header, text="Invoices", font=("Arial", 20, "bold"), bg="#F8FAFC").grid(row=0, column=0, sticky="w")

        TK.Label(header, text="Review, generate, and manage billing and payment records.", font=("Arial", 12), bg="#F8FAFC").grid(row=1, column=0, sticky="w")

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

        columns = ("Invoice ID", "Order ID", "Customer", "Status", "Total", "Date")

        self.table = TTK.Treeview(table_container, columns=columns,show="headings",height=25,style="Borderless.Treeview")
        self.table.grid(row=0, column=0, sticky="nsew", padx=12, pady=12)

        for col in columns:
            self.table.heading(col, text=col)
            self.table.column(col, anchor="center", width=160)

        # ================= BUTTONS =================
        buttons = TK.Frame(self, bg="#F8FAFC", width=220)
        buttons.grid(row=3, column=1, sticky="ns", padx=(0, 24), pady=10)

        TTK.Button(buttons, text="View Invoice", style="Side.TButton",command=self.view_invoice).grid(sticky="ew", pady=6)

        TTK.Button(buttons, text="Mark Paid", style="Side.TButton",command=self.mark_paid).grid(sticky="ew", pady=6)

        self.refresh()

    # ================= ACTIONS =================

    def view_invoice(self):
        sel = self.table.selection()
        if not sel:
            messagebox.showwarning("No selection", "Please select an invoice.")
            return

        invoice_id = self.table.item(sel[0])["values"][0]
        invoice = self.store.find_invoice(invoice_id)

        win = TK.Toplevel(self)
        win.title(f"Invoice #{invoice.invoice_id}")
        win.geometry("650x500")

        text = TK.Text(win, font=("Courier New", 11))
        text.pack(fill="both", expand=True)
        text.insert("1.0", str(invoice))
        text.configure(state="disabled")

    def mark_paid(self):
        sel = self.table.selection()
        if not sel:
            messagebox.showwarning("No selection", "Please select an invoice.")
            return

        invoice_id = self.table.item(sel[0])["values"][0]
        invoice = self.store.find_invoice(invoice_id)

        if invoice.paid:
            messagebox.showinfo("Already paid", "This invoice is already paid.")
            return

        invoice.mark_as_paid("In-Store")
        self.root.event_generate("<<RefreshAll>>")


    # ================= REFRESH (DYNAMIC SEARCH) =================

    def refresh(self):
        self.table.delete(*self.table.get_children())
        query = self.search_var.get().strip().lower()
        
        
        for inv in self.store.invoices.values():
            status = "PAID" if inv.paid else "UNPAID"

            searchable = f"""
                {inv.invoice_id}
                {inv.order.order_id}
                {inv.customer['name']}
                {status}
            """.lower()

            if query and query not in searchable:
                continue

            self.table.insert(
                "",
                TK.END,
                values=(
                    inv.invoice_id,
                    inv.order.order_id,
                    inv.customer["name"],
                    status,
                    f"${inv.total_due:.2f}",
                    inv.invoice_date.strftime("%d/%m/%Y %H:%M"),
                )
            )
