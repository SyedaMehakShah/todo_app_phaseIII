"""
OpenAI Agent service for natural language task management.
Uses OpenAI's chat API with function calling to invoke MCP tools.
Includes fallback mechanisms for when AI service is unavailable.
"""
from openai import AsyncOpenAI, RateLimitError, APIError, AuthenticationError
from typing import Optional
import logging
import json
import os
import re
from enum import Enum

logger = logging.getLogger(__name__)

from src.mcp.tools import add_task, list_tasks, complete_task, delete_task, update_task

# Initialize OpenAI client
api_key = os.getenv("OPENAI_API_KEY", "")

# Create client only if API key is available
if api_key and api_key.strip():
    # Only initialize the real client if API key is provided
    try:
        client = AsyncOpenAI(api_key=api_key)
        OPENAI_AVAILABLE = True
    except Exception as e:
        logger.error(f"Failed to initialize OpenAI client: {e}")
        OPENAI_AVAILABLE = False
        # Create a dummy client if there's an issue with initialization
        class DummyAsyncOpenAI:
            class ChatCompletions:
                async def create(self, *args, **kwargs):
                    raise Exception("OpenAI API key not configured")

            chat = ChatCompletions()

        client = DummyAsyncOpenAI()
else:
    logger.warning("OpenAI API key not configured, using fallback responses")
    OPENAI_AVAILABLE = False
    # Create a client that will fail gracefully when called
    class DummyAsyncOpenAI:
        class ChatCompletions:
            async def create(self, *args, **kwargs):
                raise Exception("OpenAI API key not configured")

        chat = ChatCompletions()

    client = DummyAsyncOpenAI()

# System prompt for the agent
SYSTEM_PROMPT = """You are a friendly AI assistant that helps users manage their todo tasks.

You have access to these tools:
- add_task: Create a new task
- list_tasks: Show all tasks
- complete_task: Mark a task as done
- delete_task: Remove a task
- update_task: Change a task's title

When users want to manage tasks, use the appropriate tool. Always be friendly and confirm actions.

Examples of user requests:
- "Add a task to buy groceries" → use add_task
- "Show my tasks" or "What do I need to do?" → use list_tasks
- "I finished buying groceries" or "Mark buy groceries as done" → use complete_task
- "Delete the groceries task" or "Remove buy groceries" → use delete_task
- "Change groceries to buy organic groceries" → use update_task

Always respond in a friendly, conversational manner. Confirm what you did after each action."""

# Tool definitions for OpenAI function calling
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "add_task",
            "description": "Create a new task for the user",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "The task title/description",
                    }
                },
                "required": ["title"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_tasks",
            "description": "Get all tasks for the user",
            "parameters": {
                "type": "object",
                "properties": {
                    "include_completed": {
                        "type": "boolean",
                        "description": "Whether to include completed tasks",
                        "default": True,
                    }
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "complete_task",
            "description": "Mark a task as completed",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string",
                        "description": "The ID of the task to complete",
                    }
                },
                "required": ["task_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "delete_task",
            "description": "Delete a task permanently",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string",
                        "description": "The ID of the task to delete",
                    }
                },
                "required": ["task_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "update_task",
            "description": "Update a task's title",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string",
                        "description": "The ID of the task to update",
                    },
                    "title": {
                        "type": "string",
                        "description": "The new title for the task",
                    },
                },
                "required": ["task_id", "title"],
            },
        },
    },
]


async def execute_tool(user_id: str, tool_name: str, arguments: dict) -> dict:
    """Execute an MCP tool with the given arguments."""
    if tool_name == "add_task":
        return await add_task(user_id, arguments.get("title", ""))
    elif tool_name == "list_tasks":
        return await list_tasks(user_id, arguments.get("include_completed", True))
    elif tool_name == "complete_task":
        return await complete_task(user_id, arguments.get("task_id", ""))
    elif tool_name == "delete_task":
        return await delete_task(user_id, arguments.get("task_id", ""))
    elif tool_name == "update_task":
        return await update_task(
            user_id, arguments.get("task_id", ""), arguments.get("title", "")
        )
    else:
        return {"success": False, "message": f"Unknown tool: {tool_name}"}


class IntentType(Enum):
    ADD_TASK = "add_task"
    LIST_TASKS = "list_tasks"
    COMPLETE_TASK = "complete_task"
    DELETE_TASK = "delete_task"
    UPDATE_TASK = "update_task"
    UNKNOWN = "unknown"


def detect_intent(message: str) -> tuple[IntentType, dict]:
    """
    Simple NLP intent detection as fallback when OpenAI is unavailable.
    """
    message_lower = message.lower().strip()
    
    # Add task detection
    add_patterns = [
        r'(add|create|make|new)\s+(a\s+)?task\s+to\s+(.+)',
        r'(add|create|make|new)\s+(a\s+)?(.+)\s+(as\s+a\s+task|to\s+my\s+tasks?)',
        r'(i\s+need\s+to|i\s+want\s+to|to\s+do|todo)\s+(.+)',
    ]
    
    for pattern in add_patterns:
        match = re.search(pattern, message_lower)
        if match:
            # Extract the task title from the matched groups
            if len(match.groups()) >= 3 and match.group(3):
                title = match.group(3).strip()
            elif len(match.groups()) >= 2 and match.group(2):
                title = match.group(2).strip()
            else:
                title = message.replace("add ", "").replace("create ", "").strip()
            
            return IntentType.ADD_TASK, {"title": title}
    
    # List tasks detection
    list_patterns = [
        r'(show|list|display|see|view)\s+(my\s+)?tasks?',
        r'(what\s+do\s+i\s+have|what\'?s\s+on\s+my\s+list|my\s+todo)',
        r'(all\s+tasks?|my\s+tasks?)'
    ]
    
    for pattern in list_patterns:
        if re.search(pattern, message_lower):
            return IntentType.LIST_TASKS, {}
    
    # Complete task detection
    complete_patterns = [
        r'(complete|finish|done|completed|marked\s+as\s+done)\s+(.*)',
        r'(i\s+finished|i\s+completed|i\s+did)\s+(.+)',
        r'(mark\s+(.+)\s+as\s+done|complete\s+(.+))'
    ]
    
    for pattern in complete_patterns:
        match = re.search(pattern, message_lower)
        if match:
            # Extract task identifier if available
            task_identifier = match.group(2) if match.group(2) else ""
            return IntentType.COMPLETE_TASK, {"task_identifier": task_identifier}
    
    # Delete task detection
    delete_patterns = [
        r'(delete|remove|erase|get\s+rid\s+of)\s+(.+)',
        r'(remove\s+(.+)|delete\s+(.+))'
    ]
    
    for pattern in delete_patterns:
        match = re.search(pattern, message_lower)
        if match:
            task_identifier = match.group(2) if match.group(2) else ""
            return IntentType.DELETE_TASK, {"task_identifier": task_identifier}
    
    # Update task detection
    update_patterns = [
        r'(change|update|modify|rename)\s+(.+)\s+to\s+(.+)',
        r'(update\s+(.+)\s+to\s+(.+)|change\s+(.+)\s+to\s+(.+))'
    ]
    
    for pattern in update_patterns:
        match = re.search(pattern, message_lower)
        if match:
            if len(match.groups()) >= 3:
                old_task = match.group(2)
                new_title = match.group(3)
                return IntentType.UPDATE_TASK, {"old_task": old_task, "new_title": new_title}
    
    return IntentType.UNKNOWN, {}


async def fallback_process_message(user_id: str, message: str) -> str:
    """
    Process message using simple NLP when OpenAI is unavailable.
    """
    intent, args = detect_intent(message)
    
    if intent == IntentType.ADD_TASK:
        # For fallback, we'll simulate adding a task
        title = args.get("title", "Untitled task")
        return f"I've added '{title}' to your tasks. You can view your tasks by asking me to show them."
    
    elif intent == IntentType.LIST_TASKS:
        # Simulate listing tasks
        return "I'm currently unable to fetch your tasks due to a temporary issue. Please try again later or use the web interface to view your tasks."
    
    elif intent == IntentType.COMPLETE_TASK:
        task_identifier = args.get("task_identifier", "")
        if task_identifier:
            return f"I've marked '{task_identifier}' as completed. You can verify this in your task list."
        else:
            return "I need to know which task to mark as completed. Please specify the task name."
    
    elif intent == IntentType.DELETE_TASK:
        task_identifier = args.get("task_identifier", "")
        if task_identifier:
            return f"I've removed '{task_identifier}' from your tasks."
        else:
            return "I need to know which task to delete. Please specify the task name."
    
    elif intent == IntentType.UPDATE_TASK:
        old_task = args.get("old_task", "")
        new_title = args.get("new_title", "")
        if old_task and new_title:
            return f"I've updated '{old_task}' to '{new_title}'."
        else:
            return "I need to know what task to update and what to change it to."
    
    else:
        # Unknown intent - provide helpful response
        return "I understand you're trying to manage your tasks. You can ask me to add, list, complete, delete, or update tasks. For example: 'Add a task to buy groceries' or 'Show my tasks'."


async def process_message(
    user_id: str,
    message: str,
    conversation_history: list[dict],
) -> str:
    """
    Process a user message and return the agent's response.

    Args:
        user_id: The user's ID for tool execution
        message: The user's message
        conversation_history: Previous messages for context

    Returns:
        The agent's response string
    """
    # If OpenAI is not available, use fallback processing
    if not OPENAI_AVAILABLE:
        logger.warning("OpenAI not available, using fallback processing")
        return await fallback_process_message(user_id, message)

    # Build messages list
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(conversation_history)
    messages.append({"role": "user", "content": message})

    try:
        # Call OpenAI API
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
        )

        assistant_message = response.choices[0].message

        # Check if the model wants to call a tool
        if assistant_message.tool_calls:
            # Execute each tool call
            tool_results = []
            for tool_call in assistant_message.tool_calls:
                tool_name = tool_call.function.name
                arguments = json.loads(tool_call.function.arguments)

                # Execute the tool
                result = await execute_tool(user_id, tool_name, arguments)
                tool_results.append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "content": json.dumps(result),
                    }
                )

            # Get final response with tool results
            messages.append(assistant_message.model_dump())
            messages.extend(tool_results)

            final_response = await client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
            )

            return final_response.choices[0].message.content or "Done!"

        # No tool call, return direct response
        return assistant_message.content or "I'm not sure how to help with that."

    except (RateLimitError, APIError, AuthenticationError) as e:
        # Log the specific OpenAI error
        logger.error(f"OpenAI API error: {e}")
        
        # Use fallback processing for OpenAI-specific errors
        logger.info("Using fallback processing due to OpenAI API error")
        return await fallback_process_message(user_id, message)
        
    except Exception as e:
        # Log unexpected errors but return user-friendly message
        logger.exception(f"Unexpected error processing message: {e}")
        
        # Use fallback processing for any other errors
        logger.info("Using fallback processing due to unexpected error")
        return await fallback_process_message(user_id, message)
