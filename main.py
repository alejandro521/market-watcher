from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List
import os

app = FastAPI()

# Pydantic models
class SignupRequest(BaseModel):
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

class AlertRequest(BaseModel):
    symbol: str
    target_price: float
    direction: str
    user_id: int

# In-memory storage
users = []
alerts = []

# Serve static files
app.mount("/static", StaticFiles(directory="."), name="static")

@app.get("/")
def home():
    return FileResponse("index.html")  # Serve index.html from current directory

# --- API endpoints ---
@app.post("/auth/signup")
def signup(request: SignupRequest):
    for user in users:
        if user["email"] == request.email:
            raise HTTPException(status_code=400, detail="Email already registered")
    user_id = len(users) + 1
    users.append({"id": user_id, "email": request.email, "password": request.password})
    return {"message": "Account created", "user_id": user_id}

@app.post("/auth/login")
def login(request: LoginRequest):
    for user in users:
        if user["email"] == request.email and user["password"] == request.password:
            return {"message": "Login OK", "user_id": user["id"]}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/alerts/add")
def add_alert(request: AlertRequest):
    if request.direction not in ["above", "below"]:
        raise HTTPException(status_code=400, detail="Direction must be 'above' or 'below'")
    alerts.append({
        "symbol": request.symbol,
        "target_price": request.target_price,
        "direction": request.direction,
        "user_id": request.user_id
    })
    return {"alert_created": request.symbol}

@app.get("/alerts/list/{user_id}")
def list_alerts(user_id: int):
    return {"alerts": [a for a in alerts if a["user_id"] == user_id]}



