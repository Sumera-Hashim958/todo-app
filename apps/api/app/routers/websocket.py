"""WebSocket router for real-time updates"""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlmodel import Session
import logging

from ..database import get_session
from ..websocket_manager import manager
from ..middleware.jwt_middleware import decode_access_token

logger = logging.getLogger(__name__)

router = APIRouter()


@router.websocket("/ws/{user_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    user_id: str,
    session: Session = Depends(get_session)
):
    """
    WebSocket endpoint for real-time todo updates

    Connect with: ws://localhost:8000/ws/{user_id}?token=<jwt_token>
    """
    # Get token from query params
    token = websocket.query_params.get("token")

    if not token:
        await websocket.close(code=1008, reason="Missing token")
        return

    try:
        # Verify JWT token
        payload = decode_access_token(token)
        token_user_id = payload.get("sub")

        # Ensure user can only connect to their own channel
        if str(token_user_id) != str(user_id):
            await websocket.close(code=1008, reason="Unauthorized")
            return

        # Accept connection
        await manager.connect(websocket, user_id)

        try:
            # Send initial connection confirmation
            await manager.send_personal_message({
                "type": "connected",
                "data": {"message": "Connected to real-time updates"}
            }, user_id)

            # Keep connection alive and listen for messages
            while True:
                data = await websocket.receive_text()
                logger.info(f"Received from user {user_id}: {data}")

                # Echo back for now (can add ping/pong logic)
                await manager.send_personal_message({
                    "type": "pong",
                    "data": {"message": "Connection alive"}
                }, user_id)

        except WebSocketDisconnect:
            manager.disconnect(websocket, user_id)
            logger.info(f"User {user_id} disconnected")

    except Exception as e:
        logger.error(f"WebSocket error for user {user_id}: {e}")
        await websocket.close(code=1011, reason="Internal error")
