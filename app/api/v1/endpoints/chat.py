from typing import List
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from datetime import datetime

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        # Map patient_id to list of websockets
        self.active_connections: dict[int, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, patient_id: int):
        await websocket.accept()
        if patient_id not in self.active_connections:
            self.active_connections[patient_id] = []
        self.active_connections[patient_id].append(websocket)

    def disconnect(self, websocket: WebSocket, patient_id: int):
        if patient_id in self.active_connections:
            self.active_connections[patient_id].remove(websocket)

    async def broadcast(self, message: str, patient_id: int):
        if patient_id in self.active_connections:
            for connection in self.active_connections[patient_id]:
                await connection.send_text(message)

manager = ConnectionManager()

@router.websocket("/ws/{patient_id}")
async def websocket_endpoint(websocket: WebSocket, patient_id: int):
    """
    Real-time Chat and System Logs.
    Connects to a specific Patient's channel.
    """
    await manager.connect(websocket, patient_id)
    try:
        while True:
            data = await websocket.receive_text()
            # In a real app, we would parse JSON, validate User token, and store message in DB.
            # Here we just echo to the room with a timestamp.
            timestamp = datetime.now().strftime("%H:%M")
            await manager.broadcast(f"[{timestamp}] User: {data}", patient_id)
    except WebSocketDisconnect:
        manager.disconnect(websocket, patient_id)
        # await manager.broadcast(f"Client left the chat", patient_id)
