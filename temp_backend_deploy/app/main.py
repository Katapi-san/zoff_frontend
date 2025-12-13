from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base

from app.routers import staff, stores, tags

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Zoff Scope API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(staff.router)
app.include_router(stores.router)
app.include_router(tags.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Zoff Scope API"}

@app.get("/health")
def health_check():
    return {"status": "ok"}
