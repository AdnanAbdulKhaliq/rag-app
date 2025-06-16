# db/database.py
import sqlite3
from sqlite3 import Error
import os
from datetime import date
import uuid

# Define the path for the database file in a 'db' subdirectory
DB_DIR = "db"
DB_FILE = os.path.join(DB_DIR, "employees.sqlite")


def create_connection():
    """Create a database connection to the SQLite database."""
    # Ensure the 'db' directory exists
    os.makedirs(DB_DIR, exist_ok=True)

    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
        # print(f"Successfully connected to SQLite database at '{DB_FILE}'") # Quieter on repeated calls
    except Error as e:
        print(f"Error connecting to database: {e}")
        raise
    return conn


def create_table(conn):
    """Create the employees table if it doesn't exist."""
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id TEXT NOT NULL UNIQUE,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        role TEXT NOT NULL,
        joining_date TEXT NOT NULL
    );
    """
    try:
        cursor = conn.cursor()
        cursor.execute(create_table_sql)
        conn.commit()
        print("Table 'employees' is ready.")
    except Error as e:
        print(f"Error creating table: {e}")
        raise


def initialize_database():
    """Initializes the database and creates the table."""
    conn = create_connection()
    if conn:
        create_table(conn)
        conn.close()


# --- CRUD Operations ---


def add_employee(first_name: str, last_name: str, role: str, joining_date: date):
    """
    Add a new employee to the employees table with a generated UUID.

    Args:
        first_name (str): The employee's first name.
        last_name (str): The employee's last name.
        role (str): The employee's job role.
        joining_date (date): The employee's start date.

    Returns:
        str: The UUID of the newly created employee, or None on failure.
    """
    conn = create_connection()
    sql = """ INSERT INTO employees(employee_id, first_name, last_name, role, joining_date)
              VALUES(?,?,?,?,?) """

    employee_id = str(uuid.uuid4())

    try:
        cursor = conn.cursor()
        cursor.execute(
            sql, (employee_id, first_name, last_name, role, str(joining_date))
        )
        conn.commit()
        print(
            f"Successfully added employee {first_name} {last_name} with ID: {employee_id}"
        )
        return employee_id
    except Error as e:
        print(f"Error adding employee: {e}")
        return None
    finally:
        if conn:
            conn.close()


def get_employee_by_id(employee_id: str):
    """
    Query an employee by their employee_id (UUID).

    Args:
        employee_id (str): The UUID of the employee to find.

    Returns:
        dict: A dictionary containing the employee's data or None if not found.
    """
    conn = create_connection()
    try:
        conn.row_factory = sqlite3.Row  # This allows accessing columns by name
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM employees WHERE employee_id=?", (employee_id,))
        row = cursor.fetchone()
        if row:
            return dict(row)
        return None
    except Error as e:
        print(f"Error fetching employee: {e}")
        return None
    finally:
        if conn:
            conn.close()


def get_all_employees():
    """
    Query all employees from the table.

    Returns:
        list: A list of dictionaries, where each dictionary is an employee.
    """
    conn = create_connection()
    try:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM employees")
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    except Error as e:
        print(f"Error fetching all employees: {e}")
        return []
    finally:
        if conn:
            conn.close()


def update_employee_role(employee_id: str, new_role: str):
    """
    Update an employee's role.

    Args:
        employee_id (str): The UUID of the employee to update.
        new_role (str): The new role to assign.

    Returns:
        bool: True if update was successful, False otherwise.
    """
    conn = create_connection()
    sql = """ UPDATE employees
              SET role = ?
              WHERE employee_id = ?"""
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (new_role, employee_id))
        conn.commit()
        if cursor.rowcount == 0:
            print(f"No employee found with ID '{employee_id}'.")
            return False
        print(f"Successfully updated role for employee ID '{employee_id}'.")
        return True
    except Error as e:
        print(f"Error updating employee: {e}")
        return False
    finally:
        if conn:
            conn.close()


def delete_employee(employee_id: str):
    """
    Delete an employee by their employee_id.

    Args:
        employee_id (str): The UUID of the employee to delete.

    Returns:
        bool: True if deletion was successful, False otherwise.
    """
    conn = create_connection()
    sql = "DELETE FROM employees WHERE employee_id = ?"
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (employee_id,))
        conn.commit()
        if cursor.rowcount == 0:
            print(f"No employee found with ID '{employee_id}'.")
            return False
        print(f"Successfully deleted employee ID '{employee_id}'.")
        return True
    except Error as e:
        print(f"Error deleting employee: {e}")
        return False
    finally:
        if conn:
            conn.close()


# --- Main execution block for testing ---
if __name__ == "__main__":
    print("Running database script for setup and testing...")

    # 1. Initialize DB and Table
    initialize_database()

    # 2. Add some sample employees (Create)
    print("\n--- Testing ADD ---")
    john_id = add_employee("John", "Doe", "Software Engineer", date(2024, 6, 15))
    jane_id = add_employee("Jane", "Smith", "Project Manager", date(2023, 1, 20))

    # 3. Retrieve all employees (Read)
    print("\n--- Testing GET ALL ---")
    all_employees = get_all_employees()
    print(f"Found {len(all_employees)} employees:")
    for emp in all_employees:
        print(emp)

    # 4. Retrieve a single employee (Read)
    print("\n--- Testing GET BY ID ---")
    if john_id:
        employee = get_employee_by_id(john_id)
        if employee:
            print(f"Found employee {john_id}:", employee)
        else:
            print(f"Employee {john_id} not found.")

    # 5. Update an employee's role (Update)
    print("\n--- Testing UPDATE ---")
    if john_id:
        update_employee_role(john_id, "Senior Software Engineer")
        employee = get_employee_by_id(john_id)
        print(f"Employee {john_id} after update:", employee)

    # 6. Delete an employee (Delete)
    print("\n--- Testing DELETE ---")
    if jane_id:
        delete_employee(jane_id)
        employees_after_delete = get_all_employees()
        print(f"Employees remaining: {len(employees_after_delete)}")
        for emp in employees_after_delete:
            print(emp)

    print("\nDatabase script execution finished.")
