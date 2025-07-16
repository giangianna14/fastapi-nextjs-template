from fastapi import APIRouter, Depends, HTTPException, status
from app.core.security import get_current_user

router = APIRouter(prefix="/user", tags=["user"])

@router.get("/")
def list_users():
    return ["user1", "user2"]

@router.get("/protected")
def protected_route(current_user=Depends(get_current_user)):
    return {"user": current_user}
