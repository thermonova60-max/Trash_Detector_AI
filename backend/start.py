"""Simple FastAPI app runner without reload issues"""
import os
import sys

# Add backend to path
sys.path.insert(0, os.path.dirname(__file__))

from main import app
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
