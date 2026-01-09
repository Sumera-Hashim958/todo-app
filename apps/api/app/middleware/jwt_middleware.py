"""JWT authentication middleware and dependency"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session, select
from typing import Optional

from ..database import get_session
from ..models.user import User
from ..services.auth_service import decode_access_token


# HTTP Bearer token security scheme
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session)
) -> User:
    """
    Dependency to get the current authenticated user from JWT token

    Args:
        credentials: HTTP Authorization header with Bearer token
        session: Database session

    Returns:
        User object if authenticated

    Raises:
        HTTPException: 401 if token is invalid or user not found
    """
    # Extract token
    token = credentials.credentials

    # Decode token
    payload = decode_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Extract user_id from token payload (JWT spec uses string for sub)
    user_id_str: Optional[str] = payload.get("sub")

    if user_id_str is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Convert to integer for database lookup
    try:
        user_id = int(user_id_str)
    except (ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user ID in token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Get user from database
    user = session.get(User, user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False)),
    session: Session = Depends(get_session)
) -> Optional[User]:
    """
    Optional dependency to get current user if token is present

    Returns None if no token is provided instead of raising an error

    Args:
        credentials: Optional HTTP Authorization header
        session: Database session

    Returns:
        User object if authenticated, None otherwise
    """
    if credentials is None:
        return None

    token = credentials.credentials
    payload = decode_access_token(token)

    if payload is None:
        return None

    user_id_str: Optional[str] = payload.get("sub")

    if user_id_str is None:
        return None

    # Convert to integer for database lookup
    try:
        user_id = int(user_id_str)
    except (ValueError, TypeError):
        return None

    user = session.get(User, user_id)
    return user
