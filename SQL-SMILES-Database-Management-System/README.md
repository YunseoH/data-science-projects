# SMILES Database Management System 🚘

This project involves the **design, implementation, and querying of a relational database** named **SMILES**, built using **MySQL Workbench** and supplemented by Python for data generation.

---

## Features
- **Schema Design:** Created relational tables with appropriate constraints and indexes to efficiently store chemical data.
- **Data Management:** Inserted, modified, and validated large datasets using SQL scripts and Python loaders.
- **Advanced Queries & Views:** 
  - Developed complex SQL queries to extract insights.
  - Created views to simplify repeated analyses.
- **MySQL Specifics:** Handled data type nuances and SQL dialect limitations inherent to MySQL.

---

## 📁 Project Structure
```
├── Documentation.pdf # Describes schema & sample query results
├── sql/ # All SQL scripts
│ ├── ex2.sql # Table creation (Exercise 2)
│ ├── ex3.sql # Data insertion (Exercise 3)
│ ├── ex5.sql # Query execution (Exercise 5)
│ ├── ex6.sql # Data modification (Exercise 6)
│ └── ex7.sql # View creation (Exercise 7)
├── src/
│ └── data_insertion.py # Python script to auto-generate & load data
└── README.md
```

---

## How to Use

### 1. Set up the Database
- Open `sql/ex2.sql` in **MySQL Workbench** and execute to create tables.

### 2. Insert Data
- Run `sql/ex3.sql` to populate tables with initial data.
- Or, execute the Python script to generate and insert randomized data:
```
python src/data_insertion.py
```
### 3.  Run Queries & Views
- Use `ex5.sql`, `ex6.sql`, and `ex7.sql` to:
- Extract meaningful subsets of data.
- Modify existing records.
- Create database views for easier reporting.

## Documentation
Detailed schema diagrams, ER diagrams, and example query outputs are included in `Documentation.pdf`.

## Tech Stack
- MySQL Workbench for database design & visualization.
- Python (MySQL Connector / pymysql) for data generation & insertion.
- SQL for complex querying, data manipulation, and view creation.
