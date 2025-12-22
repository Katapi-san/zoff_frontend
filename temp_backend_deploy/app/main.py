from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base

from app.routers import staff, stores, tags, customers, reservations

# Create database tables
try:
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully")
except Exception as e:
    print(f"Error creating database tables: {e}")


app = FastAPI(title="Zoff Scope API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(staff.router)
app.include_router(stores.router)
app.include_router(tags.router)
app.include_router(customers.router)
app.include_router(reservations.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Zoff Scope API"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

import os
import subprocess
import sys

@app.post("/api/dev/reset-data")
def reset_data():
    try:
        # backend/app/main.py -> backend/
        current_dir = os.path.dirname(os.path.abspath(__file__))
        backend_root = os.path.dirname(current_dir)
        script_path = os.path.join(backend_root, "create_customer_data.py")
        
        if not os.path.exists(script_path):
            return {"status": "error", "message": f"Script not found at {script_path}"}
            
        # Run script with backend root as CWD to ensure imports work
        result = subprocess.run(
            [sys.executable, script_path], 
            cwd=backend_root,
            capture_output=True, 
            text=True
        )
        
        if result.returncode == 0:
            return {"status": "success", "output": result.stdout}
        else:
            return {"status": "error", "message": result.stderr or result.stdout}
    except Exception as e:
        return {"status": "error", "detail": str(e)}
