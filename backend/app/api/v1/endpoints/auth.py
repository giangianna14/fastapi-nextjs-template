from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from app.core.security import create_access_token
from app.services.user_service import authenticate_admin

router = APIRouter(prefix="/auth", tags=["auth"])

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

@router.post("/login", response_model=TokenResponse)
def login_admin(data: LoginRequest):
    user = authenticate_admin(data.username, data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    token = create_access_token({"sub": user.username, "role": "admin"})
    return {"access_token": token, "token_type": "bearer"}
