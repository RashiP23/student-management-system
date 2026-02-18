# Student Management System (Python + Oracle SQL)

This project is a basic **Student Management System** developed using **Python** and **Oracle Database (SQL*Plus)**.  
It demonstrates how Python applications can interact with an Oracle database to perform CRUD operations.

---

## 📌 Features
- Add new student records
- View all students
- Update student marks
- Delete student records

---

## 🛠 Technologies Used
- Python 3
- Oracle Database Express Edition (XE)
- SQL*Plus
- cx_Oracle (Python–Oracle connector)

---

## 📁 Project Structure

STUDENT-MANAGEMENT-SYSTEM  
├── python/  
│   ├── main.py  
│   └── db_config.py  
│  
├── sql/  
│   ├── create_tables.sql  
│   ├── insert_data.sql  
│   └── queries.sql  
│  
├── README.md  
└── requirements.txt  

---

## ▶️ How to Run the Project

1. Install **Oracle Database Express Edition**
2. Open **SQL*Plus** and run:
   - `create_tables.sql`
   - `insert_data.sql` (optional)
3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
