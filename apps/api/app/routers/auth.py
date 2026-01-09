"""Authentication router with register, login, and logout endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from ..database import get_session
from ..models.user import User
from ..schemas.auth import (
    UserRegisterRequest,
    UserLoginRequest,
    AuthResponse,
    LogoutResponse,
    UserResponse
)
from ..services.auth_service import (
    hash_password,
    verify_password,
    create_access_token
)
from ..middleware.jwt_middleware import get_current_user


router = APIRouter(prefix="/api/auth", tags=["authentication"])


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def register(
    request: UserRegisterRequest,
    session: Session = Depends(get_session)
):
    """
    Register a new user account

    - Validates email format and password strength
    - Checks for duplicate email
    - Creates user with hashed password
    - Returns user data and JWT token
    """
    # Check if email already exists
    existing_user = session.exec(
        select(User).where(User.email == request.email)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "error": {
                    "code": "EMAIL_ALREADY_EXISTS",
                    "message": "Email already registered",
                    "details": {}
                }
            }
        )

    # Hash password
    hashed_password = hash_password(request.password)

    # Create new user
    new_user = User(
        email=request.email,
        hashed_password=hashed_password
    )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    # Create JWT token
    access_token = create_access_token(data={"sub": new_user.id})

    # Return user data and token
    return AuthResponse(
        user=UserResponse.model_validate(new_user),
        token=access_token
    )


@router.post("/login", response_model=AuthResponse)
async def login(
    request: UserLoginRequest,
    session: Session = Depends(get_session)
):
    """
    Authenticate user and receive JWT token

    - Validates email and password
    - Returns user data and JWT token
    - Returns 401 for invalid credentials (without revealing which field is incorrect)
    """
    # Get user by email
    user = session.exec(
        select(User).where(User.email == request.email)
    ).first()

    # Verify password
    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": {
                    "code": "INVALID_CREDENTIALS",
                    "message": "Invalid email or password",
                    "details": {}
                }
            }
        )

    # Create JWT token
    access_token = create_access_token(data={"sub": user.id})

    # Return user data and token
    return AuthResponse(
        user=UserResponse.model_validate(user),
        token=access_token
    )


@router.post("/logout", response_model=LogoutResponse)
async def logout(
    current_user: User = Depends(get_current_user)
):
    """
    Terminate user session

    - Client-side token deletion
    - Server-side token blacklist (Phase III feature)

    Note: In Phase II, logout is handled client-side by deleting the JWT token.
    Server-side token blacklisting will be added in Phase III.
    """
    return LogoutResponse(message="Logged out successfully")
