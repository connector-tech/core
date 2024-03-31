from fastapi import Response, status


async def health():
    return Response(status_code=status.HTTP_200_OK)
