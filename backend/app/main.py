from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import chat, health
from app.config import settings

app = FastAPI(
    title="SocratesAI API",
    version="1.0.0",
    description="Socratic Learning Platform Backend"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat.router)
app.include_router(health.router)

@app.get("/")
async def root():
    return {"status": "ok", "message": "SocratesAI Backend Running", "version": "1.0.0"}

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup."""
    print("SocratesAI Backend Starting...")
    pass

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    pass
