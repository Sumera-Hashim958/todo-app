"""FastAPI application with AI Chatbot endpoint"""
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from pydantic import BaseModel
from typing import Optional
import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from uuid import UUID, uuid4
from datetime import datetime

from .database import get_session, create_tables
from .models import Conversation, Message, Task
from .routers import auth, todos, websocket

load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="Todo AI Chatbot API")

# Register routers
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(websocket.router)

# CORS middleware
# Get allowed origins from environment or use defaults
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:5173,http://localhost:5174").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize OpenAI client
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Get environment variables
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")
AGENT_TEMPERATURE = float(os.getenv("AGENT_TEMPERATURE", "0.7"))
CONTEXT_MESSAGE_LIMIT = int(os.getenv("CONTEXT_MESSAGE_LIMIT", "20"))


# Pydantic models for API
class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None


class ChatResponse(BaseModel):
    conversation_id: str
    message: str
    tool_calls: list = []
    created_at: str


# Function definitions for OpenAI
def add_task_tool(text: str, user_id: str, conversation_id: str, session: Session, priority: str = "medium", tags: list = None, due_date: str = None, recurrence: str = None) -> dict:
    """Add a new task with optional priority, tags, due date, and recurrence"""
    try:
        import json
        from dateutil import parser

        # Parse due_date if provided
        parsed_due_date = None
        if due_date:
            try:
                parsed_due_date = parser.parse(due_date)
            except:
                pass

        task = Task(
            user_id=user_id,
            text=text,
            conversation_id=UUID(conversation_id),
            created_via="chat",
            priority=priority if priority in ["low", "medium", "high"] else "medium",
            tags=json.dumps(tags) if tags else None,
            due_date=parsed_due_date,
            recurrence=recurrence.lower() if recurrence and recurrence.lower() in ["daily", "weekly", "monthly"] else None
        )
        session.add(task)
        session.commit()
        session.refresh(task)
        return {
            "success": True,
            "task_id": str(task.id),
            "text": task.text,
            "priority": task.priority,
            "tags": tags,
            "due_date": parsed_due_date.isoformat() if parsed_due_date else None,
            "recurrence": task.recurrence,
            "message": f"Task created successfully"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def list_tasks_tool(user_id: str, session: Session, priority: str = None, tag: str = None, sort_by: str = None) -> dict:
    """List all tasks for a user with optional filtering and sorting"""
    try:
        import json
        from datetime import datetime

        query = select(Task).where(Task.user_id == user_id)

        # Filter by priority
        if priority and priority in ["low", "medium", "high"]:
            query = query.where(Task.priority == priority)

        # Apply sorting
        if sort_by == "priority":
            # Custom ordering: high, medium, low
            query = query.order_by(
                Task.priority.desc()  # This will sort alphabetically, we'll handle in Python
            )
        elif sort_by == "date":
            query = query.order_by(Task.created_at.desc())
        elif sort_by == "due_date":
            query = query.order_by(Task.due_date.asc())

        tasks = session.exec(query).all()

        # Filter by tag if specified
        if tag:
            tasks = [t for t in tasks if t.tags and tag in json.loads(t.tags)]

        # Custom priority sorting if requested
        if sort_by == "priority":
            priority_order = {"high": 0, "medium": 1, "low": 2}
            tasks = sorted(tasks, key=lambda t: priority_order.get(t.priority, 1))

        now = datetime.utcnow()

        return {
            "success": True,
            "tasks": [
                {
                    "id": str(task.id),
                    "text": task.text,
                    "completed": task.completed,
                    "priority": task.priority,
                    "tags": json.loads(task.tags) if task.tags else [],
                    "due_date": task.due_date.isoformat() if task.due_date else None,
                    "recurrence": task.recurrence,
                    "overdue": task.due_date < now if task.due_date and not task.completed else False
                }
                for task in tasks
            ]
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def complete_task_tool(task_id: str, user_id: str, session: Session) -> dict:
    """Mark a task as complete and handle recurring tasks

    Args:
        task_id: Either a UUID string or a task position number (e.g., "1", "2", etc.)
        user_id: The user ID
        session: Database session
    """
    try:
        from datetime import timedelta
        import json

        # Check if task_id is a position number (e.g., "1", "2")
        if task_id.isdigit():
            position = int(task_id) - 1  # Convert to 0-based index
            # Get all tasks for user
            all_tasks = session.exec(
                select(Task).where(Task.user_id == user_id).order_by(Task.created_at)
            ).all()
            if position < 0 or position >= len(all_tasks):
                return {"success": False, "error": f"Task position {task_id} not found"}
            task = all_tasks[position]
        else:
            # Try as UUID
            task = session.exec(
                select(Task).where(Task.id == UUID(task_id), Task.user_id == user_id)
            ).first()

        if not task:
            return {"success": False, "error": "Task not found"}

        task.completed = True
        session.add(task)
        session.commit()

        message = f"Task '{task.text}' marked as complete"

        # Handle recurring tasks - create a new instance
        if task.recurrence:
            new_due_date = None
            if task.due_date:
                if task.recurrence == "daily":
                    new_due_date = task.due_date + timedelta(days=1)
                elif task.recurrence == "weekly":
                    new_due_date = task.due_date + timedelta(weeks=1)
                elif task.recurrence == "monthly":
                    new_due_date = task.due_date + timedelta(days=30)

            # Create new recurring task
            new_task = Task(
                user_id=user_id,
                text=task.text,
                conversation_id=task.conversation_id,
                created_via=task.created_via,
                priority=task.priority,
                tags=task.tags,
                due_date=new_due_date,
                recurrence=task.recurrence,
                reminder_sent=False
            )
            session.add(new_task)
            session.commit()
            message += f" and rescheduled for {new_due_date.strftime('%Y-%m-%d') if new_due_date else 'next occurrence'}"

        return {"success": True, "message": message}
    except Exception as e:
        return {"success": False, "error": str(e)}


def delete_task_tool(task_id: str, user_id: str, session: Session) -> dict:
    """Delete a task

    Args:
        task_id: Either a UUID string or a task position number (e.g., "1", "2", etc.)
        user_id: The user ID
        session: Database session
    """
    try:
        # Check if task_id is a position number
        if task_id.isdigit():
            position = int(task_id) - 1
            all_tasks = session.exec(
                select(Task).where(Task.user_id == user_id).order_by(Task.created_at)
            ).all()
            if position < 0 or position >= len(all_tasks):
                return {"success": False, "error": f"Task position {task_id} not found"}
            task = all_tasks[position]
        else:
            task = session.exec(
                select(Task).where(Task.id == UUID(task_id), Task.user_id == user_id)
            ).first()

        if not task:
            return {"success": False, "error": "Task not found"}
        task_text = task.text
        session.delete(task)
        session.commit()
        return {"success": True, "message": f"Task '{task_text}' has been deleted"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def update_task_tool(task_id: str, new_text: str, user_id: str, session: Session) -> dict:
    """Update a task's text

    Args:
        task_id: Either a UUID string or a task position number (e.g., "1", "2", etc.)
        new_text: The new text for the task
        user_id: The user ID
        session: Database session
    """
    try:
        # Check if task_id is a position number
        if task_id.isdigit():
            position = int(task_id) - 1
            all_tasks = session.exec(
                select(Task).where(Task.user_id == user_id).order_by(Task.created_at)
            ).all()
            if position < 0 or position >= len(all_tasks):
                return {"success": False, "error": f"Task position {task_id} not found"}
            task = all_tasks[position]
        else:
            task = session.exec(
                select(Task).where(Task.id == UUID(task_id), Task.user_id == user_id)
            ).first()

        if not task:
            return {"success": False, "error": "Task not found"}
        old_text = task.text
        task.text = new_text
        session.add(task)
        session.commit()
        return {"success": True, "message": f"Task updated from '{old_text}' to '{new_text}'"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def set_priority_tool(task_id: str, priority: str, user_id: str, session: Session) -> dict:
    """Set priority for a task"""
    try:
        if priority not in ["low", "medium", "high"]:
            return {"success": False, "error": "Priority must be low, medium, or high"}
        task = session.exec(
            select(Task).where(Task.id == UUID(task_id), Task.user_id == user_id)
        ).first()
        if not task:
            return {"success": False, "error": "Task not found"}
        task.priority = priority
        session.add(task)
        session.commit()
        return {"success": True, "message": f"Task '{task.text}' priority set to {priority}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def add_tags_tool(task_id: str, tags: list, user_id: str, session: Session) -> dict:
    """Add tags to a task"""
    try:
        import json
        task = session.exec(
            select(Task).where(Task.id == UUID(task_id), Task.user_id == user_id)
        ).first()
        if not task:
            return {"success": False, "error": "Task not found"}
        existing_tags = json.loads(task.tags) if task.tags else []
        # Add new tags without duplicates
        for tag in tags:
            if tag not in existing_tags:
                existing_tags.append(tag)
        task.tags = json.dumps(existing_tags)
        session.add(task)
        session.commit()
        return {"success": True, "message": f"Tags added to task '{task.text}': {', '.join(tags)}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def search_tasks_tool(query: str, user_id: str, session: Session) -> dict:
    """Search tasks by keyword in text"""
    try:
        tasks = session.exec(
            select(Task).where(Task.user_id == user_id, Task.text.contains(query))
        ).all()
        import json
        return {
            "success": True,
            "tasks": [
                {
                    "id": str(task.id),
                    "text": task.text,
                    "completed": task.completed,
                    "priority": task.priority,
                    "tags": json.loads(task.tags) if task.tags else []
                }
                for task in tasks
            ],
            "count": len(tasks)
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def set_due_date_tool(task_id: str, due_date: str, user_id: str, session: Session) -> dict:
    """Set a due date for a task"""
    try:
        from dateutil import parser
        task = session.exec(
            select(Task).where(Task.id == UUID(task_id), Task.user_id == user_id)
        ).first()
        if not task:
            return {"success": False, "error": "Task not found"}

        # Parse the due date string
        task.due_date = parser.parse(due_date)
        session.add(task)
        session.commit()
        return {"success": True, "message": f"Due date set for task '{task.text}' to {task.due_date.strftime('%Y-%m-%d %H:%M')}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def set_recurrence_tool(task_id: str, recurrence: str, user_id: str, session: Session) -> dict:
    """Set recurrence pattern for a task"""
    try:
        task = session.exec(
            select(Task).where(Task.id == UUID(task_id), Task.user_id == user_id)
        ).first()
        if not task:
            return {"success": False, "error": "Task not found"}

        valid_recurrence = ["daily", "weekly", "monthly", "none"]
        if recurrence.lower() not in valid_recurrence:
            return {"success": False, "error": f"Invalid recurrence. Must be one of: {', '.join(valid_recurrence)}"}

        task.recurrence = None if recurrence.lower() == "none" else recurrence.lower()
        session.add(task)
        session.commit()

        if task.recurrence:
            return {"success": True, "message": f"Task '{task.text}' set to recur {task.recurrence}"}
        else:
            return {"success": True, "message": f"Recurrence removed from task '{task.text}'"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_upcoming_tasks_tool(user_id: str, session: Session, days: int = 7) -> dict:
    """Get tasks due in the next N days"""
    try:
        from datetime import datetime, timedelta
        import json

        now = datetime.utcnow()
        future = now + timedelta(days=days)

        tasks = session.exec(
            select(Task).where(
                Task.user_id == user_id,
                Task.completed == False,
                Task.due_date != None,
                Task.due_date <= future
            ).order_by(Task.due_date)
        ).all()

        return {
            "success": True,
            "tasks": [
                {
                    "id": str(task.id),
                    "text": task.text,
                    "due_date": task.due_date.isoformat() if task.due_date else None,
                    "overdue": task.due_date < now if task.due_date else False,
                    "priority": task.priority,
                    "tags": json.loads(task.tags) if task.tags else []
                }
                for task in tasks
            ],
            "count": len(tasks)
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


# OpenAI function calling tools
tools = [
    {
        "type": "function",
        "function": {
            "name": "add_task",
            "description": "Create a new task for the user with optional priority, tags, due date, and recurrence",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The task description"
                    },
                    "priority": {
                        "type": "string",
                        "enum": ["low", "medium", "high"],
                        "description": "Priority level (default: medium)"
                    },
                    "tags": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of tags/categories for the task"
                    },
                    "due_date": {
                        "type": "string",
                        "description": "Due date in natural language (e.g., 'tomorrow', '2026-01-15 14:00', 'next Friday')"
                    },
                    "recurrence": {
                        "type": "string",
                        "enum": ["daily", "weekly", "monthly"],
                        "description": "Recurrence pattern for repeating tasks"
                    }
                },
                "required": ["text"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_tasks",
            "description": "List all tasks for the user with optional filtering and sorting",
            "parameters": {
                "type": "object",
                "properties": {
                    "priority": {
                        "type": "string",
                        "enum": ["low", "medium", "high"],
                        "description": "Filter by priority level"
                    },
                    "tag": {
                        "type": "string",
                        "description": "Filter by tag/category"
                    },
                    "sort_by": {
                        "type": "string",
                        "enum": ["priority", "date"],
                        "description": "Sort tasks by priority or date"
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "complete_task",
            "description": "Mark a task as complete",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string",
                        "description": "The task identifier - can be either the full UUID OR the task position number (e.g., '1' for first task, '2' for second task)"
                    }
                },
                "required": ["task_id"]
            }
        }
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
                        "description": "The task identifier - can be either the full UUID OR the task position number (e.g., '1' for first task, '2' for second task)"
                    }
                },
                "required": ["task_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_task",
            "description": "Update the text of an existing task",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string",
                        "description": "The task identifier - can be either the full UUID OR the task position number (e.g., '1' for first task, '2' for second task)"
                    },
                    "new_text": {
                        "type": "string",
                        "description": "The new text for the task"
                    }
                },
                "required": ["task_id", "new_text"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "set_priority",
            "description": "Set the priority level for a task",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string",
                        "description": "The ID of the task"
                    },
                    "priority": {
                        "type": "string",
                        "enum": ["low", "medium", "high"],
                        "description": "Priority level to set"
                    }
                },
                "required": ["task_id", "priority"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "add_tags",
            "description": "Add tags/categories to a task",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string",
                        "description": "The ID of the task"
                    },
                    "tags": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of tags to add"
                    }
                },
                "required": ["task_id", "tags"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_tasks",
            "description": "Search for tasks by keyword",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search keyword to find in task text"
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "set_due_date",
            "description": "Set a due date for a task",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string",
                        "description": "The ID of the task"
                    },
                    "due_date": {
                        "type": "string",
                        "description": "Due date in natural language (e.g., 'tomorrow', '2026-01-15', 'next Monday')"
                    }
                },
                "required": ["task_id", "due_date"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "set_recurrence",
            "description": "Set or remove recurrence pattern for a task",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string",
                        "description": "The ID of the task"
                    },
                    "recurrence": {
                        "type": "string",
                        "enum": ["daily", "weekly", "monthly", "none"],
                        "description": "Recurrence pattern (use 'none' to remove)"
                    }
                },
                "required": ["task_id", "recurrence"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_upcoming_tasks",
            "description": "Get tasks due in the next N days",
            "parameters": {
                "type": "object",
                "properties": {
                    "days": {
                        "type": "integer",
                        "description": "Number of days to look ahead (default: 7)",
                        "default": 7
                    }
                },
                "required": []
            }
        }
    }
]


@app.on_event("startup")
def on_startup():
    """Create database tables on startup"""
    create_tables()


@app.get("/")
def root():
    """Root endpoint"""
    return {"message": "Todo AI Chatbot API", "version": "1.0.0"}


@app.post("/api/{user_id}/chat", response_model=ChatResponse)
def chat(
    user_id: str,
    request: ChatRequest,
    session: Session = Depends(get_session)
):
    """Chat endpoint for AI-powered todo management"""
    try:
        # Get or create conversation
        if request.conversation_id:
            conversation = session.get(Conversation, UUID(request.conversation_id))
            if not conversation or conversation.user_id != user_id:
                raise HTTPException(status_code=404, detail="Conversation not found")
        else:
            # Create new conversation
            conversation = Conversation(user_id=user_id)
            session.add(conversation)
            session.commit()
            session.refresh(conversation)

        # Load conversation history
        messages_from_db = session.exec(
            select(Message)
            .where(Message.conversation_id == conversation.id)
            .order_by(Message.created_at)
            .limit(CONTEXT_MESSAGE_LIMIT)
        ).all()

        # Build context for OpenAI
        messages = [
            {
                "role": "system",
                "content": """You are a helpful task management assistant. You help users manage their todo list using natural language.

SIMPLE TASK OPERATION INSTRUCTIONS:
When users say things like:
- "mark task 1 as done" or "complete the first task"
- "delete task 2" or "remove the second task"
- "update task 1 to buy groceries"

You can use the task POSITION NUMBER directly! Just pass "1", "2", "3", etc. as the task_id.

Examples:
- complete_task(task_id="1") - Marks first task as done
- delete_task(task_id="2") - Deletes second task
- update_task(task_id="1", new_text="new text") - Updates first task

You can also use full UUIDs if you have them, but position numbers are simpler and work great!

Available functions:
- add_task: Create new tasks
- list_tasks: Show all tasks
- complete_task: Mark task as complete (task_id can be position number or UUID)
- delete_task: Delete a task (task_id can be position number or UUID)
- update_task: Change task text (task_id can be position number or UUID)
- set_priority: Change task priority
- add_tags: Add tags to tasks
- search_tasks: Search for tasks by keyword
- set_due_date: Set due dates
- set_recurrence: Set recurring tasks
- get_upcoming_tasks: Show upcoming tasks"""
            }
        ]

        # Add conversation history with tool results
        for msg in messages_from_db:
            messages.append({"role": msg.role, "content": msg.content})
            # If assistant message had tool calls, add them to help AI remember task IDs
            if msg.role == "assistant" and msg.tool_calls:
                # Add tool results as a hidden system message for context
                tool_summary = []
                for tc in msg.tool_calls:
                    if tc["function"] == "list_tasks" and tc["result"].get("success"):
                        tasks = tc["result"]["tasks"]
                        for i, task in enumerate(tasks, 1):
                            tool_summary.append(f"Task {i} ID: {task['id']}")
                if tool_summary:
                    messages.append({
                        "role": "system",
                        "content": f"[Tool Results Reference - Use these IDs for operations]\n" + "\n".join(tool_summary)
                    })

        # Add current user message
        messages.append({"role": "user", "content": request.message})

        # Save user message
        user_message = Message(
            conversation_id=conversation.id,
            role="user",
            content=request.message
        )
        session.add(user_message)

        # Call OpenAI with function calling
        response = openai_client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=messages,
            tools=tools,
            temperature=AGENT_TEMPERATURE
        )

        assistant_message_content = ""
        tool_calls_made = []

        # Handle tool calls
        if response.choices[0].message.tool_calls:
            for tool_call in response.choices[0].message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)

                # Execute function
                if function_name == "add_task":
                    result = add_task_tool(
                        function_args["text"],
                        user_id,
                        str(conversation.id),
                        session,
                        priority=function_args.get("priority", "medium"),
                        tags=function_args.get("tags"),
                        due_date=function_args.get("due_date"),
                        recurrence=function_args.get("recurrence")
                    )
                    tool_calls_made.append({
                        "function": function_name,
                        "args": function_args,
                        "result": result
                    })
                    if result["success"]:
                        priority_msg = f" with {result['priority']} priority" if result.get('priority') != 'medium' else ""
                        tags_msg = f" tagged as {', '.join(result['tags'])}" if result.get('tags') else ""
                        due_msg = f" due {result.get('due_date', '')[:10]}" if result.get('due_date') else ""
                        recur_msg = f" (repeats {result.get('recurrence')})" if result.get('recurrence') else ""
                        assistant_message_content += f"I've added '{function_args['text']}' to your tasks{priority_msg}{tags_msg}{due_msg}{recur_msg}. "
                    else:
                        assistant_message_content += f"Sorry, I couldn't add that task: {result.get('error', 'Unknown error')}. "

                elif function_name == "list_tasks":
                    result = list_tasks_tool(
                        user_id,
                        session,
                        priority=function_args.get("priority"),
                        tag=function_args.get("tag"),
                        sort_by=function_args.get("sort_by")
                    )
                    tool_calls_made.append({
                        "function": function_name,
                        "args": function_args,
                        "result": result
                    })
                    if result["success"]:
                        tasks = result["tasks"]
                        if not tasks:
                            assistant_message_content += "You have no tasks yet. "
                        else:
                            assistant_message_content += f"You have {len(tasks)} task(s):\n"
                            for i, task in enumerate(tasks, 1):
                                status = "✓" if task["completed"] else "○"
                                priority_indicator = {"high": "🔴", "medium": "🟡", "low": "🟢"}[task.get("priority", "medium")]
                                tags_display = f" [{', '.join(task['tags'])}]" if task.get("tags") else ""
                                # Don't show ID in message - AI will get it from tool result
                                assistant_message_content += f"{i}. {status} {priority_indicator} {task['text']}{tags_display}\n"
                    else:
                        assistant_message_content += f"Sorry, I couldn't list your tasks: {result.get('error', 'Unknown error')}. "

                elif function_name == "complete_task":
                    result = complete_task_tool(
                        function_args["task_id"],
                        user_id,
                        session
                    )
                    tool_calls_made.append({
                        "function": function_name,
                        "args": function_args,
                        "result": result
                    })
                    if result["success"]:
                        assistant_message_content += result["message"] + " "
                    else:
                        assistant_message_content += f"Sorry, I couldn't complete that task: {result.get('error', 'Unknown error')}. "

                elif function_name == "delete_task":
                    result = delete_task_tool(
                        function_args["task_id"],
                        user_id,
                        session
                    )
                    tool_calls_made.append({
                        "function": function_name,
                        "args": function_args,
                        "result": result
                    })
                    if result["success"]:
                        assistant_message_content += result["message"] + " "
                    else:
                        assistant_message_content += f"Sorry, I couldn't delete that task: {result.get('error', 'Unknown error')}. "

                elif function_name == "update_task":
                    result = update_task_tool(
                        function_args["task_id"],
                        function_args["new_text"],
                        user_id,
                        session
                    )
                    tool_calls_made.append({
                        "function": function_name,
                        "args": function_args,
                        "result": result
                    })
                    if result["success"]:
                        assistant_message_content += result["message"] + " "
                    else:
                        assistant_message_content += f"Sorry, I couldn't update that task: {result.get('error', 'Unknown error')}. "

                elif function_name == "set_priority":
                    result = set_priority_tool(
                        function_args["task_id"],
                        function_args["priority"],
                        user_id,
                        session
                    )
                    tool_calls_made.append({
                        "function": function_name,
                        "args": function_args,
                        "result": result
                    })
                    if result["success"]:
                        assistant_message_content += result["message"] + " "
                    else:
                        assistant_message_content += f"Sorry, I couldn't set priority: {result.get('error', 'Unknown error')}. "

                elif function_name == "add_tags":
                    result = add_tags_tool(
                        function_args["task_id"],
                        function_args["tags"],
                        user_id,
                        session
                    )
                    tool_calls_made.append({
                        "function": function_name,
                        "args": function_args,
                        "result": result
                    })
                    if result["success"]:
                        assistant_message_content += result["message"] + " "
                    else:
                        assistant_message_content += f"Sorry, I couldn't add tags: {result.get('error', 'Unknown error')}. "

                elif function_name == "search_tasks":
                    result = search_tasks_tool(
                        function_args["query"],
                        user_id,
                        session
                    )
                    tool_calls_made.append({
                        "function": function_name,
                        "args": function_args,
                        "result": result
                    })
                    if result["success"]:
                        tasks = result["tasks"]
                        if not tasks:
                            assistant_message_content += f"No tasks found matching '{function_args['query']}'. "
                        else:
                            assistant_message_content += f"Found {result['count']} task(s) matching '{function_args['query']}':\n"
                            for i, task in enumerate(tasks, 1):
                                status = "✓" if task["completed"] else "○"
                                priority_indicator = {"high": "🔴", "medium": "🟡", "low": "🟢"}[task["priority"]]
                                assistant_message_content += f"{i}. {status} {priority_indicator} {task['text']}\n"
                    else:
                        assistant_message_content += f"Sorry, I couldn't search tasks: {result.get('error', 'Unknown error')}. "

                elif function_name == "set_due_date":
                    result = set_due_date_tool(
                        function_args["task_id"],
                        function_args["due_date"],
                        user_id,
                        session
                    )
                    tool_calls_made.append({
                        "function": function_name,
                        "args": function_args,
                        "result": result
                    })
                    if result["success"]:
                        assistant_message_content += result["message"] + " "
                    else:
                        assistant_message_content += f"Sorry, I couldn't set due date: {result.get('error', 'Unknown error')}. "

                elif function_name == "set_recurrence":
                    result = set_recurrence_tool(
                        function_args["task_id"],
                        function_args["recurrence"],
                        user_id,
                        session
                    )
                    tool_calls_made.append({
                        "function": function_name,
                        "args": function_args,
                        "result": result
                    })
                    if result["success"]:
                        assistant_message_content += result["message"] + " "
                    else:
                        assistant_message_content += f"Sorry, I couldn't set recurrence: {result.get('error', 'Unknown error')}. "

                elif function_name == "get_upcoming_tasks":
                    result = get_upcoming_tasks_tool(
                        user_id,
                        session,
                        days=function_args.get("days", 7)
                    )
                    tool_calls_made.append({
                        "function": function_name,
                        "args": function_args,
                        "result": result
                    })
                    if result["success"]:
                        tasks = result["tasks"]
                        if not tasks:
                            assistant_message_content += f"You have no tasks due in the next {function_args.get('days', 7)} days. "
                        else:
                            assistant_message_content += f"You have {result['count']} task(s) due soon:\n"
                            for i, task in enumerate(tasks, 1):
                                priority_indicator = {"high": "🔴", "medium": "🟡", "low": "🟢"}[task["priority"]]
                                overdue_flag = "⚠️ OVERDUE" if task["overdue"] else ""
                                due_date_str = task["due_date"][:10] if task["due_date"] else "No date"
                                assistant_message_content += f"{i}. {priority_indicator} {task['text']} - Due: {due_date_str} {overdue_flag}\n"
                    else:
                        assistant_message_content += f"Sorry, I couldn't get upcoming tasks: {result.get('error', 'Unknown error')}. "

        else:
            # No tool calls, use assistant's direct response
            assistant_message_content = response.choices[0].message.content

        # Save assistant message
        assistant_message = Message(
            conversation_id=conversation.id,
            role="assistant",
            content=assistant_message_content.strip(),
            tool_calls=tool_calls_made if tool_calls_made else None
        )
        session.add(assistant_message)

        # Update conversation timestamp
        conversation.updated_at = datetime.utcnow()
        session.add(conversation)

        session.commit()

        return ChatResponse(
            conversation_id=str(conversation.id),
            message=assistant_message_content.strip(),
            tool_calls=tool_calls_made,
            created_at=assistant_message.created_at.isoformat()
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
