import tkinter as TK
from tkinter import ttk as TTK, messagebox


class Books(TK.Frame):

    def __init__(self, parent, store):
        super().__init__(parent, bg="#F8FAFC")
        self.store = store
        self.root = self.winfo_toplevel()
        
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)
        self.rowconfigure(3, weight=1)

        header = TK.Frame(self, bg="#F8FAFC")
        header.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        header.columnconfigure(0, weight=1)

        TK.Label(header, text="Books", font=("Arial", 20, "bold"), bg="#F8FAFC",fg="#0F172A").grid(row=0, column=0, sticky="w")

        TK.Label(header,text="Browse, add, and update book records, pricing, and availability.", font=("Arial", 12), bg="#F8FAFC",fg="#0F172A").grid(row=1, column=0, sticky="w")

        search_frame = TK.Frame(self, bg="#F8FAFC")
        search_frame.grid(row=1, column=0, sticky="ew", padx=24, pady=(0, 10))
        search_frame.columnconfigure(1, weight=1)

        TK.Label(search_frame, text="Search:", bg="#F8FAFC").grid(row=0, column=0, sticky="w")

        self.search_var = TK.StringVar()
        self.search_var.trace_add("write", lambda *_: self.refresh())

        TK.Entry(search_frame, textvariable=self.search_var).grid(row=0, column=1, sticky="ew", padx=(8, 0))

        table_container = TK.Frame(self, bg="#F8FAFC")
        table_container.grid(row=3, column=0, sticky="nsew", padx=(24, 10), pady=10)
        table_container.rowconfigure(0, weight=1)
        table_container.columnconfigure(0, weight=1)

        columns = ("Book ID", "Title", "Author", "Price", "Quantity", "Date Created")

        self.table = TTK.Treeview(table_container, columns=columns, show="headings", height=25, style="Borderless.Treeview")
        self.table.grid(row=0, column=0, sticky="nsew", padx=12, pady=12)

        for col in columns:
            self.table.heading(col, text=col)
            self.table.column(col, anchor="center", width=160)

        buttons = TK.Frame(self, bg="#F8FAFC", width=220)
        buttons.grid(row=3, column=1, sticky="ns", padx=(0, 24), pady=10)

        TTK.Button(buttons,text="Add Book",style="Side.TButton",command=self.add_book).grid(sticky="ew", pady=6)

        TTK.Button(buttons,text="Edit Book",style="Side.TButton",command=self.edit_book).grid(sticky="ew", pady=6)

        TTK.Button(buttons,text="Delete Book",style="Side.TButton",command=self.delete_book).grid(sticky="ew", pady=6)

        self.refresh()

    def add_book(self):
        if not self.store.authors:
            messagebox.showwarning(
                "No authors",
                "You must add an author before adding a book."
            )
            return
        self._open_form("Add Book")

    def edit_book(self):
        sel = self.table.selection()
        if not sel:
            messagebox.showwarning("No selection", "Please select a book.")
            return

        values = self.table.item(sel[0])["values"]
        self._open_form("Edit Book", values)

    def _open_form(self, title, values=None):
        form = TK.Toplevel(self, bg="#F8FAFC")
        form.title(title)
        form.geometry("420x420")
        form.grab_set()

        fields = ["Title", "Price", "Quantity"]
        entries = {}

        # ----- TITLE -----
        TK.Label(form, text="Title", bg="#F8FAFC").pack(anchor="w", padx=24, pady=(12, 0))
        title_entry = TK.Entry(form)
        title_entry.pack(fill="x", padx=24)
        entries["Title"] = title_entry

        # ----- AUTHOR -----
        TK.Label(form, text="Author", bg="#F8FAFC").pack(anchor="w", padx=24, pady=(12, 0))
        author_var = TK.StringVar()

        authors = {
            f"{a.first_name} {a.last_name}": a.author_id
            for a in self.store.authors.values()
        }

        author_box = TTK.Combobox(
            form,
            textvariable=author_var,
            values=list(authors.keys()),
            state="readonly"
        )
        author_box.pack(fill="x", padx=24)

        # ----- PRICE -----
        TK.Label(form, text="Price", bg="#F8FAFC").pack(anchor="w", padx=24, pady=(12, 0))
        price_entry = TK.Entry(form)
        price_entry.pack(fill="x", padx=24)
        entries["Price"] = price_entry

        # ----- QUANTITY -----
        TK.Label(form, text="Quantity", bg="#F8FAFC").pack(anchor="w", padx=24, pady=(12, 0))
        qty_entry = TK.Entry(form)
        qty_entry.pack(fill="x", padx=24)
        entries["Quantity"] = qty_entry

        # ----- PRE-FILL (EDIT) -----
        if values:
            book_id, title, author, price, qty, _ = values
            title_entry.insert(0, title)
            author_var.set(author)
            price_entry.insert(0, price)
            qty_entry.insert(0, qty)

        save_btn = TK.Button(
            form,
            text="Save",
            bg="#111827",
            fg="white",
            state="disabled"
        )
        save_btn.pack(pady=20)

        def validate():
            try:
                valid = (
                    title_entry.get().strip() and
                    author_var.get() and
                    float(price_entry.get()) >= 0 and
                    int(qty_entry.get()) >= 0
                )
            except ValueError:
                valid = False

            save_btn.config(state="normal" if valid else "disabled")

        for w in (title_entry, price_entry, qty_entry):
            w.bind("<KeyRelease>", lambda *_: validate())
        author_box.bind("<<ComboboxSelected>>", lambda *_: validate())

        def save():
            try:
                if values:
                    book = self.store.books[book_id]
                    book.title = title_entry.get()
                    book.author = author_var.get()
                    book.price = float(price_entry.get())
                    book.quantity = int(qty_entry.get())
                else:
                    self.store.add_book(
                        title_entry.get(),
                        authors[author_var.get()],
                        float(price_entry.get()),
                        int(qty_entry.get())
                    )

                self.root.event_generate("<<RefreshAll>>")
                form.destroy()

            except Exception as e:
                messagebox.showerror("Error", str(e))

        save_btn.config(command=save)
        validate()

    # ================= DELETE =================

    def delete_book(self):
        sel = self.table.selection()
        if not sel:
            return

        book_id = self.table.item(sel[0])["values"][0]
        self.store.delete_book(book_id)
        self.root.event_generate("<<RefreshAll>>")


    # ================= REFRESH (DYNAMIC SEARCH) =================

    def refresh(self):
        self.table.delete(*self.table.get_children())
        query = self.search_var.get().strip().lower()

        for b in self.store.books.values():
            text = f"{b.title} {b.author}".lower()

            if query and query not in text:
                continue

            self.table.insert(
                "",
                TK.END,
                values=(
                    b.book_id,
                    b.title,
                    b.author,
                    f"{b.price:.2f}",
                    b.quantity,
                    b.date_created.strftime("%d/%m/%Y %H:%M"),
                )
            )
