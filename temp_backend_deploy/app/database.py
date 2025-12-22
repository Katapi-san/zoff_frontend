from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

import shutil
import logging

# Setup Logger for database module
logger = logging.getLogger("zoff_scope.database")

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Original DB Path
ORIGINAL_DB_PATH = os.path.join(BASE_DIR, '..', 'zoff_scope_v3.db')
# Temp DB Path for Azure (writable)
TEMP_DB_PATH = "/tmp/zoff_scope_v3.db"

# Check if running on Azure (simple check via file existence or env)
# Always try to copy to tmp if the original exists and we are not on Windows local dev
if os.path.exists(ORIGINAL_DB_PATH) and os.name != 'nt':
    try:
        logger.info(f"Copying DB from {ORIGINAL_DB_PATH} to {TEMP_DB_PATH}")
        shutil.copy2(ORIGINAL_DB_PATH, TEMP_DB_PATH)
        SQLALCHEMY_DATABASE_URL = f"sqlite:///{TEMP_DB_PATH}"
    except Exception as e:
        logger.error(f"Failed to copy DB to temp: {e}")
        # Fallback to original path
        SQLALCHEMY_DATABASE_URL = f"sqlite:///{ORIGINAL_DB_PATH}"
else:
    # Local Windows Dev or DB missing
    SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{ORIGINAL_DB_PATH}")

logger.info(f"Using Database URL: {SQLALCHEMY_DATABASE_URL}")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in SQLALCHEMY_DATABASE_URL else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
