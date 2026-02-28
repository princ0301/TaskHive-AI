from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from db.database import init_db
from api.routes import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Starting up... Initializing database.")
    init_db()
    yield
    print("👋 Shutting down.")

app = FastAPI(
    title="Multi-Agent Research API",
    description="API to trigger AI research pipelines and retrieve generated reports.",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/")
def root():
    return {
        "message": "Multi-Agent Research API",
        "docs": "/docs",
        "version": "1.0.0"
    }


@app.get("/health")
def health():
    return {"status": "ok"}