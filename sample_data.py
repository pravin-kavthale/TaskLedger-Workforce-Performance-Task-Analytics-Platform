"""
Sample data generator for TaskLedger

This script creates sample data to demonstrate the TaskLedger system capabilities.
"""

from datetime import datetime, timedelta
from taskledger.database import init_db
from taskledger.models import (
    Department, Team, Employee, Task, TimeEntry, PerformanceMetric,
    TaskStatus, TaskPriority, TimeEntryType
)


def generate_sample_data():
    """Generate sample data for TaskLedger"""
    
    # Initialize database
    db = init_db()
    session = db.get_session()
    
    try:
        # Clear existing data
        session.query(PerformanceMetric).delete()
        session.query(TimeEntry).delete()
        session.query(Task).delete()
        session.query(Employee).delete()
        session.query(Team).delete()
        session.query(Department).delete()
        session.commit()
        
        # Create departments
        print("Creating departments...")
        engineering = Department(
            name="Engineering",
            description="Software development and engineering teams"
        )
        sales = Department(
            name="Sales",
            description="Sales and business development teams"
        )
        hr = Department(
            name="Human Resources",
            description="HR and recruitment teams"
        )
        
        session.add_all([engineering, sales, hr])
        session.commit()
        
        # Create teams
        print("Creating teams...")
        backend_team = Team(
            name="Backend Development",
            description="Backend API and database development",
            department_id=engineering.id
        )
        frontend_team = Team(
            name="Frontend Development",
            description="UI/UX and frontend development",
            department_id=engineering.id
        )
        sales_team = Team(
            name="Enterprise Sales",
            description="Enterprise sales team",
            department_id=sales.id
        )
        
        session.add_all([backend_team, frontend_team, sales_team])
        session.commit()
        
        # Create employees
        print("Creating employees...")
        employees = [
            Employee(
                employee_id="JODO0001",
                first_name="John",
                last_name="Doe",
                email="john.doe@taskledger.com",
                department_id=engineering.id,
                team_id=backend_team.id,
                position="Senior Backend Developer",
                hire_date=datetime(2022, 1, 15),
                is_active=True
            ),
            Employee(
                employee_id="JASM0002",
                first_name="Jane",
                last_name="Smith",
                email="jane.smith@taskledger.com",
                department_id=engineering.id,
                team_id=frontend_team.id,
                position="Frontend Developer",
                hire_date=datetime(2022, 3, 10),
                is_active=True
            ),
            Employee(
                employee_id="BOJO0003",
                first_name="Bob",
                last_name="Johnson",
                email="bob.johnson@taskledger.com",
                department_id=sales.id,
                team_id=sales_team.id,
                position="Sales Manager",
                hire_date=datetime(2021, 6, 1),
                is_active=True
            ),
            Employee(
                employee_id="ALEE0004",
                first_name="Alice",
                last_name="Lee",
                email="alice.lee@taskledger.com",
                department_id=engineering.id,
                team_id=backend_team.id,
                position="Backend Developer",
                hire_date=datetime(2023, 2, 20),
                is_active=True
            )
        ]
        
        session.add_all(employees)
        session.commit()
        
        # Create tasks
        print("Creating tasks...")
        base_date = datetime.utcnow() - timedelta(days=30)
        
        tasks = [
            Task(
                task_id="TASK-{}-00001".format(backend_team.id),
                title="Implement user authentication API",
                description="Create REST API endpoints for user authentication",
                status=TaskStatus.COMPLETED,
                priority=TaskPriority.HIGH,
                assigned_to=employees[0].id,
                team_id=backend_team.id,
                estimated_hours=40.0,
                actual_hours=38.5,
                due_date=base_date + timedelta(days=14),
                started_at=base_date,
                completed_at=base_date + timedelta(days=12)
            ),
            Task(
                task_id="TASK-{}-00002".format(backend_team.id),
                title="Database schema optimization",
                description="Optimize database queries and add indexes",
                status=TaskStatus.IN_PROGRESS,
                priority=TaskPriority.MEDIUM,
                assigned_to=employees[3].id,
                team_id=backend_team.id,
                estimated_hours=30.0,
                actual_hours=15.0,
                due_date=base_date + timedelta(days=21),
                started_at=base_date + timedelta(days=10)
            ),
            Task(
                task_id="TASK-{}-00001".format(frontend_team.id),
                title="Design dashboard UI",
                description="Create mockups and implement dashboard interface",
                status=TaskStatus.COMPLETED,
                priority=TaskPriority.HIGH,
                assigned_to=employees[1].id,
                team_id=frontend_team.id,
                estimated_hours=50.0,
                actual_hours=52.0,
                due_date=base_date + timedelta(days=20),
                started_at=base_date + timedelta(days=2),
                completed_at=base_date + timedelta(days=18)
            ),
            Task(
                task_id="TASK-{}-00002".format(frontend_team.id),
                title="Implement responsive navigation",
                description="Create responsive navigation component",
                status=TaskStatus.PENDING,
                priority=TaskPriority.MEDIUM,
                assigned_to=employees[1].id,
                team_id=frontend_team.id,
                estimated_hours=20.0,
                due_date=base_date + timedelta(days=25)
            ),
            Task(
                task_id="TASK-{}-00001".format(sales_team.id),
                title="Q4 sales strategy planning",
                description="Develop and document Q4 sales strategy",
                status=TaskStatus.COMPLETED,
                priority=TaskPriority.CRITICAL,
                assigned_to=employees[2].id,
                team_id=sales_team.id,
                estimated_hours=25.0,
                actual_hours=28.0,
                due_date=base_date + timedelta(days=10),
                started_at=base_date,
                completed_at=base_date + timedelta(days=8)
            )
        ]
        
        session.add_all(tasks)
        session.commit()
        
        # Create time entries
        print("Creating time entries...")
        time_entries = []
        
        # Time entries for John Doe
        for day in range(12):
            entry_date = base_date + timedelta(days=day)
            time_entries.append(TimeEntry(
                employee_id=employees[0].id,
                task_id=tasks[0].id,
                entry_type=TimeEntryType.TASK_WORK,
                start_time=entry_date.replace(hour=9, minute=0),
                end_time=entry_date.replace(hour=12, minute=30),
                duration_hours=3.5,
                description="Working on authentication endpoints"
            ))
        
        # Time entries for Jane Smith
        for day in range(2, 18):
            entry_date = base_date + timedelta(days=day)
            time_entries.append(TimeEntry(
                employee_id=employees[1].id,
                task_id=tasks[2].id,
                entry_type=TimeEntryType.TASK_WORK,
                start_time=entry_date.replace(hour=9, minute=0),
                end_time=entry_date.replace(hour=12, minute=0),
                duration_hours=3.0,
                description="Designing and implementing dashboard"
            ))
        
        # Time entries for Alice Lee
        for day in range(10, 25):
            if day < 20:
                entry_date = base_date + timedelta(days=day)
                time_entries.append(TimeEntry(
                    employee_id=employees[3].id,
                    task_id=tasks[1].id,
                    entry_type=TimeEntryType.TASK_WORK,
                    start_time=entry_date.replace(hour=10, minute=0),
                    end_time=entry_date.replace(hour=11, minute=30),
                    duration_hours=1.5,
                    description="Database optimization work"
                ))
        
        # Time entries for Bob Johnson
        for day in range(8):
            entry_date = base_date + timedelta(days=day)
            time_entries.append(TimeEntry(
                employee_id=employees[2].id,
                task_id=tasks[4].id,
                entry_type=TimeEntryType.TASK_WORK,
                start_time=entry_date.replace(hour=9, minute=0),
                end_time=entry_date.replace(hour=12, minute=30),
                duration_hours=3.5,
                description="Sales strategy planning"
            ))
        
        session.add_all(time_entries)
        session.commit()
        
        # Create performance metrics
        print("Creating performance metrics...")
        metrics_start = base_date
        metrics_end = base_date + timedelta(days=30)
        
        metrics = [
            PerformanceMetric(
                employee_id=employees[0].id,
                metric_name="Task Completion Rate",
                metric_value=95.5,
                metric_period_start=metrics_start,
                metric_period_end=metrics_end,
                notes="Excellent task completion rate"
            ),
            PerformanceMetric(
                employee_id=employees[1].id,
                metric_name="Code Review Quality",
                metric_value=88.0,
                metric_period_start=metrics_start,
                metric_period_end=metrics_end,
                notes="High quality code reviews"
            ),
            PerformanceMetric(
                employee_id=employees[2].id,
                metric_name="Sales Target Achievement",
                metric_value=112.0,
                metric_period_start=metrics_start,
                metric_period_end=metrics_end,
                notes="Exceeded sales targets"
            )
        ]
        
        session.add_all(metrics)
        session.commit()
        
        print("\nSample data generated successfully!")
        print(f"- {len([engineering, sales, hr])} departments")
        print(f"- {len([backend_team, frontend_team, sales_team])} teams")
        print(f"- {len(employees)} employees")
        print(f"- {len(tasks)} tasks")
        print(f"- {len(time_entries)} time entries")
        print(f"- {len(metrics)} performance metrics")
        
    except Exception as e:
        print(f"Error generating sample data: {e}")
        session.rollback()
    finally:
        session.close()


if __name__ == "__main__":
    generate_sample_data()
