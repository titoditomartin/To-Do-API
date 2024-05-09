from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from uuid import UUID, uuid4
from typing import List, Optional

app = FastAPI()

class TodoItem(BaseModel):
    id: UUID
    text: str
    completed: bool
    status: str
    user: str

class UpdateTodoItem(BaseModel):
    text: Optional[str]
    completed: Optional[bool]
    status: Optional[str]

# Dummy data for demonstration
todos = {
    UUID("8ffadce6-60d4-431f-afdb-3c53aac9d3c1"): TodoItem(id=UUID("8ffadce6-60d4-431f-afdb-3c53aac9d3c1"), text="Sleeping", completed=False, status="pending", user="example@example.com"),
    UUID("33d1f1c4-1ce4-46f5-9b88-dc42b86a0083"): TodoItem(id=UUID("33d1f1c4-1ce4-46f5-9b88-dc42b86a0083"), text="Singing", completed=True, status="completed", user="example@example.com")
}

@app.get("/todo/get")
def get_todos():
    return {"Todos": list(todos.values())}

@app.get("/todo/get/user")
def get_todos_by_user(user_email: str):
    filtered_todos = [todo for todo in todos.values() if todo.user == user_email]
    return {"Todos": filtered_todos}

@app.get("/todo/get/{todo_id}")
def get_todo(todo_id: UUID):
    todo = todos.get(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo item not found")
    return {"Todo": todo}

@app.post("/todo/post")
def add_todo(todo: TodoItem):
    todos[todo.id] = todo
    return {"Todo": todo}

@app.delete("/todo/delete/{todo_id}")
def delete_todo(todo_id: UUID):
    if todo_id in todos:
        del todos[todo_id]
        return {"Success": True, "Message": "Todo item deleted successfully"}
    else:
        return {"Success": False, "Message": "Todo item not found"}

@app.put("/todo/put/{todo_id}")
def update_todo(todo_id: UUID, todo_data: UpdateTodoItem):
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail="Todo item not found")
    if todo_data.text:
        todos[todo_id].text = todo_data.text
    if todo_data.completed is not None:
        todos[todo_id].completed = todo_data.completed
    if todo_data.status:
        todos[todo_id].status = todo_data.status
    return {"Success": True, "Message": "Todo item updated successfully", "Todo": todos[todo_id]}
