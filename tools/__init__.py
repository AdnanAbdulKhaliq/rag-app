# tools/__init__.py
from .retriever_tool import retriever_tool
from .employee_tools import add_new_employee_form

# This list is what the agent will use.
# Just add your new tools to this list to make them available to the agent.
all_tools = [retriever_tool, add_new_employee_form]
