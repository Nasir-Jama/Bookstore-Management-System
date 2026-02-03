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

- Application.py



## Technologies Used
- Python 3
- Tkinter (GUI)
- Object-Oriented Programming (OOP)
- MVC-style architectural pattern

---

## How to Run
1. Ensure Python 3 is installed
2. Clone or download the repository
3. Run the application:
```bash
python Application.py


Academic Context

This project was developed for:

University of Northampton

BSc Computer Science

Module: CSY1020 – Problem Solving & Programming

It demonstrates:

Encapsulation, inheritance, abstraction, and polymorphism

Separation of business logic from presentation logic

Maintainable and scalable application structure

Documentation & Demo

Full project report included in this repository

Video demonstration:

https://www.youtube.com/watch?v=VjZdsMqxRd4

Author

Abdinasir Jama
Computer Science Student
University of Northampton
