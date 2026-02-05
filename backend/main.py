from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse
import os
from pathlib import Path
from dotenv import load_dotenv
import requests
from PIL import Image
import io
import base64
import json
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(
    title="TrashCollector AI API",
    description="Vision-based waste classification API",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen3-vl:235b-cloud")
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5MB
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}

# Waste categories
WASTE_CATEGORIES = [
    "Wet",
    "Dry",
    "Plastic",
    "Metal",
    "Glass",
    "E-Waste",
    "Hazardous",
    "Unknown"
]

# Category color mapping
CATEGORY_COLORS = {
    "Wet": "#2ecc71",      # Green
    "Dry": "#3498db",      # Blue
    "Plastic": "#f1c40f",  # Yellow
    "Metal": "#95a5a6",    # Gray
    "Glass": "#1abc9c",    # Teal
    "E-Waste": "#9b59b6",  # Purple
    "Hazardous": "#e74c3c", # Red
    "Unknown": "#7f8c8d"   # Neutral
}


def validate_image(file: UploadFile) -> bool:
    """Validate image file"""
    if file.size and file.size > MAX_IMAGE_SIZE:
        raise HTTPException(status_code=400, detail="Image size exceeds 5MB limit")
    
    ext = file.filename.split('.')[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Unsupported format. Allowed: {ALLOWED_EXTENSIONS}")
    
    return True


def resize_image(image_bytes: bytes, max_size: int = 1024) -> bytes:
    """Resize image for inference"""
    try:
        img = Image.open(io.BytesIO(image_bytes))
        img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
        output = io.BytesIO()
        img.save(output, format="PNG")
        return output.getvalue()
    except Exception as e:
        logger.error(f"Image resize error: {e}")
        return image_bytes


def parse_model_response(response_text: str) -> dict:
    """Parse and validate model response"""
    try:
        # Try to extract JSON from response
        json_str = response_text.strip()
        if json_str.startswith("```"):
            json_str = json_str.split("```")[1]
            if json_str.startswith("json"):
                json_str = json_str[4:]
        
        result = json.loads(json_str)
        
        # Validate category
        category = result.get("category", "Unknown")
        if category not in WASTE_CATEGORIES:
            category = "Unknown"
        
        result["category"] = category
        result["color"] = CATEGORY_COLORS.get(category, CATEGORY_COLORS["Unknown"])
        result["confidence"] = result.get("confidence", "Medium")
        
        return result
    except json.JSONDecodeError:
        logger.error(f"Failed to parse model response: {response_text}")
        return {
            "object": "Unable to identify",
            "category": "Unknown",
            "color": CATEGORY_COLORS["Unknown"],
            "confidence": "Low",
            "instruction": "Please try with a clearer image"
        }


async def classify_with_ollama(image_base64: str) -> dict:
    """Classify waste using Ollama vision model"""
    try:
        prompt = """You are a waste segregation assistant.

Analyze the image and:
1. Identify the object
2. Classify it into one waste category
3. Respond in JSON format

Allowed categories:
Wet, Dry, Plastic, Metal, Glass, E-Waste, Hazardous, Unknown

Respond ONLY in valid JSON with no additional text. Example format:
{
  "object": "Plastic water bottle",
  "category": "Plastic",
  "confidence": "High",
  "instruction": "Dispose in plastic recycling bin"
}"""
        
        # Use requests to call Ollama API
        response = requests.post(
            f"{OLLAMA_HOST}/api/generate",
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "images": [image_base64],
                "stream": False,
                "options": {
                    "temperature": 0.3,
                    "top_p": 0.9
                }
            },
            timeout=120
        )
        
        response.raise_for_status()
        data = response.json()
        model_text = data.get("response", "")
        logger.info(f"Model response: {model_text}")
        
        return parse_model_response(model_text)
    
    except requests.exceptions.ConnectionError:
        logger.error(f"Cannot connect to Ollama at {OLLAMA_HOST}")
        raise HTTPException(
            status_code=503,
            detail=f"Ollama service not available at {OLLAMA_HOST}. Make sure Ollama is running."
        )
    
    except Exception as e:
        logger.error(f"Ollama classification error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Classification failed: {str(e)}"
        )


@app.get("/")
async def root():
    """API health check"""
    return {
        "name": "TrashCollector AI API",
        "version": "1.0.0",
        "status": "active"
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model": OLLAMA_MODEL,
        "categories": WASTE_CATEGORIES
    }


@app.post("/classify")
async def classify_waste(file: UploadFile = File(...)):
    """Classify waste from image"""
    try:
        # Validate image
        validate_image(file)
        
        # Read image
        image_bytes = await file.read()
        
        # Resize for inference
        resized_image = resize_image(image_bytes)
        
        # Convert to base64
        image_base64 = base64.b64encode(resized_image).decode("utf-8")
        
        # Classify with Ollama
        result = await classify_with_ollama(image_base64)
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "data": result
            }
        )
    
    except HTTPException as e:
        return JSONResponse(
            status_code=e.status_code,
            content={"success": False, "error": e.detail}
        )
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": "Internal server error"}
        )


@app.get("/categories")
async def get_categories():
    """Get all waste categories with colors"""
    return {
        "categories": [
            {
                "name": cat,
                "color": CATEGORY_COLORS[cat],
                "examples": get_category_examples(cat)
            }
            for cat in WASTE_CATEGORIES
        ]
    }


def get_category_examples(category: str) -> list:
    """Get example items for a category"""
    examples_map = {
        "Wet": ["Food scraps", "Fruit peels", "Vegetable waste"],
        "Dry": ["Paper", "Cardboard", "Newspaper"],
        "Plastic": ["Bottles", "Bags", "Wrappers"],
        "Metal": ["Cans", "Foil", "Metal utensils"],
        "Glass": ["Bottles", "Jars", "Glasses"],
        "E-Waste": ["Batteries", "Chargers", "Old electronics"],
        "Hazardous": ["Chemical bottles", "Medical waste"],
        "Unknown": ["Mixed items", "Unclear objects"]
    }
    return examples_map.get(category, [])


# Serve React frontend static files
frontend_build_dir = Path(__file__).parent.parent / "frontend" / "build"
if frontend_build_dir.exists():
    app.mount("/", StaticFiles(directory=str(frontend_build_dir), html=True), name="static")
    logger.info(f"Serving React frontend from {frontend_build_dir}")
else:
    logger.warning(f"Frontend build directory not found at {frontend_build_dir}")
    logger.info("API-only mode. Frontend not available.")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000
    )
