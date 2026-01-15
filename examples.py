"""
TaskLedger Usage Examples

This script demonstrates how to use TaskLedger for common workforce management tasks.
"""

from datetime import datetime, timedelta
from taskledger.database import init_db
from taskledger.models import (
    Department, Team, Employee, Task, TimeEntry, PerformanceMetric,
    TaskStatus, TaskPriority, TimeEntryType
)
from taskledger.analytics import PerformanceAnalytics
from taskledger.utils import (
    calculate_time_entry_duration,
    update_task_actual_hours,
    generate_employee_id,
    generate_task_id
)


def example_1_create_organizational_structure():
    """Example 1: Creating organizational structure"""
    print("\n" + "=" * 60)
    print("Example 1: Creating Organizational Structure")
    print("=" * 60)
    
    db = init_db('sqlite:///example_taskledger.db')
    session = db.get_session()
    
    # Create a department
    dept = Department(
        name="Product Development",
        description="Product development and innovation team"
    )
    session.add(dept)
    session.commit()
    print(f"✓ Created department: {dept.name}")
    
    # Create a team
    team = Team(
        name="Mobile App Team",
        description="iOS and Android app development",
        department_id=dept.id
    )
    session.add(team)
    session.commit()
    print(f"✓ Created team: {team.name}")
    
    # Create employees
    emp1 = Employee(
        employee_id="SARA0001",
        first_name="Sarah",
        last_name="Anderson",
        email="sarah.anderson@company.com",
        department_id=dept.id,
        team_id=team.id,
        position="Mobile Developer",
        hire_date=datetime(2023, 1, 15),
        is_active=True
    )
    session.add(emp1)
    session.commit()
    print(f"✓ Created employee: {emp1.first_name} {emp1.last_name}")
    
    session.close()


def example_2_create_and_track_tasks():
    """Example 2: Creating and tracking tasks"""
    print("\n" + "=" * 60)
    print("Example 2: Creating and Tracking Tasks")
    print("=" * 60)
    
    db = init_db('sqlite:///example_taskledger.db')
    session = db.get_session()
    
    # Get an employee and team
    employee = session.query(Employee).first()
    team = session.query(Team).first()
    
    if not employee or not team:
        print("⚠ Please run Example 1 first to create organizational structure")
        session.close()
        return
    
    # Create a task
    task = Task(
        task_id=generate_task_id(team.id, 1),
        title="Implement push notifications",
        description="Add push notification support to mobile app",
        status=TaskStatus.PENDING,
        priority=TaskPriority.HIGH,
        assigned_to=employee.id,
        team_id=team.id,
        estimated_hours=24.0,
        due_date=datetime.now() + timedelta(days=14)
    )
    session.add(task)
    session.commit()
    print(f"✓ Created task: {task.title} (ID: {task.task_id})")
    
    # Start working on the task
    task.status = TaskStatus.IN_PROGRESS
    task.started_at = datetime.now()
    session.commit()
    print(f"✓ Task status updated to: {task.status.value}")
    
    # Complete the task
    task.status = TaskStatus.COMPLETED
    task.completed_at = datetime.now()
    session.commit()
    print(f"✓ Task completed!")
    
    session.close()


def example_3_track_time():
    """Example 3: Tracking time entries"""
    print("\n" + "=" * 60)
    print("Example 3: Tracking Time Entries")
    print("=" * 60)
    
    db = init_db('sqlite:///example_taskledger.db')
    session = db.get_session()
    
    # Get an employee and task
    employee = session.query(Employee).first()
    task = session.query(Task).first()
    
    if not employee or not task:
        print("⚠ Please run Examples 1 and 2 first")
        session.close()
        return
    
    # Create time entry for task work
    start_time = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
    end_time = start_time + timedelta(hours=3, minutes=30)
    
    time_entry = TimeEntry(
        employee_id=employee.id,
        task_id=task.id,
        entry_type=TimeEntryType.TASK_WORK,
        start_time=start_time,
        end_time=end_time,
        description="Implementing push notification service"
    )
    
    # Calculate duration
    time_entry.duration_hours = calculate_time_entry_duration(time_entry)
    session.add(time_entry)
    session.commit()
    print(f"✓ Logged time entry: {time_entry.duration_hours} hours")
    
    # Update task actual hours
    update_task_actual_hours(session, task.id)
    session.refresh(task)
    print(f"✓ Task actual hours updated: {task.actual_hours}h")
    
    session.close()


def example_4_record_performance_metrics():
    """Example 4: Recording performance metrics"""
    print("\n" + "=" * 60)
    print("Example 4: Recording Performance Metrics")
    print("=" * 60)
    
    db = init_db('sqlite:///example_taskledger.db')
    session = db.get_session()
    
    employee = session.query(Employee).first()
    
    if not employee:
        print("⚠ Please run Example 1 first")
        session.close()
        return
    
    # Record performance metrics
    period_start = datetime.now().replace(day=1)
    period_end = datetime.now()
    
    metrics = [
        PerformanceMetric(
            employee_id=employee.id,
            metric_name="Code Quality Score",
            metric_value=92.5,
            metric_period_start=period_start,
            metric_period_end=period_end,
            notes="Based on code review ratings"
        ),
        PerformanceMetric(
            employee_id=employee.id,
            metric_name="Sprint Velocity",
            metric_value=45.0,
            metric_period_start=period_start,
            metric_period_end=period_end,
            notes="Story points completed"
        )
    ]
    
    for metric in metrics:
        session.add(metric)
        print(f"✓ Recorded metric: {metric.metric_name} = {metric.metric_value}")
    
    session.commit()
    session.close()


def example_5_generate_analytics():
    """Example 5: Generating analytics and reports"""
    print("\n" + "=" * 60)
    print("Example 5: Generating Analytics and Reports")
    print("=" * 60)
    
    db = init_db('sqlite:///example_taskledger.db')
    session = db.get_session()
    
    employee = session.query(Employee).first()
    team = session.query(Team).first()
    
    if not employee or not team:
        print("⚠ Please run previous examples first")
        session.close()
        return
    
    analytics = PerformanceAnalytics(session)
    
    # Set time period
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    # Employee performance summary
    print("\nEmployee Performance Summary:")
    summary = analytics.get_employee_performance_summary(
        employee.id, start_date, end_date
    )
    
    if summary:
        print(f"  Employee: {summary['employee_name']}")
        print(f"  Total Tasks: {summary['task_statistics']['total_tasks']}")
        print(f"  Completed: {summary['task_statistics']['completed_tasks']}")
        print(f"  Completion Rate: {summary['task_statistics']['completion_rate']}%")
        print(f"  Total Hours: {summary['time_statistics']['total_hours']}h")
        print(f"  Task Hours: {summary['time_statistics']['task_hours']}h")
        print(f"  Productivity: {summary['time_statistics']['productivity_ratio']}%")
    
    # Team performance summary
    print("\nTeam Performance Summary:")
    team_summary = analytics.get_team_performance_summary(
        team.id, start_date, end_date
    )
    
    if team_summary:
        print(f"  Team: {team_summary['team_name']}")
        print(f"  Team Size: {team_summary['team_size']}")
        print(f"  Total Tasks: {team_summary['task_statistics']['total_tasks']}")
        print(f"  Completion Rate: {team_summary['task_statistics']['completion_rate']}%")
    
    # Task analytics
    print("\nTask Analytics:")
    task_analytics = analytics.get_task_analytics(start_date, end_date, team_id=team.id)
    print(f"  Total Tasks: {task_analytics['total_tasks']}")
    print(f"  Average Completion Time: {task_analytics['average_completion_hours']}h")
    print("  Status Distribution:")
    for status, count in task_analytics['status_distribution'].items():
        print(f"    - {status}: {count}")
    
    session.close()


def example_6_query_and_filter():
    """Example 6: Querying and filtering data"""
    print("\n" + "=" * 60)
    print("Example 6: Querying and Filtering Data")
    print("=" * 60)
    
    db = init_db('sqlite:///example_taskledger.db')
    session = db.get_session()
    
    # Filter tasks by status
    print("\nFiltering tasks by status:")
    completed_tasks = session.query(Task)\
        .filter(Task.status == TaskStatus.COMPLETED)\
        .all()
    print(f"  Completed tasks: {len(completed_tasks)}")
    
    # Filter tasks by priority
    print("\nFiltering tasks by priority:")
    high_priority_tasks = session.query(Task)\
        .filter(Task.priority == TaskPriority.HIGH)\
        .all()
    print(f"  High priority tasks: {len(high_priority_tasks)}")
    
    # Get active employees
    print("\nQuerying active employees:")
    active_employees = session.query(Employee)\
        .filter(Employee.is_active == True)\
        .all()
    print(f"  Active employees: {len(active_employees)}")
    for emp in active_employees:
        print(f"    - {emp.first_name} {emp.last_name} ({emp.position})")
    
    # Get time entries for specific employee
    if active_employees:
        print(f"\nTime entries for {active_employees[0].first_name}:")
        time_entries = session.query(TimeEntry)\
            .filter(TimeEntry.employee_id == active_employees[0].id)\
            .all()
        total_hours = sum(e.duration_hours for e in time_entries if e.duration_hours)
        print(f"  Total entries: {len(time_entries)}")
        print(f"  Total hours: {total_hours:.2f}h")
    
    session.close()


def run_all_examples():
    """Run all examples in sequence"""
    print("\n" + "=" * 60)
    print("TaskLedger Usage Examples")
    print("=" * 60)
    
    # Clear previous example database
    import os
    if os.path.exists('example_taskledger.db'):
        os.remove('example_taskledger.db')
    
    example_1_create_organizational_structure()
    example_2_create_and_track_tasks()
    example_3_track_time()
    example_4_record_performance_metrics()
    example_5_generate_analytics()
    example_6_query_and_filter()
    
    print("\n" + "=" * 60)
    print("All examples completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    run_all_examples()
