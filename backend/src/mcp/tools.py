"""
MCP Tool implementations for task management.
All tools are stateless and persist effects to PostgreSQL.
Constitution Principle V: Exactly 5 tools with no hidden parameters.
"""
from typing import Optional
from datetime import datetime
import uuid

from sqlmodel import select
from src.services.database import get_session
from src.models import Task


async def add_task(user_id: str, title: str) -> dict:
    """
    Create a new task for a user.

    Args:
        user_id: The ID of the user creating the task
        title: The task title/description (1-500 chars)

    Returns:
        dict with success status, task details, and message
    """
    if not title or len(title.strip()) == 0:
        return {
            "success": False,
            "task": None,
            "message": "Task title cannot be empty",
        }

    if len(title) > 500:
        return {
            "success": False,
            "task": None,
            "message": "Task title must be 500 characters or less",
        }

    async with get_session() as session:
        task = Task(
            id=str(uuid.uuid4()),
            user_id=user_id,
            title=title.strip(),
            completed=False,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        session.add(task)
        await session.commit()
        await session.refresh(task)

        return {
            "success": True,
            "task": {
                "id": task.id,
                "title": task.title,
                "completed": task.completed,
                "created_at": task.created_at.isoformat(),
            },
            "message": f"Task '{task.title}' created successfully",
        }


async def list_tasks(user_id: str, include_completed: bool = True) -> dict:
    """
    Retrieve all tasks for a user.

    Args:
        user_id: The ID of the user
        include_completed: Whether to include completed tasks (default: True)

    Returns:
        dict with success status, tasks list, count, and message
    """
    async with get_session() as session:
        query = select(Task).where(Task.user_id == user_id)
        if not include_completed:
            query = query.where(Task.completed == False)
        query = query.order_by(Task.created_at.desc())

        result = await session.exec(query)
        tasks = result.all()

        task_list = [
            {
                "id": task.id,
                "title": task.title,
                "completed": task.completed,
                "created_at": task.created_at.isoformat(),
            }
            for task in tasks
        ]

        count = len(task_list)
        if count == 0:
            message = "No tasks found"
        elif count == 1:
            message = "Found 1 task"
        else:
            message = f"Found {count} tasks"

        return {
            "success": True,
            "tasks": task_list,
            "count": count,
            "message": message,
        }


async def complete_task(user_id: str, task_id: str) -> dict:
    """
    Mark a task as completed.

    Args:
        user_id: The ID of the user
        task_id: The ID of the task to complete

    Returns:
        dict with success status, task details, and message
    """
    async with get_session() as session:
        query = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        result = await session.exec(query)
        task = result.first()

        if not task:
            return {
                "success": False,
                "task": None,
                "message": "Task not found",
            }

        task.completed = True
        task.updated_at = datetime.utcnow()
        session.add(task)
        await session.commit()
        await session.refresh(task)

        return {
            "success": True,
            "task": {
                "id": task.id,
                "title": task.title,
                "completed": task.completed,
            },
            "message": f"Task '{task.title}' marked as complete",
        }


async def delete_task(user_id: str, task_id: str) -> dict:
    """
    Remove a task permanently.

    Args:
        user_id: The ID of the user
        task_id: The ID of the task to delete

    Returns:
        dict with success status, deleted task ID, and message
    """
    async with get_session() as session:
        query = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        result = await session.exec(query)
        task = result.first()

        if not task:
            return {
                "success": False,
                "deleted_task_id": None,
                "message": "Task not found",
            }

        task_title = task.title
        await session.delete(task)
        await session.commit()

        return {
            "success": True,
            "deleted_task_id": task_id,
            "message": f"Task '{task_title}' deleted successfully",
        }


async def update_task(user_id: str, task_id: str, title: str) -> dict:
    """
    Modify an existing task's title.

    Args:
        user_id: The ID of the user
        task_id: The ID of the task to update
        title: The new task title (1-500 chars)

    Returns:
        dict with success status, updated task details, and message
    """
    if not title or len(title.strip()) == 0:
        return {
            "success": False,
            "task": None,
            "message": "Task title cannot be empty",
        }

    if len(title) > 500:
        return {
            "success": False,
            "task": None,
            "message": "Task title must be 500 characters or less",
        }

    async with get_session() as session:
        query = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        result = await session.exec(query)
        task = result.first()

        if not task:
            return {
                "success": False,
                "task": None,
                "message": "Task not found",
            }

        old_title = task.title
        task.title = title.strip()
        task.updated_at = datetime.utcnow()
        session.add(task)
        await session.commit()
        await session.refresh(task)

        return {
            "success": True,
            "task": {
                "id": task.id,
                "title": task.title,
                "completed": task.completed,
                "updated_at": task.updated_at.isoformat(),
            },
            "message": f"Task updated from '{old_title}' to '{task.title}'",
        }
