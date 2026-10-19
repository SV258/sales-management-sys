# Sales Management System

## Project Overview
This Sales Management System is developed using Python, Streamlit, and MySQL. It helps manage customer sales, products, branches, payments, and sales reports.

## Technologies Used
- Python
- Streamlit
- MySQL
- MySQL Workbench
- Pandas
- GitHub

## Features
- User login authentication
- Super Admin dashboard
- Customer Sales Report
- Branch-wise sales filtering
- Product-wise sales filtering
- Date range filtering
- New sales entry
- Payment entry
- Automatic received amount update using MySQL trigger
- SQL queries for sales analysis

## Database
Database Name: sales_management_sys

Main Tables:
- branches
- customer_sales
- payment_splits
- users

## How to Run the Project
1. Install Python and MySQL.
2. Install required Python packages.
3. Configure the MySQL database connection.
4. Open the project folder in the terminal.
5. Run the command:

```bash
streamlit run newapp.py
```

6. Open the Streamlit application in your browser.

## Security
Database passwords and Streamlit secrets are not included in this repository.

## Project Purpose
This project demonstrates Python, SQL, database connectivity, dashboard development, sales reporting, and payment automation skills.

## Author
Suganthi Veeraraju

## Project Type
Data Analytics and Sales Management System

## User Roles and Access Control

The Sales Management System supports role-based access for different users.

### Super Admin
- View sales records across all branches.
- Access sales reports and financial summaries.
- Filter records by branch, product and date range.
- Access sales and payment entry functionality.
- Use the Advanced SQL Engine for reporting and analysis.

### Branch Admin
- Log in using assigned credentials.
- View customer sales records for their assigned branch.
- Access branch-specific reporting information.

## Sales and Payment Management

The application supports recording customer sales and payments using Streamlit forms connected to a MySQL database.

MySQL triggers help update received payment amounts when new payment records are inserted.

## Financial Reporting and Filters

The reporting interface includes:

- Branch Name filter
- Product Name filter
- Start Date filter
- End Date filter
- Financial summaries based on the selected filters
- Customer sales reports

## Advanced SQL Engine

The Advanced SQL Engine provides an interface for selecting saved SQL queries and executing supported read-only queries.

This feature helps users explore sales data, analyse business performance and practise SQL reporting.

## Project File Structure

| File | Purpose |
|---|---|
| `newapp.py` | Main Streamlit application, login and dashboards |
| `sql_connection.py` | MySQL database connection |
| `sql_engine.py` | Advanced SQL Engine functionality |
| `sales_management_queries.sql` | SQL queries used in the project |
| `README.md` | Project documentation |
| `.gitignore` | Excludes local configuration and sensitive files from Git |

## Security Practices

- Database credentials are stored locally using Streamlit secrets.
- The secrets file is excluded from Git using `.gitignore`.
- Password verification uses hashing rather than plain-text comparison.
- Branch-specific reports restrict the data shown to branch administrators.

**Note:** This project is a learning and portfolio application. Further security review and testing are recommended before production deployment.

## Future Improvements

- Add automated application tests.
- Improve error handling and input validation.
- Add data export options where required.
- Enhance dashboard visualisations.
- Prepare deployment documentation.

## Project Purpose

This project demonstrates practical skills in Python programming, MySQL database management, SQL reporting, Streamlit application development, role-based access control and Git version control.