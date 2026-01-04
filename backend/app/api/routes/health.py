from fastapi import APIRouter

router = APIRouter(tags=["Health"])

@router.get("/api/health")
async def health_check():
    """API health check."""
    return {"status": "healthy", "service": "SocratesAI"}
