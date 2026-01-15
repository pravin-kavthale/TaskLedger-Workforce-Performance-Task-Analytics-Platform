"""
Database configuration and utilities for TaskLedger
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from taskledger.models import Base


class Database:
    """Database manager for TaskLedger"""
    
    def __init__(self, database_url='sqlite:///taskledger.db'):
        """
        Initialize database connection
        
        Args:
            database_url: SQLAlchemy database URL
        """
        self.engine = create_engine(database_url, echo=False)
        self.Session = scoped_session(sessionmaker(bind=self.engine))
    
    def create_all(self):
        """Create all tables"""
        Base.metadata.create_all(self.engine)
    
    def drop_all(self):
        """Drop all tables"""
        Base.metadata.drop_all(self.engine)
    
    def get_session(self):
        """Get a new database session"""
        return self.Session()
    
    def close_session(self):
        """Close the current session"""
        self.Session.remove()


# Global database instance
db = None


def init_db(database_url='sqlite:///taskledger.db'):
    """Initialize the global database instance"""
    global db
    db = Database(database_url)
    db.create_all()
    return db


def get_db():
    """Get the global database instance"""
    return db
