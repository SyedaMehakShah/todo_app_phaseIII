"""
Google Gemini Agent service for natural language task management.
Uses Gemini's API with function calling to invoke MCP tools.
Includes fallback mechanisms for when AI service is unavailable.
"""
import google.generativeai as genai
from typing import Optional
import logging
import json
import os
import re
from enum import Enum

logger = logging.getLogger(__name__)

from src.mcp.tools import add_task, list_tasks, complete_task, delete_task, update_task

# Initialize Gemini client
api_key = os.getenv("GEMINI_API_KEY", "")

# Configure Gemini
if api_key and api_key.strip():
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        GEMINI_AVAILABLE = True
        logger.info("Gemini API initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize Gemini client: {e}")
        GEMINI_AVAILABLE = False
        model = None
else:
    logger.warning("Gemini API key not configured, using fallback responses")
    GEMINI_AVAILABLE = False
    model = None

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
- "Add a task to buy groceries" → use add_task with title "buy groceries"
- "Show my tasks" or "What do I need to do?" → use list_tasks
- "I finished buying groceries" or "Mark task 1 as done" → use complete_task
- "Delete task 1" or "Remove buy groceries" → use delete_task
- "Change task 1 to buy organic groceries" → use update_task

Always respond in a friendly, conversational manner. Confirm what you did after each action."""

# Tool definitions for Gemini function calling
TOOLS = [
    genai.protos.Tool(
        function_declarations=[
            genai.protos.FunctionDeclaration(
                name="add_task",
                description="Create a new task for the user",
                parameters=genai.protos.Schema(
                    type=genai.protos.Type.OBJECT,
                    properties={
                        "title": genai.protos.Schema(
                            type=genai.protos.Type.STRING,
                            description="The task title/description"
                        )
                    },
                    required=["title"]
                )
            ),
            genai.protos.FunctionDeclaration(
                name="list_tasks",
                description="Get all tasks for the user",
                parameters=genai.protos.Schema(
                    type=genai.protos.Type.OBJECT,
                    properties={
                        "include_completed": genai.protos.Schema(
                            type=genai.protos.Type.BOOLEAN,
                            description="Whether to include completed tasks"
                        )
                    }
                )
            ),
            genai.protos.FunctionDeclaration(
                name="complete_task",
                description="Mark a task as completed",
                parameters=genai.protos.Schema(
                    type=genai.protos.Type.OBJECT,
                    properties={
                        "task_id": genai.protos.Schema(
                            type=genai.protos.Type.STRING,
                            description="The ID of the task to complete"
                        )
                    },
                    required=["task_id"]
                )
            ),
            genai.protos.FunctionDeclaration(
                name="delete_task",
                description="Delete a task permanently",
                parameters=genai.protos.Schema(
                    type=genai.protos.Type.OBJECT,
                    properties={
                        "task_id": genai.protos.Schema(
                            type=genai.protos.Type.STRING,
                            description="The ID of the task to delete"
                        )
                    },
                    required=["task_id"]
                )
            ),
            genai.protos.FunctionDeclaration(
                name="update_task",
                description="Update a task's title",
                parameters=genai.protos.Schema(
                    type=genai.protos.Type.OBJECT,
                    properties={
                        "task_id": genai.protos.Schema(
                            type=genai.protos.Type.STRING,
                            description="The ID of the task to update"
                        ),
                        "title": genai.protos.Schema(
                            type=genai.protos.Type.STRING,
                            description="The new title for the task"
                        )
                    },
                    required=["task_id", "title"]
                )
            )
        ]
    )
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
    Simple NLP intent detection as fallback when Gemini is unavailable.
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

    return IntentType.UNKNOWN, {}


async def fallback_response(message: str, user_id: str) -> str:
    """
    Provide fallback responses when Gemini is unavailable.
    Uses simple pattern matching to attempt to handle common requests.
    """
    intent, args = detect_intent(message)

    if intent == IntentType.ADD_TASK:
        title = args.get("title", "")
        if title:
            result = await add_task(user_id, title)
            if result.get("success"):
                return f"I've added '{title}' to your tasks. You can view your tasks by asking me to show them."
            else:
                return f"I had trouble adding that task. {result.get('message', '')}"
        else:
            return "I understand you want to add a task, but I couldn't determine what the task should be. Please try again with more details."

    elif intent == IntentType.LIST_TASKS:
        result = await list_tasks(user_id, include_completed=True)
        if result.get("success"):
            tasks = result.get("tasks", [])
            if not tasks:
                return "You don't have any tasks yet. You can add one by saying 'Add a task to [task description]'."

            task_list = []
            for i, task in enumerate(tasks, 1):
                status = "✓" if task.get("completed") else " "
                task_list.append(f"{i}. [{status}] {task.get('title')}")

            return "Here are your tasks:\n" + "\n".join(task_list)
        else:
            return f"I'm currently unable to fetch your tasks. {result.get('message', '')}"

    else:
        return "I understand you're trying to manage your tasks. You can ask me to add, list, complete, delete, or update tasks. For example: 'Add a task to buy groceries' or 'Show my tasks'."


async def process_message(user_id: str, message: str, conversation_history: list = None) -> str:
    """
    Process a user message and return an AI-generated response.
    Uses Gemini with function calling when available, falls back to pattern matching otherwise.
    """
    if conversation_history is None:
        conversation_history = []

    try:
        if not GEMINI_AVAILABLE or model is None:
            logger.info("Gemini not available, using fallback processing")
            return await fallback_response(message, user_id)

        # Prepare conversation history for Gemini
        chat_history = []
        for msg in conversation_history[-10:]:  # Last 10 messages for context
            role = "user" if msg.get("role") == "user" else "model"
            chat_history.append({
                "role": role,
                "parts": [msg.get("content", "")]
            })

        # Start chat with history
        chat = model.start_chat(history=chat_history)

        # Send message with tools
        response = chat.send_message(
            f"{SYSTEM_PROMPT}\n\nUser: {message}",
            tools=TOOLS
        )

        # Handle function calls
        if response.candidates[0].content.parts:
            for part in response.candidates[0].content.parts:
                if hasattr(part, 'function_call') and part.function_call:
                    function_call = part.function_call
                    function_name = function_call.name
                    function_args = dict(function_call.args)

                    logger.info(f"Gemini function call: {function_name} with args {function_args}")

                    # Execute the tool
                    tool_result = await execute_tool(user_id, function_name, function_args)

                    # Send tool result back to Gemini
                    function_response = genai.protos.Part(
                        function_response=genai.protos.FunctionResponse(
                            name=function_name,
                            response={"result": tool_result}
                        )
                    )

                    # Get final response with tool result
                    final_response = chat.send_message(function_response)
                    return final_response.text

                # Regular text response
                elif hasattr(part, 'text') and part.text:
                    return part.text

        return response.text if response.text else "I processed your request."

    except Exception as e:
        logger.error(f"Gemini API error: {e}")
        logger.info("Using fallback processing due to Gemini API error")
        return await fallback_response(message, user_id)
