from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Пустой список пользователей
users = []

# Объект для работы с шаблонами
templates = Jinja2Templates(directory="templates")

# Модель данных пользователя
class User(BaseModel):
    id: int
    username: str
    age: int

# Маршрут для отображения всех пользователей
@app.get("/", response_class=HTMLResponse)
async def read_users(request: Request):
    return templates.TemplateResponse("users.html", {"request": request, "users": users})

# Маршрут для получения пользователя по id
@app.get("/users/{user_id}", response_class=HTMLResponse)
async def read_user(request: Request, user_id: int):
    user = next((user for user in users if user.id == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return templates.TemplateResponse("user.html", {"request": request, "user": user})

# Маршрут для создания нового пользователя
@app.post("/user/{username}/{age}")
async def create_user(username: str, age: int):
    user_id = users[-1].id + 1 if users else 1
    user = User(id=user_id, username=username, age=age)
    users.append(user)
    return user

# Маршрут для обновления существующего пользователя
@app.put("/user/{user_id}/{username}/{age}")
async def update_user(user_id: int, username: str, age: int):
    user = next((user for user in users if user.id == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.username = username
    user.age = age
    return user

# Маршрут для удаления пользователя
@app.delete("/user/{user_id}")
async def delete_user(user_id: int):
    user = next((user for user in users if user.id == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    users.remove(user)
    return user


