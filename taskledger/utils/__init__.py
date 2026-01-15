"""
Utility functions for TaskLedger
"""

from datetime import datetime, timedelta
from sqlalchemy import func
from taskledger.models import TimeEntry, Task, PerformanceMetric


def calculate_time_entry_duration(time_entry):
    """
    Calculate duration in hours for a time entry
    
    Args:
        time_entry: TimeEntry object
        
    Returns:
        float: Duration in hours
    """
    if time_entry.end_time and time_entry.start_time:
        delta = time_entry.end_time - time_entry.start_time
        return delta.total_seconds() / 3600.0
    return 0.0


def update_task_actual_hours(session, task_id):
    """
    Update the actual hours for a task based on time entries
    
    Args:
        session: Database session
        task_id: Task ID
    """
    task = session.query(Task).filter(Task.id == task_id).first()
    if task:
        total_hours = session.query(func.sum(TimeEntry.duration_hours))\
            .filter(TimeEntry.task_id == task_id)\
            .scalar() or 0.0
        task.actual_hours = total_hours
        session.commit()


def generate_employee_id(first_name, last_name, sequence_number):
    """
    Generate a unique employee ID
    
    Args:
        first_name: Employee first name
        last_name: Employee last name
        sequence_number: Sequence number for uniqueness
        
    Returns:
        str: Generated employee ID
    """
    prefix = (first_name[:2] + last_name[:2]).upper()
    return f"{prefix}{sequence_number:04d}"


def generate_task_id(team_id, sequence_number):
    """
    Generate a unique task ID
    
    Args:
        team_id: Team ID
        sequence_number: Sequence number for uniqueness
        
    Returns:
        str: Generated task ID
    """
    return f"TASK-{team_id}-{sequence_number:05d}"


def calculate_completion_rate(session, employee_id, start_date, end_date):
    """
    Calculate task completion rate for an employee
    
    Args:
        session: Database session
        employee_id: Employee ID
        start_date: Start date for calculation
        end_date: End date for calculation
        
    Returns:
        float: Completion rate (0-100)
    """
    from taskledger.models import TaskStatus
    
    total_tasks = session.query(Task)\
        .filter(Task.assigned_to == employee_id)\
        .filter(Task.created_at >= start_date)\
        .filter(Task.created_at <= end_date)\
        .count()
    
    if total_tasks == 0:
        return 0.0
    
    completed_tasks = session.query(Task)\
        .filter(Task.assigned_to == employee_id)\
        .filter(Task.status == TaskStatus.COMPLETED)\
        .filter(Task.created_at >= start_date)\
        .filter(Task.created_at <= end_date)\
        .count()
    
    return (completed_tasks / total_tasks) * 100.0


def calculate_average_task_duration(session, employee_id, start_date, end_date):
    """
    Calculate average task duration for an employee
    
    Args:
        session: Database session
        employee_id: Employee ID
        start_date: Start date for calculation
        end_date: End date for calculation
        
    Returns:
        float: Average duration in hours
    """
    from taskledger.models import TaskStatus
    
    completed_tasks = session.query(Task)\
        .filter(Task.assigned_to == employee_id)\
        .filter(Task.status == TaskStatus.COMPLETED)\
        .filter(Task.completed_at >= start_date)\
        .filter(Task.completed_at <= end_date)\
        .all()
    
    if not completed_tasks:
        return 0.0
    
    total_duration = sum([
        (task.completed_at - task.started_at).total_seconds() / 3600.0
        for task in completed_tasks
        if task.started_at and task.completed_at
    ])
    
    return total_duration / len(completed_tasks) if completed_tasks else 0.0
