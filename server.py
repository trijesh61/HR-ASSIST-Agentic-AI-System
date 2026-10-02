from fastmcp import FastMCP
from typing import  Dict, List
import os

from HRMS import *
from emails import EmailSender
from utils import seed_services

from dotenv import load_dotenv
_ = load_dotenv()

email_sender = EmailSender(
        smtp_server="smtp.gmail.com",
        port=587,
        username=os.getenv("CB_EMAIL"),
        password=os.getenv("CB_EMAIL_PWD"),
        use_tls=True
    )


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

@mcp.tool()
def send_email(subject: str, body: str, to_emails: list[str]) -> str:
    """
    Send an email.

    :param subject: Subject of the email
    :param body: Body of the email
    :param to_emails: List of emails of employees

        """
    email_sender.send_email(
        subject=subject,
        body=body,
        to_emails=to_emails,
        from_email= email_sender.username,)
    return f"Email successfully sent!"

@mcp.tool()
def create_ticket(emp_id: str, item: str, reason:str) -> str:
    """
    Create a ticket for buying required items for an employee.
    :param emp_id: Employee ID
    :param item: Item requested (Laptop, ID Card, etc.)
    :param reason: Reason for the request
    :return: Confirmation message
    """
    ticket_req = TicketCreate(emp_id=emp_id, item=item, reason=reason)
    return ticket_manager.create_ticket(ticket_req)



@mcp.tool()
def update_ticket_status(ticket_id: str, status: str) -> str:
    """
    Update the status of a ticket.
    :param ticket_id: Ticket ID
    :param status: New status of the ticket
    :return: Confirmation message
    """
    ticket_status_update = TicketStatusUpdate(status=status)
    return ticket_manager.update_ticket_status(ticket_status_update, ticket_id)

@mcp.tool()
def list_tickets(employee_id: str, status: str) -> list[dict[str, str]]:
    """
    List tickets for an employee with optional status filter.
    :param employee_id: Employee ID
    :param status: Ticket status (optional)
    :return: List of tickets
    """
    return ticket_manager.list_tickets(employee_id=employee_id, status=status)

@mcp.tool()
def schedule_meeting(emp_id:str, meeting_time: datetime, topic:str) -> str:
    """
    Schedule a meeting.
    :param emp_id: Employee ID
    :param meeting_time: Meeting time
    :param topic: Meeting topic
    :return: Confirmation message

    """
    meeting_req = MeetingCreate(
        emp_id=emp_id,
        topic=topic,
        meeting_dt=meeting_time)
    return meeting_manager.schedule_meeting(meeting_req)


@mcp.tool()
def get_meetings(emp_id: str) -> list[dict[str, str]]:
    """
    Get meetings for an employee.
    :param emp_id: Employee ID
    :return: List of meetings

    """
    return meeting_manager.get_meetings(emp_id)

@mcp.tool()
def cancel_meeting(emp_id : str, meeting_dt : datetime, topic: str) -> str:
    """
    Cancel a meeting.

    :param emp_id: Employee ID
    :param meeting_dt: Meeting time
    :param topic: Meeting topic
    :return: Confirmation message

       """
    req = MeetingCancelRequest(
        emp_id=emp_id,
        meeting_dt=meeting_dt,
        topic=topic
    )
    return meeting_manager.cancel_meeting(req)

@mcp.tool()
def get_employee_leave_balance(emp_id:str)->str:
    """
    Get employee leave balance.
    :param emp_id: Employee ID
    :return: Employee leave balance

    """
    return leave_manager.get_leave_balance(emp_id)

@mcp.tool()
def apply_leave(emp_id: str, leave_dates:List[date]) -> str:
    """
    Apply leave for an employee.
    :param emp_id: Employee ID

    :param leave_dates: List of dates
    :return: Confirmation message
    """
    req = LeaveApplyRequest(emp_id=emp_id, leave_dates=leave_dates)
    return leave_manager.apply_leave(req)

@mcp.tool()
def get_leave_history(emp_id:str) -> str:
    """
    Get leave history for an employee.
    :param emp_id: Employee ID
    :return: Confirmation message
    """
    return leave_manager.get_leave_history(emp_id)

@mcp.prompt("onboard_new_employee")
def onboard_new_employee(employee_name: str, manager_name: str):
    return f"""Onboard a new employee with the following details:
    - Name: {employee_name}
    - Manager Name: {manager_name}
    Steps to follow:
    - Add the employee to the HRMS system.
    - Send a welcome email to the employee with their login credentials. (Format: employee_name@atliq.com)
    - Notify the manager about the new employee's onboarding.
    - Raise tickets for a new laptop, id card, and other necessary equipment.
    - Schedule an introductory meeting between the employee and the manager.
    """



if __name__ == '__main__':
    mcp.run(transport="stdio")