# SMILES Database Management System 🚘

This project involves the design, implementation, and querying of a relational database for **SMILES**, an imaginary car rental firm.  

It was developed as part of a university assignment to practice database design and analysis, using MySQL Workbench for schema creation and Python for automated data generation.

---

## Features

- **Schema Design:**  
  - Designed a fully normalized (3NF) relational schema with clear entity relationships (outlets, vehicles, clients, staff, rental agreements, fault reports).  
  - Enforced primary and foreign key constraints to guarantee data integrity.

- **Data Management:**  
  - Inserted, modified, and validated large datasets using SQL scripts and automated data loaders built with Python + Faker.

- **Advanced Queries & Views:**  
  - Complex JOINs, GROUP BY, HAVING, EXISTS queries to support business-style questions (e.g., most rented vehicles, top spending clients).
  - Created views for active clients, available vehicles, and high spending clients, simplifying repeated analytics.

- **MySQL Specific Handling:**  
  Addressed limitations like lack of FULL OUTER JOIN by implementing UNION of LEFT and RIGHT JOINs.

---

## Project Structure
```
├── Documentation.pdf # Describes schema & sample query results
├── sql/ # All SQL scripts
│ ├── ex2.sql # Table creation 
│ ├── ex3.sql # Data insertion 
│ ├── ex5.sql # Query execution 
│ ├── ex6.sql # Data modification 
│ └── ex7.sql # View creation 
├── src/
│ └── data_insertion.py # Python script to auto-generate & load data
└── README.md
```

---

## How to Use

1. **Set up the Database:**  
   Open `sql/ex2.sql` in MySQL Workbench and execute to create all tables.

2. **Insert Data:**  
   - Run `sql/ex3.sql` for manual insertion.
   - Or use Python script to auto-generate data:
     ```bash
     python src/data_insertion.py
     ```

3. **Run Queries & Views:**  
   Execute `ex5.sql`, `ex6.sql`, `ex7.sql` to explore advanced queries, perform data updates, and create views for easier reporting.

---

## Tech Stack
- MySQL Workbench for ER design, table creation, and visual schema management.
- Python (Faker, MySQL Connector) for data generation and insertion.
- SQL for complex querying, data manipulation, and business analytics.

---

✅ This project gave me hands-on experience transforming a conceptual car rental process into a robust relational database that not only preserves data integrity but also enables meaningful business-style analysis.

📌 For full ER diagrams, normalization process, and example queries, see `Documentation.pdf`.
