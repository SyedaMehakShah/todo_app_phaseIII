"""
Test just the conversation history function
"""
import asyncio
import sys
import os

# Add the backend directory to the path so imports work
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from src.services.conversation import get_conversation_history

async def test_conversation_history():
    print("Testing conversation history function...")
    user_id = "052d18ef-25e0-4cb1-9dcd-56bd37335589"
    
    try:
        history = await get_conversation_history(user_id, limit=20)
        print(f"History length: {len(history)}")
        print(f"Sample history item: {history[0] if history else 'None'}")
        print("✓ Conversation history function works!")
    except Exception as e:
        print(f"✗ Error in conversation history: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_conversation_history())