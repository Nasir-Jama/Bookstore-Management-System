# Bookstore-Management-System
Python Bookstore Management System (University of Northampton – CSY1020)

## Overview
This project is a **Bookstore Management System** developed in **Python** as part of the  
**University of Northampton – Computer Science** module:

**CSY1020: Problem Solving & Programming**

The application replaces a paper-based bookstore workflow with a **desktop-based graphical system** built using **Tkinter**, following **object-oriented design principles** and an **MVC-style architecture**.

---

## Key Features
- Customer management (add, edit, remove)
- Author management
- Book inventory & stock control
- Order creation with validation
- Automatic invoice generation
- Shipping & urgent shipping options
- Dashboard with live statistics
- Search functionality across records
- Error handling & input validation

---

## Architecture
The system follows a **Model–View–Controller (MVC)-style design**:

- **Model**  
  `BookStoreCore.py`  
  Centralised business logic handled by the `Store` class

- **View**  
  Tkinter-based GUI pages located in the `Pages/` directory

- **Controller**  
  `BookStoreApp.py` manages navigation and interaction between UI and core logic

The application entry point is:
