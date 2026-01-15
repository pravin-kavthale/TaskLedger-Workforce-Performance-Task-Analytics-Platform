"""
Main entry point for running TaskLedger API server
"""

import os
from taskledger.api import create_app

if __name__ == '__main__':
    app = create_app()
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() in ('true', '1', 'yes')
    
    print("Starting TaskLedger API server on http://0.0.0.0:5000")
    print("\nAvailable endpoints:")
    print("  - GET  /health - Health check")
    print("  - GET  /api/departments - List departments")
    print("  - GET  /api/teams - List teams")
    print("  - GET  /api/employees - List employees")
    print("  - GET  /api/tasks - List tasks")
    print("  - GET  /api/time-entries - List time entries")
    print("  - GET  /api/analytics/employee/<id> - Employee analytics")
    print("\nSee README.md for complete API documentation\n")
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
