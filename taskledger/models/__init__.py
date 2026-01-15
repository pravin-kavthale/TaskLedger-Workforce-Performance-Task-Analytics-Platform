"""
TaskLedger Data Models

This module defines the core data models for the TaskLedger workforce management system.
It includes models for employees, teams, departments, tasks, time tracking, and performance metrics.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Boolean, Text, Enum
from sqlalchemy.orm import relationship, declarative_base
import enum

Base = declarative_base()


class TaskStatus(enum.Enum):
    """Task status enumeration"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"
    CANCELLED = "cancelled"


class TaskPriority(enum.Enum):
    """Task priority enumeration"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class TimeEntryType(enum.Enum):
    """Time entry type enumeration"""
    TASK_WORK = "task_work"
    MEETING = "meeting"
    BREAK = "break"
    TRAINING = "training"
    OTHER = "other"


class Department(Base):
    """Department model for organizational structure"""
    __tablename__ = 'departments'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    teams = relationship("Team", back_populates="department", cascade="all, delete-orphan")
    employees = relationship("Employee", back_populates="department")
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class Team(Base):
    """Team model for group organization"""
    __tablename__ = 'teams'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    department_id = Column(Integer, ForeignKey('departments.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    department = relationship("Department", back_populates="teams")
    employees = relationship("Employee", back_populates="team")
    tasks = relationship("Task", back_populates="team")
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'department_id': self.department_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class Employee(Base):
    """Employee model for workforce tracking"""
    __tablename__ = 'employees'
    
    id = Column(Integer, primary_key=True)
    employee_id = Column(String(50), unique=True, nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    department_id = Column(Integer, ForeignKey('departments.id'), nullable=False)
    team_id = Column(Integer, ForeignKey('teams.id'))
    position = Column(String(100))
    hire_date = Column(DateTime)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    department = relationship("Department", back_populates="employees")
    team = relationship("Team", back_populates="employees")
    tasks = relationship("Task", back_populates="assigned_to_employee")
    time_entries = relationship("TimeEntry", back_populates="employee", cascade="all, delete-orphan")
    performance_metrics = relationship("PerformanceMetric", back_populates="employee", cascade="all, delete-orphan")
    
    def to_dict(self):
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'department_id': self.department_id,
            'team_id': self.team_id,
            'position': self.position,
            'hire_date': self.hire_date.isoformat() if self.hire_date else None,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class Task(Base):
    """Task model for structured task execution"""
    __tablename__ = 'tasks'
    
    id = Column(Integer, primary_key=True)
    task_id = Column(String(50), unique=True, nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    status = Column(Enum(TaskStatus), default=TaskStatus.PENDING, nullable=False)
    priority = Column(Enum(TaskPriority), default=TaskPriority.MEDIUM, nullable=False)
    assigned_to = Column(Integer, ForeignKey('employees.id'))
    team_id = Column(Integer, ForeignKey('teams.id'))
    estimated_hours = Column(Float)
    actual_hours = Column(Float)
    due_date = Column(DateTime)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    assigned_to_employee = relationship("Employee", back_populates="tasks")
    team = relationship("Team", back_populates="tasks")
    time_entries = relationship("TimeEntry", back_populates="task", cascade="all, delete-orphan")
    
    def to_dict(self):
        return {
            'id': self.id,
            'task_id': self.task_id,
            'title': self.title,
            'description': self.description,
            'status': self.status.value if self.status else None,
            'priority': self.priority.value if self.priority else None,
            'assigned_to': self.assigned_to,
            'team_id': self.team_id,
            'estimated_hours': self.estimated_hours,
            'actual_hours': self.actual_hours,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class TimeEntry(Base):
    """Time entry model for event-driven time tracking"""
    __tablename__ = 'time_entries'
    
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.id'), nullable=False)
    task_id = Column(Integer, ForeignKey('tasks.id'))
    entry_type = Column(Enum(TimeEntryType), default=TimeEntryType.TASK_WORK, nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime)
    duration_hours = Column(Float)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    employee = relationship("Employee", back_populates="time_entries")
    task = relationship("Task", back_populates="time_entries")
    
    def to_dict(self):
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'task_id': self.task_id,
            'entry_type': self.entry_type.value if self.entry_type else None,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'duration_hours': self.duration_hours,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class PerformanceMetric(Base):
    """Performance metric model for analytics-ready data"""
    __tablename__ = 'performance_metrics'
    
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.id'), nullable=False)
    metric_name = Column(String(100), nullable=False)
    metric_value = Column(Float, nullable=False)
    metric_period_start = Column(DateTime, nullable=False)
    metric_period_end = Column(DateTime, nullable=False)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    employee = relationship("Employee", back_populates="performance_metrics")
    
    def to_dict(self):
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'metric_name': self.metric_name,
            'metric_value': self.metric_value,
            'metric_period_start': self.metric_period_start.isoformat() if self.metric_period_start else None,
            'metric_period_end': self.metric_period_end.isoformat() if self.metric_period_end else None,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
