<div align="center">

# 🤖 HR-ASSIST: Agentic AI System

**Automate HR workflows, starting with employee onboarding, through an MCP server and Claude Desktop.**

![Python](https://img.shields.io/badge/Python-3.12+-blue?logo=python&logoColor=white)
![FastMCP](https://img.shields.io/badge/FastMCP-MCP%20Server-purple)
![Claude Desktop](https://img.shields.io/badge/Client-Claude%20Desktop-orange)
![uv](https://img.shields.io/badge/Package%20Manager-uv-green)

</div>

---

## 📌 Overview

HR-ASSIST is an **agentic AI system** that helps HR teams automate routine, manual workflows. The flagship demo is **employee onboarding**: a single request makes the agent add the employee, email them, notify the manager, raise equipment tickets and schedule an intro meeting.

**How it works**

- **MCP client:** Claude Desktop (the agent that reasons and decides which tools to call)
- **MCP server:** this repository (exposes HR tools and prompts built with FastMCP)

```
┌────────────────────┐   MCP over stdio   ┌────────────────────────────┐
│   Claude Desktop   │ ◄────────────────► │  server.py (FastMCP)       │
│   (MCP client)     │                    │  tools + onboarding prompt │
└────────────────────┘                    └─────────────┬──────────────┘
                                                        │
              ┌────────────────┬────────────────┬───────┴────────┐
              ▼                ▼                ▼                ▼
       EmployeeManager   LeaveManager    TicketManager    MeetingManager
                         (HRMS package)                         │
                                                                ▼
                                                     EmailSender (emails.py)
```

---

## ✨ Features

| Area | What the agent can do |
|------|-----------------------|
| 👤 **Employees** | Add new employees, look up details by name |
| 🏖️ **Leave** | Check balance, apply for leave dates, view history |
| 🎫 **Tickets** | Raise equipment requests (laptop, ID card, etc.), update status, list by employee and status |
| 📅 **Meetings** | Schedule, list and cancel meetings |
| ✉️ **Email** | Send emails to one or many employees via SMTP |
| 🧭 **Workflow prompt** | One-click `onboard_new_employee` flow |

---

## 🧰 Tools and Prompts

<details>
<summary><b>Click to view all MCP tools</b></summary>

| Tool | Description |
|------|-------------|
| `add_employee(emp_name, manager_id, email)` | Add a new employee to the HRMS |
| `get_employee_details(name)` | Get employee ID and manager ID by name |
| `get_employee_leave_balance(emp_id)` | Remaining leave balance |
| `apply_leave(emp_id, leave_dates)` | Apply leave for a list of dates |
| `get_leave_history(emp_id)` | Past leave records |
| `create_ticket(emp_id, item, reason)` | Raise a ticket for an item |
| `update_ticket_status(ticket_id, status)` | Update a ticket's status |
| `list_tickets(employee_id, status)` | List tickets with status filter |
| `schedule_meeting(emp_id, meeting_time, topic)` | Schedule a meeting |
| `get_meetings(emp_id)` | List an employee's meetings |
| `cancel_meeting(emp_id, meeting_dt, topic)` | Cancel a meeting |
| `send_email(subject, body, to_emails)` | Send an email |

</details>

### Onboarding prompt: `onboard_new_employee(employee_name, manager_name)`

When triggered, the agent will:

1. Add the employee to the HRMS system
2. Send a welcome email with login details
3. Notify the manager about the new joiner
4. Raise tickets for a laptop, ID card and other equipment
5. Schedule an introductory meeting between the employee and manager

---

## 📁 Project Structure

```
HR-ASSIST-Agentic-AI-System/
├── HRMS/              # Employee, Leave, Ticket and Meeting managers + models
├── resources/         # Screenshots used in this README
├── server.py          # FastMCP server: tools and prompt definitions
├── emails.py          # SMTP email helper (EmailSender)
├── utils.py           # Seeds sample data on startup
├── main.py            # Entry-point stub
├── pyproject.toml     # Project metadata and dependencies
├── uv.lock            # Locked dependencies
└── .python-version    # Python version pin
```

---

## 🛠️ Setup Instructions

### Prerequisites

- Python **3.12+**
- [uv](https://docs.astral.sh/uv/) package manager
- [Claude Desktop](https://claude.ai/download)
- An email account with an **app-specific password** (e.g., a Gmail App Password)

### 1. Clone and install

```bash
git clone https://github.com/trijesh61/HR-ASSIST-Agentic-AI-System.git
cd HR-ASSIST-Agentic-AI-System
uv sync
```

Starting from scratch instead? Run `uv init` and then `uv add "mcp[cli]" fastmcp python-dotenv`.

### 2. Configure Claude Desktop

Open `claude_desktop_config.json` and add:

```json
{
  "mcpServers": {
    "hr-assist": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/HR-ASSIST-Agentic-AI-System",
        "run",
        "server.py"
      ],
      "env": {
        "CB_EMAIL": "YOUR_EMAIL",
        "CB_EMAIL_PWD": "YOUR_APP_PASSWORD"
      }
    }
  }
}
```

<details>
<summary><b>Windows example</b></summary>

```json
{
  "mcpServers": {
    "hr-assist": {
      "command": "C:\\Users\\<your-username>\\.local\\bin\\uv.exe",
      "args": [
        "--directory",
        "C:\\code\\HR-ASSIST-Agentic-AI-System",
        "run",
        "server.py"
      ],
      "env": {
        "CB_EMAIL": "YOUR_EMAIL",
        "CB_EMAIL_PWD": "YOUR_APP_PASSWORD"
      }
    }
  }
}
```

</details>

- Replace `YOUR_EMAIL` with your email address.
- Replace `YOUR_APP_PASSWORD` with your provider's **app-specific password**.
- Restart Claude Desktop after saving.

> ⚠️ Never commit real credentials. Keep secrets in the config `env` block or a git-ignored `.env` file.

---

## 🚀 Usage

1. Open Claude Desktop and click the **`+`** icon.
2. Choose **Add from hr-assist** and select the `onboard_new_employee` prompt.
3. Fill in the new employee's details and send.

<img src="resources/image.jpg" alt="Claude Desktop onboarding prompt with fields" height="300">

You can also write your own prompt and let the agent take over:

- *"Onboard Priya Sharma under manager Rahul Verma."*
- *"What is Arjun's leave balance?"*
- *"Apply leave for E002 on 12 and 13 November."*
- *"Raise a ticket for a new laptop for E005, the current one is damaged."*
- *"Show all open tickets for E001."*

### Debugging with MCP Inspector

```bash
uv run fastmcp dev server.py
```

---

## 🧱 Tech Stack

Python · FastMCP · MCP (Model Context Protocol) · SMTP · python-dotenv · uv · Claude Desktop

---

## 🗺️ Roadmap

- [ ] Replace in-memory sample data with a persistent database
- [ ] Role-based access (employee / manager / HR)
- [ ] Leave approval workflow
- [ ] Remote transport (HTTP/SSE) for deployment
- [ ] Unit tests for HRMS managers
- [ ] Docker support

---

## 🔒 Security Notes

- Use app-specific passwords, never your main account password.
- Add `.env` to `.gitignore` and rotate any credential that was ever committed.
- Validate inputs and add access control before connecting to real HR data.

---

## 🙌 Acknowledgements

Based on the HR-ASSIST agentic AI project from the Codebasics / LearnerX India course.

**Author:** [Trijesh](https://github.com/trijesh61)

---

<sub>All rights reserved @Codebasics Inc and LearnerX India Private Ltd.</sub>
