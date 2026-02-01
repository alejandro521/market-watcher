from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# --- Pydantic Models ---

class SignupRequest(BaseModel):
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

class AlertRequest(BaseModel):
    symbol: str
    target_price: float
    direction: str  # "above" or "below"
    user_id: int

# --- In-memory storage (for MVP) ---
users = []
alerts = []

# --- Endpoints ---

@app.get("/")
def root():
    return {"status": "running"}

@app.post("/auth/signup")
def signup(request: SignupRequest):
    # Check if user exists
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
    # Validate direction
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
    user_alerts = [a for a in alerts if a["user_id"] == user_id]
    return {"alerts": user_alerts}
