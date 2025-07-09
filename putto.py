📂 putto.py

Buddhochain (พุทธโธเชน) - Minimal Prototype in a Single Python File

from fastapi import FastAPI, HTTPException, Depends from fastapi.middleware.cors import CORSMiddleware from pydantic import BaseModel from typing import List from datetime import datetime from uuid import uuid4

app = FastAPI()

--- CORS ---

app.add_middleware( CORSMiddleware, allow_origins=[""], allow_credentials=True, allow_methods=[""], allow_headers=["*"], )

--- In-memory Database (Example Only) ---

users_db = {} meditation_logs = [] karma_wallet = {}

--- Models ---

class User(BaseModel): username: str password: str

class MeditationLog(BaseModel): username: str minutes: int feeling: str

class KarmaTransfer(BaseModel): from_user: str to_user: str amount: int

--- Authentication Endpoints ---

@app.post("/auth/register") def register(user: User): if user.username in users_db: raise HTTPException(status_code=400, detail="Username already exists") users_db[user.username] = user.password karma_wallet[user.username] = 100  # Starting Karma return {"message": "Registered successfully", "karma": 100}

@app.post("/auth/login") def login(user: User): if users_db.get(user.username) != user.password: raise HTTPException(status_code=400, detail="Invalid credentials") return {"message": "Login successful", "karma": karma_wallet.get(user.username, 0)}

--- Meditation Log & Karma Reward ---

@app.post("/meditate") def meditate(log: MeditationLog): log_entry = { "id": str(uuid4()), "username": log.username, "minutes": log.minutes, "feeling": log.feeling, "timestamp": datetime.utcnow().isoformat() } meditation_logs.append(log_entry)

# Reward Karma: 1 karma per minute
karma_reward = log.minutes
karma_wallet[log.username] = karma_wallet.get(log.username, 0) + karma_reward

return {"message": "Meditation logged", "karma_reward": karma_reward, "total_karma": karma_wallet[log.username]}

@app.get("/meditations/{username}", response_model=List[dict]) def get_meditations(username: str): return [log for log in meditation_logs if log["username"] == username]

--- Karma Transfer (Simple Blockchain Concept) ---

@app.post("/karma/transfer") def transfer_karma(transfer: KarmaTransfer): if karma_wallet.get(transfer.from_user, 0) < transfer.amount: raise HTTPException(status_code=400, detail="Insufficient Karma")

karma_wallet[transfer.from_user] -= transfer.amount
karma_wallet[transfer.to_user] = karma_wallet.get(transfer.to_user, 0) + transfer.amount

return {"message": "Transfer successful", "from_user_karma": karma_wallet[transfer.from_user], "to_user_karma": karma_wallet[transfer.to_user]}

--- Karma Balance ---

@app.get("/karma/{username}") def get_karma(username: str): return {"username": username, "karma": karma_wallet.get(username, 0)}

--- Root ---

@app.get("/") def root(): return {"message": "Welcome to Buddhochain Prototype"}

--- Run: uvicorn putto:app --reload ---

