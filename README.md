# TaskLedger - Workforce Performance & Task Analytics Platform

TaskLedger is a modular workforce management system designed to track tasks, time-based activities, and performance metrics across employees, teams, and departments. The platform focuses on structured task execution, event-driven time tracking, and analytics-ready data modeling, making it suitable for enterprise environments and data-driven performance evaluation.

## Features

### Core Capabilities

- **Employee Management**: Track employee information, organizational structure, and team assignments
- **Task Tracking**: Structured task execution with status tracking, priority management, and time estimation
- **Time Tracking**: Event-driven time tracking with support for different activity types
- **Team & Department Organization**: Hierarchical organizational structure management
- **Performance Metrics**: Analytics-ready performance data collection and evaluation
- **RESTful API**: Comprehensive REST API for all platform operations

### Data Models

- **Employee**: Workforce tracking with department and team assignments
- **Department**: High-level organizational units
- **Team**: Work groups within departments
- **Task**: Structured tasks with status, priority, and time tracking
- **TimeEntry**: Event-driven time tracking entries
- **PerformanceMetric**: Performance measurement data

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/pravin-kavthale/TaskLedger-Workforce-Performance-Task-Analytics-Platform.git
cd TaskLedger-Workforce-Performance-Task-Analytics-Platform
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install the package:
```bash
pip install -e .
```

## Usage

### Starting the API Server

```bash
python -m taskledger.api
```

The API server will start on `http://localhost:5000`

### Generating Sample Data

To populate the database with sample data for testing:

```bash
python sample_data.py
```

This will create:
- 3 departments (Engineering, Sales, HR)
- 3 teams with various members
- 4 employees with different roles
- 5 tasks with different statuses
- Multiple time entries
- Performance metrics

## API Endpoints

### Health Check
- `GET /health` - Health check endpoint

### Departments
- `GET /api/departments` - List all departments
- `POST /api/departments` - Create a new department
- `GET /api/departments/<id>` - Get department details
- `PUT /api/departments/<id>` - Update department
- `DELETE /api/departments/<id>` - Delete department

### Teams
- `GET /api/teams` - List all teams
- `POST /api/teams` - Create a new team
- `GET /api/teams/<id>` - Get team details
- `PUT /api/teams/<id>` - Update team
- `DELETE /api/teams/<id>` - Delete team

### Employees
- `GET /api/employees` - List all employees
- `POST /api/employees` - Create a new employee
- `GET /api/employees/<id>` - Get employee details
- `PUT /api/employees/<id>` - Update employee
- `DELETE /api/employees/<id>` - Delete employee

### Tasks
- `GET /api/tasks` - List all tasks (supports filtering by status, assigned_to, team_id)
- `POST /api/tasks` - Create a new task
- `GET /api/tasks/<id>` - Get task details
- `PUT /api/tasks/<id>` - Update task
- `DELETE /api/tasks/<id>` - Delete task

### Time Entries
- `GET /api/time-entries` - List all time entries (supports filtering by employee_id, task_id)
- `POST /api/time-entries` - Create a new time entry
- `GET /api/time-entries/<id>` - Get time entry details
- `PUT /api/time-entries/<id>` - Update time entry
- `DELETE /api/time-entries/<id>` - Delete time entry

### Performance Metrics
- `GET /api/performance-metrics` - List all metrics (supports filtering by employee_id)
- `POST /api/performance-metrics` - Create a new metric

### Analytics
- `GET /api/analytics/employee/<id>?start_date=<date>&end_date=<date>` - Employee performance summary
- `GET /api/analytics/team/<id>?start_date=<date>&end_date=<date>` - Team performance summary
- `GET /api/analytics/department/<id>?start_date=<date>&end_date=<date>` - Department performance summary
- `GET /api/analytics/tasks?start_date=<date>&end_date=<date>` - Task analytics

## Example API Usage

### Create a Department
```bash
curl -X POST http://localhost:5000/api/departments \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Engineering",
    "description": "Software development teams"
  }'
```

### Create a Task
```bash
curl -X POST http://localhost:5000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Implement API endpoint",
    "description": "Create REST API for user management",
    "status": "pending",
    "priority": "high",
    "assigned_to": 1,
    "team_id": 1,
    "estimated_hours": 40.0,
    "due_date": "2026-02-01T00:00:00"
  }'
```

### Track Time Entry
```bash
curl -X POST http://localhost:5000/api/time-entries \
  -H "Content-Type: application/json" \
  -d '{
    "employee_id": 1,
    "task_id": 1,
    "entry_type": "task_work",
    "start_time": "2026-01-15T09:00:00",
    "end_time": "2026-01-15T12:30:00",
    "description": "Working on API implementation"
  }'
```

### Get Employee Analytics
```bash
curl "http://localhost:5000/api/analytics/employee/1?start_date=2026-01-01T00:00:00&end_date=2026-01-31T23:59:59"
```

## Architecture

### Data Models

TaskLedger uses SQLAlchemy ORM for data modeling with the following relationships:

- Department → Teams (one-to-many)
- Department → Employees (one-to-many)
- Team → Employees (one-to-many)
- Team → Tasks (one-to-many)
- Employee → Tasks (one-to-many)
- Employee → TimeEntries (one-to-many)
- Employee → PerformanceMetrics (one-to-many)
- Task → TimeEntries (one-to-many)

### Technology Stack

- **Backend Framework**: Flask
- **ORM**: SQLAlchemy
- **Database**: SQLite (default), PostgreSQL (production-ready)
- **Python Version**: 3.8+

## Database Configuration

By default, TaskLedger uses SQLite. To use PostgreSQL:

```python
from taskledger.api import create_app

app = create_app('postgresql://user:password@localhost/taskledger')
```

## Project Structure

```
TaskLedger-Workforce-Performance-Task-Analytics-Platform/
├── taskledger/
│   ├── __init__.py
│   ├── models/
│   │   └── __init__.py          # Data models
│   ├── api/
│   │   └── __init__.py          # REST API endpoints
│   ├── analytics/
│   │   └── __init__.py          # Analytics and reporting
│   ├── utils/
│   │   └── __init__.py          # Utility functions
│   └── database.py              # Database configuration
├── sample_data.py               # Sample data generator
├── requirements.txt             # Python dependencies
├── setup.py                     # Package setup
└── README.md                    # This file
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.