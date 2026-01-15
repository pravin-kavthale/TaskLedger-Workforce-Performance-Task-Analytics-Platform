from setuptools import setup, find_packages

setup(
    name="taskledger",
    version="1.0.0",
    description="TaskLedger - Workforce Performance & Task Analytics Platform",
    author="TaskLedger Team",
    packages=find_packages(),
    install_requires=[
        "Flask>=3.0.0",
        "SQLAlchemy>=2.0.23",
        "python-dateutil>=2.8.2",
        "psycopg2-binary>=2.9.9",
    ],
    python_requires=">=3.8",
)
