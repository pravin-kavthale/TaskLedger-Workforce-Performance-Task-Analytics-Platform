"""
Analytics module for TaskLedger

This module provides analytics and reporting capabilities for workforce performance,
task execution, and time tracking data.
"""

from datetime import datetime, timedelta
from sqlalchemy import func, and_, case
from taskledger.models import (
    Employee, Task, TimeEntry, PerformanceMetric, 
    Team, Department, TaskStatus, TimeEntryType
)


class PerformanceAnalytics:
    """Analytics for workforce performance metrics"""
    
    def __init__(self, session):
        """
        Initialize analytics with database session
        
        Args:
            session: SQLAlchemy database session
        """
        self.session = session
    
    def get_employee_performance_summary(self, employee_id, start_date, end_date):
        """
        Get comprehensive performance summary for an employee
        
        Args:
            employee_id: Employee ID
            start_date: Start date for analysis
            end_date: End date for analysis
            
        Returns:
            dict: Performance summary
        """
        employee = self.session.query(Employee).filter(Employee.id == employee_id).first()
        if not employee:
            return None
        
        # Task statistics
        total_tasks = self.session.query(Task)\
            .filter(Task.assigned_to == employee_id)\
            .filter(Task.created_at >= start_date)\
            .filter(Task.created_at <= end_date)\
            .count()
        
        completed_tasks = self.session.query(Task)\
            .filter(Task.assigned_to == employee_id)\
            .filter(Task.status == TaskStatus.COMPLETED)\
            .filter(Task.created_at >= start_date)\
            .filter(Task.created_at <= end_date)\
            .count()
        
        in_progress_tasks = self.session.query(Task)\
            .filter(Task.assigned_to == employee_id)\
            .filter(Task.status == TaskStatus.IN_PROGRESS)\
            .filter(Task.created_at >= start_date)\
            .filter(Task.created_at <= end_date)\
            .count()
        
        # Time tracking statistics
        total_hours = self.session.query(func.sum(TimeEntry.duration_hours))\
            .filter(TimeEntry.employee_id == employee_id)\
            .filter(TimeEntry.start_time >= start_date)\
            .filter(TimeEntry.start_time <= end_date)\
            .scalar() or 0.0
        
        task_hours = self.session.query(func.sum(TimeEntry.duration_hours))\
            .filter(TimeEntry.employee_id == employee_id)\
            .filter(TimeEntry.entry_type == TimeEntryType.TASK_WORK)\
            .filter(TimeEntry.start_time >= start_date)\
            .filter(TimeEntry.start_time <= end_date)\
            .scalar() or 0.0
        
        # Calculate metrics
        completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0.0
        
        return {
            'employee_id': employee_id,
            'employee_name': f"{employee.first_name} {employee.last_name}",
            'period_start': start_date.isoformat(),
            'period_end': end_date.isoformat(),
            'task_statistics': {
                'total_tasks': total_tasks,
                'completed_tasks': completed_tasks,
                'in_progress_tasks': in_progress_tasks,
                'completion_rate': round(completion_rate, 2)
            },
            'time_statistics': {
                'total_hours': round(total_hours, 2),
                'task_hours': round(task_hours, 2),
                'productivity_ratio': round((task_hours / total_hours * 100) if total_hours > 0 else 0.0, 2)
            }
        }
    
    def get_team_performance_summary(self, team_id, start_date, end_date):
        """
        Get comprehensive performance summary for a team
        
        Args:
            team_id: Team ID
            start_date: Start date for analysis
            end_date: End date for analysis
            
        Returns:
            dict: Team performance summary
        """
        team = self.session.query(Team).filter(Team.id == team_id).first()
        if not team:
            return None
        
        # Get all team members
        team_members = self.session.query(Employee)\
            .filter(Employee.team_id == team_id)\
            .filter(Employee.is_active == True)\
            .all()
        
        team_member_ids = [member.id for member in team_members]
        
        # Task statistics
        total_tasks = self.session.query(Task)\
            .filter(Task.team_id == team_id)\
            .filter(Task.created_at >= start_date)\
            .filter(Task.created_at <= end_date)\
            .count()
        
        completed_tasks = self.session.query(Task)\
            .filter(Task.team_id == team_id)\
            .filter(Task.status == TaskStatus.COMPLETED)\
            .filter(Task.created_at >= start_date)\
            .filter(Task.created_at <= end_date)\
            .count()
        
        # Time statistics
        total_hours = self.session.query(func.sum(TimeEntry.duration_hours))\
            .filter(TimeEntry.employee_id.in_(team_member_ids))\
            .filter(TimeEntry.start_time >= start_date)\
            .filter(TimeEntry.start_time <= end_date)\
            .scalar() or 0.0
        
        return {
            'team_id': team_id,
            'team_name': team.name,
            'period_start': start_date.isoformat(),
            'period_end': end_date.isoformat(),
            'team_size': len(team_members),
            'task_statistics': {
                'total_tasks': total_tasks,
                'completed_tasks': completed_tasks,
                'completion_rate': round((completed_tasks / total_tasks * 100) if total_tasks > 0 else 0.0, 2)
            },
            'time_statistics': {
                'total_hours': round(total_hours, 2),
                'average_hours_per_member': round(total_hours / len(team_members) if team_members else 0.0, 2)
            }
        }
    
    def get_department_performance_summary(self, department_id, start_date, end_date):
        """
        Get comprehensive performance summary for a department
        
        Args:
            department_id: Department ID
            start_date: Start date for analysis
            end_date: End date for analysis
            
        Returns:
            dict: Department performance summary
        """
        department = self.session.query(Department).filter(Department.id == department_id).first()
        if not department:
            return None
        
        # Get all teams in department
        teams = self.session.query(Team)\
            .filter(Team.department_id == department_id)\
            .all()
        
        team_ids = [team.id for team in teams]
        
        # Get all department employees
        employees = self.session.query(Employee)\
            .filter(Employee.department_id == department_id)\
            .filter(Employee.is_active == True)\
            .all()
        
        employee_ids = [emp.id for emp in employees]
        
        # Task statistics
        total_tasks = self.session.query(Task)\
            .filter(Task.team_id.in_(team_ids))\
            .filter(Task.created_at >= start_date)\
            .filter(Task.created_at <= end_date)\
            .count()
        
        completed_tasks = self.session.query(Task)\
            .filter(Task.team_id.in_(team_ids))\
            .filter(Task.status == TaskStatus.COMPLETED)\
            .filter(Task.created_at >= start_date)\
            .filter(Task.created_at <= end_date)\
            .count()
        
        # Time statistics
        total_hours = self.session.query(func.sum(TimeEntry.duration_hours))\
            .filter(TimeEntry.employee_id.in_(employee_ids))\
            .filter(TimeEntry.start_time >= start_date)\
            .filter(TimeEntry.start_time <= end_date)\
            .scalar() or 0.0
        
        return {
            'department_id': department_id,
            'department_name': department.name,
            'period_start': start_date.isoformat(),
            'period_end': end_date.isoformat(),
            'number_of_teams': len(teams),
            'number_of_employees': len(employees),
            'task_statistics': {
                'total_tasks': total_tasks,
                'completed_tasks': completed_tasks,
                'completion_rate': round((completed_tasks / total_tasks * 100) if total_tasks > 0 else 0.0, 2)
            },
            'time_statistics': {
                'total_hours': round(total_hours, 2),
                'average_hours_per_employee': round(total_hours / len(employees) if employees else 0.0, 2)
            }
        }
    
    def get_task_analytics(self, start_date, end_date, team_id=None, department_id=None):
        """
        Get task analytics for specified period and filters
        
        Args:
            start_date: Start date for analysis
            end_date: End date for analysis
            team_id: Optional team filter
            department_id: Optional department filter
            
        Returns:
            dict: Task analytics
        """
        query = self.session.query(Task)\
            .filter(Task.created_at >= start_date)\
            .filter(Task.created_at <= end_date)
        
        if team_id:
            query = query.filter(Task.team_id == team_id)
        
        if department_id:
            query = query.join(Team).filter(Team.department_id == department_id)
        
        # Status distribution
        status_counts = self.session.query(
            Task.status,
            func.count(Task.id)
        ).filter(Task.created_at >= start_date)\
         .filter(Task.created_at <= end_date)
        
        if team_id:
            status_counts = status_counts.filter(Task.team_id == team_id)
        
        status_counts = status_counts.group_by(Task.status).all()
        
        # Priority distribution
        priority_counts = self.session.query(
            Task.priority,
            func.count(Task.id)
        ).filter(Task.created_at >= start_date)\
         .filter(Task.created_at <= end_date)
        
        if team_id:
            priority_counts = priority_counts.filter(Task.team_id == team_id)
        
        priority_counts = priority_counts.group_by(Task.priority).all()
        
        # Average completion time
        completed_tasks = query.filter(Task.status == TaskStatus.COMPLETED)\
            .filter(Task.started_at.isnot(None))\
            .filter(Task.completed_at.isnot(None))\
            .all()
        
        avg_completion_hours = 0.0
        if completed_tasks:
            total_hours = sum([
                (task.completed_at - task.started_at).total_seconds() / 3600.0
                for task in completed_tasks
            ])
            avg_completion_hours = total_hours / len(completed_tasks)
        
        return {
            'period_start': start_date.isoformat(),
            'period_end': end_date.isoformat(),
            'status_distribution': {
                status.value: count for status, count in status_counts
            },
            'priority_distribution': {
                priority.value: count for priority, count in priority_counts
            },
            'average_completion_hours': round(avg_completion_hours, 2),
            'total_tasks': query.count()
        }
