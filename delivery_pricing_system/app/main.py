import uuid
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from graph import compiled_graph
from models import async_session, Request, User, Escalation, init_db
import asyncio
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()

import pathlib

app.mount("/static", StaticFiles(directory=str(pathlib.Path(__file__).parent.parent / "static")), name="static")

@app.get("/")
async def read_root():
    return FileResponse(str(pathlib.Path(__file__).parent.parent / "index.html"))

class PriceRequest(BaseModel):
    material_type: str
    distance: Optional[float] = None  # optional, will calculate
    urgency: str
    weight: float
    location_type: str
    origin: str = "New York, NY"
    destination: str = "Los Angeles, CA"

@app.on_event("startup")
async def startup():
    await init_db()

@app.post("/calculate_price")
async def calculate_price(req: PriceRequest):
    ticket_id = f"D-{uuid.uuid4().hex[:6].upper()}"
    user_id = 1  # placeholder, assume user exists
    inputs = req.dict()
    state = {
        "ticket_id": ticket_id,
        "user_id": user_id,
        "inputs": inputs,
        "price_attempts": 0,
        "action_log": []
    }
    try:
        result = await compiled_graph.ainvoke(state)
    except Exception as e:
        # On failure, escalation
        result = state
        result["action_log"].append(f"Workflow failed: {str(e)}")
        # Save escalation
        async with async_session() as session:
            escalation = Escalation(request_id=None, error_message=str(e))
            session.add(escalation)
            await session.commit()

    # Save request
    async with async_session() as session:
        request = Request(
            ticket_id=ticket_id,
            user_id=user_id,
            inputs=inputs,
            total_price=result.get("total_price"),
            action_log=result.get("action_log", []),
            price_attempts=result.get("price_attempts", 0)
        )
        session.add(request)
        await session.commit()

    return result

# Optional: endpoint to create user
@app.post("/users")
async def create_user(name: str, email: str, phone: str):
    async with async_session() as session:
        user = User(name=name, email=email, phone=phone)
        session.add(user)
        await session.commit()
        return {"user_id": user.id}
