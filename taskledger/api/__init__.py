"""
TaskLedger REST API

This module provides a RESTful API for the TaskLedger workforce management system.
"""

from flask import Flask, request, jsonify
from datetime import datetime
from taskledger.database import init_db, get_db
from taskledger.models import (
    Employee, Department, Team, Task, TimeEntry, PerformanceMetric,
    TaskStatus, TaskPriority, TimeEntryType
)
from taskledger.analytics import PerformanceAnalytics
from taskledger.utils import (
    calculate_time_entry_duration,
    update_task_actual_hours,
    generate_employee_id,
    generate_task_id
)


def create_app(database_url='sqlite:///taskledger.db'):
    """
    Create and configure the Flask application
    
    Args:
        database_url: Database connection URL
        
    Returns:
        Flask: Configured Flask application
    """
    app = Flask(__name__)
    app.config['DATABASE_URL'] = database_url
    
    # Initialize database
    init_db(database_url)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Resource not found'}), 404
    
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'error': 'Bad request'}), 400
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500
    
    # Health check endpoint
    @app.route('/health', methods=['GET'])
    def health_check():
        """Health check endpoint"""
        return jsonify({'status': 'healthy', 'service': 'TaskLedger'}), 200
    
    # Department endpoints
    @app.route('/api/departments', methods=['GET', 'POST'])
    def departments():
        """List all departments or create a new department"""
        db = get_db()
        session = db.get_session()
        
        try:
            if request.method == 'GET':
                departments = session.query(Department).all()
                return jsonify([dept.to_dict() for dept in departments]), 200
            
            elif request.method == 'POST':
                data = request.json
                department = Department(
                    name=data['name'],
                    description=data.get('description')
                )
                session.add(department)
                session.commit()
                return jsonify(department.to_dict()), 201
        finally:
            session.close()
    
    @app.route('/api/departments/<int:dept_id>', methods=['GET', 'PUT', 'DELETE'])
    def department_detail(dept_id):
        """Get, update, or delete a specific department"""
        db = get_db()
        session = db.get_session()
        
        try:
            department = session.query(Department).filter(Department.id == dept_id).first()
            if not department:
                return jsonify({'error': 'Department not found'}), 404
            
            if request.method == 'GET':
                return jsonify(department.to_dict()), 200
            
            elif request.method == 'PUT':
                data = request.json
                if 'name' in data:
                    department.name = data['name']
                if 'description' in data:
                    department.description = data['description']
                session.commit()
                return jsonify(department.to_dict()), 200
            
            elif request.method == 'DELETE':
                session.delete(department)
                session.commit()
                return jsonify({'message': 'Department deleted'}), 200
        finally:
            session.close()
    
    # Team endpoints
    @app.route('/api/teams', methods=['GET', 'POST'])
    def teams():
        """List all teams or create a new team"""
        db = get_db()
        session = db.get_session()
        
        try:
            if request.method == 'GET':
                teams = session.query(Team).all()
                return jsonify([team.to_dict() for team in teams]), 200
            
            elif request.method == 'POST':
                data = request.json
                team = Team(
                    name=data['name'],
                    description=data.get('description'),
                    department_id=data['department_id']
                )
                session.add(team)
                session.commit()
                return jsonify(team.to_dict()), 201
        finally:
            session.close()
    
    @app.route('/api/teams/<int:team_id>', methods=['GET', 'PUT', 'DELETE'])
    def team_detail(team_id):
        """Get, update, or delete a specific team"""
        db = get_db()
        session = db.get_session()
        
        try:
            team = session.query(Team).filter(Team.id == team_id).first()
            if not team:
                return jsonify({'error': 'Team not found'}), 404
            
            if request.method == 'GET':
                return jsonify(team.to_dict()), 200
            
            elif request.method == 'PUT':
                data = request.json
                if 'name' in data:
                    team.name = data['name']
                if 'description' in data:
                    team.description = data['description']
                if 'department_id' in data:
                    team.department_id = data['department_id']
                session.commit()
                return jsonify(team.to_dict()), 200
            
            elif request.method == 'DELETE':
                session.delete(team)
                session.commit()
                return jsonify({'message': 'Team deleted'}), 200
        finally:
            session.close()
    
    # Employee endpoints
    @app.route('/api/employees', methods=['GET', 'POST'])
    def employees():
        """List all employees or create a new employee"""
        db = get_db()
        session = db.get_session()
        
        try:
            if request.method == 'GET':
                employees = session.query(Employee).all()
                return jsonify([emp.to_dict() for emp in employees]), 200
            
            elif request.method == 'POST':
                data = request.json
                
                # Generate employee ID if not provided
                if 'employee_id' not in data:
                    count = session.query(Employee).count()
                    employee_id = generate_employee_id(
                        data['first_name'],
                        data['last_name'],
                        count + 1
                    )
                else:
                    employee_id = data['employee_id']
                
                employee = Employee(
                    employee_id=employee_id,
                    first_name=data['first_name'],
                    last_name=data['last_name'],
                    email=data['email'],
                    department_id=data['department_id'],
                    team_id=data.get('team_id'),
                    position=data.get('position'),
                    hire_date=datetime.fromisoformat(data['hire_date']) if 'hire_date' in data else None
                )
                session.add(employee)
                session.commit()
                return jsonify(employee.to_dict()), 201
        finally:
            session.close()
    
    @app.route('/api/employees/<int:emp_id>', methods=['GET', 'PUT', 'DELETE'])
    def employee_detail(emp_id):
        """Get, update, or delete a specific employee"""
        db = get_db()
        session = db.get_session()
        
        try:
            employee = session.query(Employee).filter(Employee.id == emp_id).first()
            if not employee:
                return jsonify({'error': 'Employee not found'}), 404
            
            if request.method == 'GET':
                return jsonify(employee.to_dict()), 200
            
            elif request.method == 'PUT':
                data = request.json
                if 'first_name' in data:
                    employee.first_name = data['first_name']
                if 'last_name' in data:
                    employee.last_name = data['last_name']
                if 'email' in data:
                    employee.email = data['email']
                if 'position' in data:
                    employee.position = data['position']
                if 'team_id' in data:
                    employee.team_id = data['team_id']
                if 'is_active' in data:
                    employee.is_active = data['is_active']
                session.commit()
                return jsonify(employee.to_dict()), 200
            
            elif request.method == 'DELETE':
                session.delete(employee)
                session.commit()
                return jsonify({'message': 'Employee deleted'}), 200
        finally:
            session.close()
    
    # Task endpoints
    @app.route('/api/tasks', methods=['GET', 'POST'])
    def tasks():
        """List all tasks or create a new task"""
        db = get_db()
        session = db.get_session()
        
        try:
            if request.method == 'GET':
                # Support filtering
                query = session.query(Task)
                
                if 'status' in request.args:
                    query = query.filter(Task.status == TaskStatus(request.args['status']))
                if 'assigned_to' in request.args:
                    query = query.filter(Task.assigned_to == int(request.args['assigned_to']))
                if 'team_id' in request.args:
                    query = query.filter(Task.team_id == int(request.args['team_id']))
                
                tasks = query.all()
                return jsonify([task.to_dict() for task in tasks]), 200
            
            elif request.method == 'POST':
                data = request.json
                
                # Generate task ID if not provided
                if 'task_id' not in data:
                    team_id = data.get('team_id', 0)
                    count = session.query(Task).filter(Task.team_id == team_id).count()
                    task_id = generate_task_id(team_id, count + 1)
                else:
                    task_id = data['task_id']
                
                task = Task(
                    task_id=task_id,
                    title=data['title'],
                    description=data.get('description'),
                    status=TaskStatus(data.get('status', 'pending')),
                    priority=TaskPriority(data.get('priority', 'medium')),
                    assigned_to=data.get('assigned_to'),
                    team_id=data.get('team_id'),
                    estimated_hours=data.get('estimated_hours'),
                    due_date=datetime.fromisoformat(data['due_date']) if 'due_date' in data else None
                )
                session.add(task)
                session.commit()
                return jsonify(task.to_dict()), 201
        finally:
            session.close()
    
    @app.route('/api/tasks/<int:task_id>', methods=['GET', 'PUT', 'DELETE'])
    def task_detail(task_id):
        """Get, update, or delete a specific task"""
        db = get_db()
        session = db.get_session()
        
        try:
            task = session.query(Task).filter(Task.id == task_id).first()
            if not task:
                return jsonify({'error': 'Task not found'}), 404
            
            if request.method == 'GET':
                return jsonify(task.to_dict()), 200
            
            elif request.method == 'PUT':
                data = request.json
                if 'title' in data:
                    task.title = data['title']
                if 'description' in data:
                    task.description = data['description']
                if 'status' in data:
                    new_status = TaskStatus(data['status'])
                    task.status = new_status
                    
                    # Update timestamps based on status
                    if new_status == TaskStatus.IN_PROGRESS and not task.started_at:
                        task.started_at = datetime.utcnow()
                    elif new_status == TaskStatus.COMPLETED and not task.completed_at:
                        task.completed_at = datetime.utcnow()
                
                if 'priority' in data:
                    task.priority = TaskPriority(data['priority'])
                if 'assigned_to' in data:
                    task.assigned_to = data['assigned_to']
                if 'estimated_hours' in data:
                    task.estimated_hours = data['estimated_hours']
                if 'due_date' in data:
                    task.due_date = datetime.fromisoformat(data['due_date'])
                
                session.commit()
                return jsonify(task.to_dict()), 200
            
            elif request.method == 'DELETE':
                session.delete(task)
                session.commit()
                return jsonify({'message': 'Task deleted'}), 200
        finally:
            session.close()
    
    # Time entry endpoints
    @app.route('/api/time-entries', methods=['GET', 'POST'])
    def time_entries():
        """List all time entries or create a new time entry"""
        db = get_db()
        session = db.get_session()
        
        try:
            if request.method == 'GET':
                query = session.query(TimeEntry)
                
                if 'employee_id' in request.args:
                    query = query.filter(TimeEntry.employee_id == int(request.args['employee_id']))
                if 'task_id' in request.args:
                    query = query.filter(TimeEntry.task_id == int(request.args['task_id']))
                
                entries = query.all()
                return jsonify([entry.to_dict() for entry in entries]), 200
            
            elif request.method == 'POST':
                data = request.json
                
                time_entry = TimeEntry(
                    employee_id=data['employee_id'],
                    task_id=data.get('task_id'),
                    entry_type=TimeEntryType(data.get('entry_type', 'task_work')),
                    start_time=datetime.fromisoformat(data['start_time']),
                    end_time=datetime.fromisoformat(data['end_time']) if 'end_time' in data else None,
                    description=data.get('description')
                )
                
                # Calculate duration if end_time is provided
                if time_entry.end_time:
                    time_entry.duration_hours = calculate_time_entry_duration(time_entry)
                
                session.add(time_entry)
                session.commit()
                
                # Update task actual hours if applicable
                if time_entry.task_id and time_entry.duration_hours:
                    update_task_actual_hours(session, time_entry.task_id)
                
                return jsonify(time_entry.to_dict()), 201
        finally:
            session.close()
    
    @app.route('/api/time-entries/<int:entry_id>', methods=['GET', 'PUT', 'DELETE'])
    def time_entry_detail(entry_id):
        """Get, update, or delete a specific time entry"""
        db = get_db()
        session = db.get_session()
        
        try:
            time_entry = session.query(TimeEntry).filter(TimeEntry.id == entry_id).first()
            if not time_entry:
                return jsonify({'error': 'Time entry not found'}), 404
            
            if request.method == 'GET':
                return jsonify(time_entry.to_dict()), 200
            
            elif request.method == 'PUT':
                data = request.json
                
                if 'end_time' in data and not time_entry.end_time:
                    time_entry.end_time = datetime.fromisoformat(data['end_time'])
                    time_entry.duration_hours = calculate_time_entry_duration(time_entry)
                    
                    # Update task actual hours
                    if time_entry.task_id:
                        update_task_actual_hours(session, time_entry.task_id)
                
                if 'description' in data:
                    time_entry.description = data['description']
                
                session.commit()
                return jsonify(time_entry.to_dict()), 200
            
            elif request.method == 'DELETE':
                task_id = time_entry.task_id
                session.delete(time_entry)
                session.commit()
                
                # Update task actual hours
                if task_id:
                    update_task_actual_hours(session, task_id)
                
                return jsonify({'message': 'Time entry deleted'}), 200
        finally:
            session.close()
    
    # Performance metrics endpoints
    @app.route('/api/performance-metrics', methods=['GET', 'POST'])
    def performance_metrics():
        """List all performance metrics or create a new metric"""
        db = get_db()
        session = db.get_session()
        
        try:
            if request.method == 'GET':
                query = session.query(PerformanceMetric)
                
                if 'employee_id' in request.args:
                    query = query.filter(PerformanceMetric.employee_id == int(request.args['employee_id']))
                
                metrics = query.all()
                return jsonify([metric.to_dict() for metric in metrics]), 200
            
            elif request.method == 'POST':
                data = request.json
                
                metric = PerformanceMetric(
                    employee_id=data['employee_id'],
                    metric_name=data['metric_name'],
                    metric_value=data['metric_value'],
                    metric_period_start=datetime.fromisoformat(data['metric_period_start']),
                    metric_period_end=datetime.fromisoformat(data['metric_period_end']),
                    notes=data.get('notes')
                )
                session.add(metric)
                session.commit()
                return jsonify(metric.to_dict()), 201
        finally:
            session.close()
    
    # Analytics endpoints
    @app.route('/api/analytics/employee/<int:employee_id>', methods=['GET'])
    def employee_analytics(employee_id):
        """Get performance analytics for an employee"""
        db = get_db()
        session = db.get_session()
        
        try:
            start_date = datetime.fromisoformat(request.args.get('start_date'))
            end_date = datetime.fromisoformat(request.args.get('end_date'))
            
            analytics = PerformanceAnalytics(session)
            summary = analytics.get_employee_performance_summary(employee_id, start_date, end_date)
            
            if not summary:
                return jsonify({'error': 'Employee not found'}), 404
            
            return jsonify(summary), 200
        finally:
            session.close()
    
    @app.route('/api/analytics/team/<int:team_id>', methods=['GET'])
    def team_analytics(team_id):
        """Get performance analytics for a team"""
        db = get_db()
        session = db.get_session()
        
        try:
            start_date = datetime.fromisoformat(request.args.get('start_date'))
            end_date = datetime.fromisoformat(request.args.get('end_date'))
            
            analytics = PerformanceAnalytics(session)
            summary = analytics.get_team_performance_summary(team_id, start_date, end_date)
            
            if not summary:
                return jsonify({'error': 'Team not found'}), 404
            
            return jsonify(summary), 200
        finally:
            session.close()
    
    @app.route('/api/analytics/department/<int:department_id>', methods=['GET'])
    def department_analytics(department_id):
        """Get performance analytics for a department"""
        db = get_db()
        session = db.get_session()
        
        try:
            start_date = datetime.fromisoformat(request.args.get('start_date'))
            end_date = datetime.fromisoformat(request.args.get('end_date'))
            
            analytics = PerformanceAnalytics(session)
            summary = analytics.get_department_performance_summary(department_id, start_date, end_date)
            
            if not summary:
                return jsonify({'error': 'Department not found'}), 404
            
            return jsonify(summary), 200
        finally:
            session.close()
    
    @app.route('/api/analytics/tasks', methods=['GET'])
    def task_analytics():
        """Get task analytics"""
        db = get_db()
        session = db.get_session()
        
        try:
            start_date = datetime.fromisoformat(request.args.get('start_date'))
            end_date = datetime.fromisoformat(request.args.get('end_date'))
            team_id = int(request.args['team_id']) if 'team_id' in request.args else None
            department_id = int(request.args['department_id']) if 'department_id' in request.args else None
            
            analytics = PerformanceAnalytics(session)
            summary = analytics.get_task_analytics(start_date, end_date, team_id, department_id)
            
            return jsonify(summary), 200
        finally:
            session.close()
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
