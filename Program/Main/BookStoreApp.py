import tkinter as TK
from tkinter import ttk as TTK
from Main.BookStoreCore import Store
from Pages.Dashboard import Dashboard
from Pages.Customers import Customers
from Pages.Authors import Authors
from Pages.Books import Books
from Pages.Orders import Orders
from Pages.Invoices import Invoices

class RMSApp(TK.Tk):
    def __init__(self):
        super().__init__()
        # Configuration / Applying Settings
        self.title("Bookstore App")
        self.root = self.winfo_toplevel()
        self.geometry("1380x720")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.configure(bg="#F8FAFC")
        self.store = Store()

        self.root.bind("<<RefreshAll>>", self._refresh_all)


        # Tree View & Button Styles
        style = TTK.Style()
        style.theme_use("default")
        style.layout("Borderless.Treeview", [("Treeview.treearea", {"sticky": "nswe"})])
        style.configure("Borderless.Treeview", background="#FFFFFF", fieldbackground="#FFFFFF", borderwidth=0, relief="flat")
        style.configure("Borderless.Treeview.Heading", background="#111827", foreground="#FFFFFF", font=("Segoe UI", 10, "bold"))
        style.configure("Side.TButton", background="#111827", foreground="#FFFFFF", font=("Segoe UI", 10, "bold"), padding=8)
        style.map("Borderless.Treeview.Heading",background=[("active", "#1D4ED8"),("pressed", "#1E40AF") ])

        style.map("Side.TButton", background=[("active", "#1D4ED8"), ("pressed", "#1E40AF")])

        self.navigation_bar = TK.Frame(self, bg="#111827")
        self.navigation_bar.grid(row=0, column=0, sticky='ns')

        self.content_page = TK.Frame(self, bg="#F8FAFC")
        self.content_page.grid(row=0, column=1, sticky='nsew')

        title_label = TK.Label(self.navigation_bar, text="BookStore", fg="#E5E7EB", bg="#111827",font=("Segoe UI", 12, "bold"))
        title_label.grid(pady=0, padx=0, sticky="w")


        TK.Frame(self.navigation_bar, bg="#FFFFFF", height=1 ).grid(row=1, column=0, sticky="ew", padx=25)

        self.frames = {}

        for Page in (Dashboard, Customers, Authors, Books, Orders, Invoices):
            frame = Page(self.content_page, self.store)
            self.frames[Page.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            self.root.bind(f"<<{Page.__name__}>>", frame.refresh)
            self.make_nav(Page.__name__)
            frame.refresh()


        self.show("Dashboard")

    def make_nav(self, page_name):
        TK.Button(
            self.navigation_bar,
            text=page_name.replace("Page", ""),
            fg="white",
            bg="#111827",
            relief="flat",
            command=lambda: self.show(page_name)
         ).grid(sticky="ew", padx=10, pady=2)


    def show(self, page_name):
        self.frames[page_name].tkraise()

    def _refresh_all(self, event=None):
        for frame in self.frames.values():
            frame.refresh()




if __name__ == "__main__":
    print("[BookStoreApp]: Can not start program , Please Open Application.py")
