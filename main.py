from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Task Management System")


# Task model
class Task(BaseModel):
    title: str
    description: Optional[str] = ""
    completed: bool = False


# Temporary database
tasks = []
task_id = 1


@app.get("/")
def home():
    return {"message": "Task Management System API is working!"}


# Get all tasks
@app.get("/tasks")
def get_tasks():
    return tasks


# Create a task
@app.post("/tasks")
def create_task(task: Task):
    global task_id

    new_task = {
        "id": task_id,
        "title": task.title,
        "description": task.description,
        "completed": task.completed
    }

    tasks.append(new_task)
    task_id += 1

    return new_task


# Get one task
@app.get("/tasks/{id}")
def get_task(id: int):
    for task in tasks:
        if task["id"] == id:
            return task

    raise HTTPException(status_code=404, detail="Task not found")


# Update a task
@app.put("/tasks/{id}")
def update_task(id: int, task: Task):
    for existing_task in tasks:
        if existing_task["id"] == id:
            existing_task["title"] = task.title
            existing_task["description"] = task.description
            existing_task["completed"] = task.completed

            return existing_task

    raise HTTPException(status_code=404, detail="Task not found")


# Delete a task
@app.delete("/tasks/{id}")
def delete_task(id: int):
    for task in tasks:
        if task["id"] == id:
            tasks.remove(task)
            return {"message": "Task deleted successfully"}

    raise HTTPException(status_code=404, detail="Task not found")