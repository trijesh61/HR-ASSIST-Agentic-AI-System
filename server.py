from fastmcp import FastMCP
from typing import  Dict, List

from HRMS import *
'''from HRMS.employee_manager import EmployeeManager
from HRMS.leave_manager import LeaveManager
from HRMS.meeting_manager import MeetingManager
from HRMS.schemas import EmployeeCreate
from HRMS.ticket_manager import TicketManager'''

from utils import seed_services

employee_manager = EmployeeManager()
leave_manager = LeaveManager()
ticket_manager = TicketManager()
meeting_manager = MeetingManager()

seed_services(employee_manager, leave_manager, meeting_manager, ticket_manager)

mcp = FastMCP("HR-ASSIST-Agentic-AI-System")

#tools
@mcp.tool()
def add_employee( emp_name: str, manager_id : str, email : str) -> str :
    """
    Add a new Employee to HRMS System.
    :param emp_name: Employee Name
    :param manager_id: Employee Manager ID (Optional)
    :param email: Employee Email
    :return: Confirmation message
    """
    emp = EmployeeCreate(
        emp_id= employee_manager.get_next_emp_id(),
        name=emp_name,
        manager_id=manager_id ,
        email=email)
    employee_manager.add_employee(emp)
    return f"Employee {emp_name} added Successfully"


@mcp.tool()
def get_employee_details(name: str) -> Dict[str, str]:
    """
    Get employee details by name.
    :param name: Name of the employee
    :return: Employee ID and manager ID
    """
    matches = employee_manager.search_employee_by_name(name)

    if len(matches) == 0:
        raise ValueError(f"No employees found with name {name}.")

    emp_id = matches[0]
    emp_details = employee_manager.get_employee_details(emp_id)
    return emp_details




if __name__ == '__main__':
    mcp.run(transport="stdio")