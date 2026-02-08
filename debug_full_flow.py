"""
More comprehensive debug of the full chat flow
"""
import asyncio
import sys
import os

# Add the backend directory to the path so imports work
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from src.services.agent import process_message
from src.services.conversation import get_conversation_history, save_message, get_or_create_conversation

async def debug_full_flow():
    print("Testing full chat flow...")
    user_id = "052d18ef-25e0-4cb1-9dcd-56bd37335589"
    
    try:
        # Test conversation creation
        print("1. Creating/getting conversation...")
        conversation = await get_or_create_conversation(user_id)
        print(f"   Conversation ID: {conversation.id}")
        
        # Test getting history
        print("2. Getting conversation history...")
        history = await get_conversation_history(user_id, limit=20)
        print(f"   History length: {len(history)}")
        
        # Test saving user message
        print("3. Saving user message...")
        user_message = await save_message(user_id, "user", "Add a task to buy groceries")
        print(f"   Saved message ID: {user_message.id}")
        
        # Test agent processing
        print("4. Processing with agent...")
        response = await process_message(user_id, "Add a task to buy groceries", history)
        print(f"   Agent response: {response}")
        
        # Test saving assistant response
        print("5. Saving assistant response...")
        assistant_message = await save_message(user_id, "assistant", response)
        print(f"   Saved assistant message ID: {assistant_message.id}")
        
        print("\n✓ Full flow completed successfully!")
        
    except Exception as e:
        print(f"\n✗ Error in flow: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(debug_full_flow())