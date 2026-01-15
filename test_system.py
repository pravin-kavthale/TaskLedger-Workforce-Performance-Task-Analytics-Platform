"""
Test script to verify TaskLedger functionality
"""

from datetime import datetime, timedelta
from taskledger.database import init_db
from taskledger.models import Department, Team, Employee, Task, TimeEntry, TaskStatus
from taskledger.analytics import PerformanceAnalytics

def test_taskledger():
    """Test TaskLedger core functionality"""
    
    print("=" * 60)
    print("TaskLedger System Test")
    print("=" * 60)
    
    # Initialize database
    db = init_db('sqlite:///test_taskledger.db')
    session = db.get_session()
    
    try:
        # Test 1: Query departments
        print("\n1. Testing Department Queries:")
        departments = session.query(Department).all()
        print(f"   Found {len(departments)} departments")
        for dept in departments:
            print(f"   - {dept.name}: {dept.description}")
        
        # Test 2: Query teams
        print("\n2. Testing Team Queries:")
        teams = session.query(Team).all()
        print(f"   Found {len(teams)} teams")
        for team in teams:
            print(f"   - {team.name} (Department: {team.department.name})")
        
        # Test 3: Query employees
        print("\n3. Testing Employee Queries:")
        employees = session.query(Employee).all()
        print(f"   Found {len(employees)} employees")
        for emp in employees:
            print(f"   - {emp.first_name} {emp.last_name} ({emp.position})")
            print(f"     Email: {emp.email}")
            print(f"     Department: {emp.department.name}")
            if emp.team:
                print(f"     Team: {emp.team.name}")
        
        # Test 4: Query tasks
        print("\n4. Testing Task Queries:")
        tasks = session.query(Task).all()
        print(f"   Found {len(tasks)} tasks")
        for task in tasks:
            print(f"   - {task.title}")
            print(f"     Status: {task.status.value}, Priority: {task.priority.value}")
            if task.assigned_to_employee:
                print(f"     Assigned to: {task.assigned_to_employee.first_name} {task.assigned_to_employee.last_name}")
            print(f"     Estimated: {task.estimated_hours}h, Actual: {task.actual_hours}h")
        
        # Test 5: Query time entries
        print("\n5. Testing Time Entry Queries:")
        time_entries = session.query(TimeEntry).all()
        print(f"   Found {len(time_entries)} time entries")
        total_hours = sum(entry.duration_hours for entry in time_entries if entry.duration_hours)
        print(f"   Total tracked hours: {total_hours:.2f}h")
        
        # Test 6: Analytics
        print("\n6. Testing Analytics:")
        if employees:
            analytics = PerformanceAnalytics(session)
            
            # Calculate date range
            end_date = datetime.now()
            start_date = end_date - timedelta(days=60)
            
            # Employee analytics
            for emp in employees[:2]:  # Test first 2 employees
                print(f"\n   Employee: {emp.first_name} {emp.last_name}")
                summary = analytics.get_employee_performance_summary(
                    emp.id, start_date, end_date
                )
                if summary:
                    print(f"   - Total tasks: {summary['task_statistics']['total_tasks']}")
                    print(f"   - Completed tasks: {summary['task_statistics']['completed_tasks']}")
                    print(f"   - Completion rate: {summary['task_statistics']['completion_rate']}%")
                    print(f"   - Total hours: {summary['time_statistics']['total_hours']}h")
                    print(f"   - Task hours: {summary['time_statistics']['task_hours']}h")
        
        # Test 7: Task status distribution
        print("\n7. Testing Task Status Distribution:")
        for status in TaskStatus:
            count = session.query(Task).filter(Task.status == status).count()
            print(f"   - {status.value}: {count} tasks")
        
        # Test 8: Team analytics
        print("\n8. Testing Team Analytics:")
        if teams:
            analytics = PerformanceAnalytics(session)
            for team in teams[:2]:  # Test first 2 teams
                end_date = datetime.now()
                start_date = end_date - timedelta(days=60)
                summary = analytics.get_team_performance_summary(
                    team.id, start_date, end_date
                )
                if summary:
                    print(f"\n   Team: {team.name}")
                    print(f"   - Team size: {summary['team_size']}")
                    print(f"   - Total tasks: {summary['task_statistics']['total_tasks']}")
                    print(f"   - Completion rate: {summary['task_statistics']['completion_rate']}%")
        
        print("\n" + "=" * 60)
        print("All tests completed successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\nError during testing: {e}")
        import traceback
        traceback.print_exc()
    finally:
        session.close()


if __name__ == "__main__":
    test_taskledger()
