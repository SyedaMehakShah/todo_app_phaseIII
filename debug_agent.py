"""
Debug the agent processing
"""
import asyncio
import sys
import os

# Add the backend directory to the path so imports work
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from src.services.agent import process_message

async def debug_agent():
    print("Testing agent processing...")
    try:
        result = await process_message(
            user_id="052d18ef-25e0-4cb1-9dcd-56bd37335589",
            message="Add a task to buy groceries",
            conversation_history=[]
        )
        print(f"Success! Result: {result}")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(debug_agent())