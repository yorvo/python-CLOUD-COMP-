from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import csv
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # This allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # This allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # This allows all headers
)

USERS_FILE = "users.csv"
TASKS_FILE = "tasks.csv"

class User(BaseModel):
    username: str
    password: str 

class Task(BaseModel):
    task: str
    deadline: str 
    user: str

# Ensure CSV files exist
def initialize_files():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["username", "password"])
    
    if not os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["task", "deadline", "user"])

initialize_files()

@app.post("/login/")
async def user_login(user: User):
    """
    Handles the user login process by checking stored credentials in users.csv.
    """
    with open(USERS_FILE, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["username"] == user.username and row["password"] == user.password:
                return {"status": "Logged in"}
    raise HTTPException(status_code=401, detail="Invalid username or password")

@app.post("/create_user/")
async def create_user(user: User):
    """
    Creates a new user by adding their username and password to users.csv.
    """
    with open(USERS_FILE, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["username"] == user.username:
                raise HTTPException(status_code=400, detail="User already exists")
    
    with open(USERS_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([user.username, user.password])
    
    return {"status": "User Created"}

@app.post("/create_task/")
async def create_task(task: Task):
    """
    Creates a new task by adding the task description, deadline, and user to tasks.csv.
    """
    with open(TASKS_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([task.task, task.deadline, task.user])
    
    return {"status": "Task Created"}

@app.get("/get_tasks/")
async def get_tasks(name: str):
    """
    Retrieves all tasks associated with a specific user from tasks.csv.
    """
    user_tasks = []
    with open(TASKS_FILE, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["user"] == name:
                user_tasks.append([row["task"], row["deadline"], row["user"]])
    
    return {"tasks": user_tasks}
