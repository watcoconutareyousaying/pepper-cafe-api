from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/login")
def login():
    return {"message": "Login route"}
