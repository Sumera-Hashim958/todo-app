"""WebSocket Connection Manager for Real-time Updates"""
from typing import Dict, List
from fastapi import WebSocket
import json
import logging

logger = logging.getLogger(__name__)


class ConnectionManager:
    """Manage WebSocket connections and broadcast updates"""

    def __init__(self):
        # user_id -> list of active connections
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, user_id: str):
        """Accept a new WebSocket connection"""
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        self.active_connections[user_id].append(websocket)
        logger.info(f"WebSocket connected for user {user_id}")

    def disconnect(self, websocket: WebSocket, user_id: str):
        """Remove a WebSocket connection"""
        if user_id in self.active_connections:
            if websocket in self.active_connections[user_id]:
                self.active_connections[user_id].remove(websocket)
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]
        logger.info(f"WebSocket disconnected for user {user_id}")

    async def send_personal_message(self, message: dict, user_id: str):
        """Send a message to all connections of a specific user"""
        if user_id not in self.active_connections:
            return

        message_json = json.dumps(message)
        disconnected = []

        for connection in self.active_connections[user_id]:
            try:
                await connection.send_text(message_json)
            except Exception as e:
                logger.error(f"Error sending message to user {user_id}: {e}")
                disconnected.append(connection)

        # Clean up disconnected connections
        for connection in disconnected:
            self.disconnect(connection, user_id)

    async def broadcast_to_user(self, user_id: str, event_type: str, data: dict):
        """Broadcast an event to all connections of a user"""
        message = {
            "type": event_type,
            "data": data
        }
        await self.send_personal_message(message, user_id)


# Global connection manager instance
manager = ConnectionManager()
