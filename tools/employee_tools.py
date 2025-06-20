# tools/employee_tools.py
from langchain_core.tools import tool
from db.database import add_employee
from datetime import date
from pydantic import BaseModel, Field


class NewEmployeeForm(BaseModel):
    """The form schema for adding a new employee."""

    first_name: str = Field(description="The employee's first name.")
    last_name: str = Field(description="The employee's last name.")
    role: str = Field(
        description="The employee's job role, for example 'Software Engineer' or 'Project Manager'."
    )


@tool(args_schema=NewEmployeeForm)
def add_new_employee_form(first_name: str, last_name: str, role: str) -> str:
    """Use this tool to add a new employee to the database. If a user wants to register or add an employee, present a form with fields for first name, last name, and role. Do not call this until you have all the details of the employee."""
    print(f"Executing add_new_employee_form tool for {first_name} {last_name}...")
    try:
        # The joining date is automatically set to today
        joining_date = date.today()

        employee_uuid = add_employee(
            first_name=first_name,
            last_name=last_name,
            role=role,
            joining_date=joining_date,
        )

        if employee_uuid:
            return (
                f"Successfully added new employee: {first_name} {last_name} (Role: {role}) "
                f"with Employee ID: {employee_uuid}. They are registered as joining on {joining_date.isoformat()}."
            )
        else:
            return "Failed to add the new employee. An employee with this ID might already exist or there was a database error."

    except Exception as e:
        return f"An unexpected error occurred: {e}"
