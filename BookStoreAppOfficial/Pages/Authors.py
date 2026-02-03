import tkinter as TK
from tkinter import ttk as TTK, messagebox


class Authors(TK.Frame):

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

        TK.Label(header,text="Authors",font=("Arial", 20, "bold"),bg="#F8FAFC",fg="#0F172A").grid(row=0, column=0, sticky="w")

        TK.Label(header,text="Manage author information, biographies, and associated publications.",font=("Arial", 12),bg="#F8FAFC",fg="#0F172A").grid(row=1, column=0, sticky="w")

   
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

        columns = ("Author ID", "First Name", "Last Name", "Email", "Phone", "Date Created")

        self.table = TTK.Treeview(table_container, columns=columns, show="headings", height=25,style="Borderless.Treeview")
        self.table.grid(row=0, column=0, sticky="nsew", padx=12, pady=12)

        for col in columns:
            self.table.heading(col, text=col)
            self.table.column(col, anchor="center", width=160)

        buttons = TK.Frame(self, bg="#F8FAFC", width=220)
        buttons.grid(row=3, column=1, sticky="ns", padx=(0, 24), pady=10)

        TTK.Button(buttons, text="Add Author", style="Side.TButton", command=self.add_author).grid(sticky="ew", pady=6)

        TTK.Button(buttons,text="Edit Author",style="Side.TButton",command=self.edit_author).grid(sticky="ew", pady=6)

        TTK.Button(buttons,text="Delete Author",style="Side.TButton",command=self.delete_author).grid(sticky="ew", pady=6)

        self.refresh()

    def add_author(self):
        self._open_form("Add Author")

    def edit_author(self):
        sel = self.table.selection()
        if not sel:
            messagebox.showwarning("No selection", "Please select an author.")
            return

        values = self.table.item(sel[0])["values"]
        self._open_form("Edit Author", values)

    def _open_form(self, title, values=None):
        form = TK.Toplevel(self, bg="#F8FAFC")
        form.title(title)
        form.geometry("400x360")
        form.grab_set()

        fields = ["First Name", "Last Name", "Email", "Phone"]
        entries = {}

        for i, field in enumerate(fields):
            TK.Label(form, text=field, bg="#F8FAFC")\
                .pack(anchor="w", padx=24, pady=(12, 0))

            e = TK.Entry(form)
            if values:
                e.insert(0, values[i + 1])
            e.pack(fill="x", padx=24)
            entries[field] = e

        save_btn = TK.Button(form,text="Save",bg="#111827",fg="white",state="disabled")
        save_btn.pack(pady=20)

        def validate():
            save_btn.config(state="normal" if all(e.get().strip() for e in entries.values())else "disabled")

        for e in entries.values():
            e.bind("<KeyRelease>", lambda *_: validate())

        def save():
            try:
                if values:
                    aid = values[0]
                    self.store.edit_author(
                        aid,
                        entries["First Name"].get(),
                        entries["Last Name"].get(),
                        entries["Email"].get(),
                        entries["Phone"].get(),
                    )
                else:
                    self.store.add_author(
                        entries["First Name"].get(),
                        entries["Last Name"].get(),
                        entries["Email"].get(),
                        entries["Phone"].get(),
                    )

                self.root.event_generate("<<RefreshAll>>")
                form.destroy()

            except Exception as e:
                messagebox.showerror("Error", str(e))

        save_btn.config(command=save)
        validate()

    def delete_author(self):
        sel = self.table.selection()
        if not sel:
            return

        aid = self.table.item(sel[0])["values"][0]

        try:
            self.store.delete_author(aid)
            self.root.event_generate("<<RefreshAll>>")
        except Exception as e:
            messagebox.showerror("Error", str(e))


    def refresh(self):
        self.table.delete(*self.table.get_children())
        query = self.search_var.get().strip().lower()

        for a in self.store.authors.values():
            text = f"{a.first_name} {a.last_name} {a.email_address} {a.phone_number}".lower()

            if query and query not in text:
                continue

            self.table.insert(
                "",
                TK.END,
                values=(
                    a.author_id,
                    a.first_name,
                    a.last_name,
                    a.email_address,
                    a.phone_number,
                    a.date_created.strftime("%d/%m/%Y %H:%M"),
                )
            )
