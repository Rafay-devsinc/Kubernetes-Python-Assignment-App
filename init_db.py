#!/usr/bin/env python3
"""
Database initialization script for the Docker Assignment App.
This script creates all database tables.
"""

from app import app, db

def init_database():
    """Initialize the database by creating all tables."""
    with app.app_context():
        # Create all tables
        db.create_all()
        print("✅ Database tables created successfully!")
        print("📊 You can now run the application with: python app.py")

if __name__ == "__main__":
    init_database()
