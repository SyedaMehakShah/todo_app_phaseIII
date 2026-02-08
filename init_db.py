"""
Initialize the database tables
"""
import asyncio
import sys
import os

# Add the backend directory to the path so imports work
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from src.services.database import init_db

async def setup_database():
    print("Initializing database tables...")
    try:
        await init_db()
        print("Database tables created successfully!")
    except Exception as e:
        print(f"Error initializing database: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(setup_database())