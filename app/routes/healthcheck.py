"""
Simple endpoint for testing if the server works.
"""
from fastapi import APIRouter

router = APIRouter()

@router.get(
    "/ping",
    tags=["health-check"],
    responses={200: {"description": "Returns 'pong' as status check msg"}},
)
async def root():
    return {"message": "pong"}
