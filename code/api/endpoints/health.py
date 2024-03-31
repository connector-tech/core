from fastapi import APIRouter, Response, status


router = APIRouter(prefix="/health", tags=["health"])


@router.get("/")
async def health():
    return Response(status_code=status.HTTP_200_OK)
