# TrashCollector AI

Vision-based waste classification system for smart waste segregation.

## Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- Docker & Docker Compose
- Ollama (or Docker)

### 1. Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
```

Create `.env` from `.env.example`:
```bash
cp .env.example .env
```

Run backend:
```bash
python main.py
# or
uvicorn main:app --reload --port 8000
```

Backend will be available at: `http://localhost:8000`

### 2. Ollama Setup

**Option A: Docker (Recommended)**
```bash
docker run -d -p 11434:11434 ollama/ollama:latest
```

**Option B: Direct Installation**
Download from [ollama.ai](https://ollama.ai)

### 3. Pull the Vision Model

```bash
ollama pull qwen3-vl:235b-cloud
# or use qwen3-vl:3b or qwen3-vl:7b for lightweight systems
```

### 4. Frontend Setup

```bash
cd frontend
npm install
npm start
```

Frontend will be available at: `http://localhost:3000`

### 5. Test the API

```bash
# Health check
curl http://localhost:8000/health

# Get categories
curl http://localhost:8000/categories

# Classify waste (multipart form-data with image)
curl -X POST -F "file=@image.jpg" http://localhost:8000/classify
```

## Docker Compose (All-in-One)

```bash
cd docker
docker-compose up -d
```

This will start:
- Ollama: `http://localhost:11434`
- Backend: `http://localhost:8000`
- Frontend: `http://localhost:3000`

## Project Structure

```
.
├── backend/              # FastAPI inference server
│   ├── main.py          # API endpoints
│   ├── requirements.txt  # Python dependencies
│   ├── Dockerfile       # Container image
│   └── .env.example     # Environment template
├── frontend/            # React UI
│   ├── src/
│   │   ├── screens/     # UI screens (Capture, Result)
│   │   ├── App.js       # Main component
│   │   └── index.js     # Entry point
│   ├── package.json
│   ├── Dockerfile.dev
│   └── public/
├── docker/
│   └── docker-compose.yml
├── docs/
├── .vscode/
├── implementation.md     # Project specification
└── README.md
```

## API Endpoints

### Health Check
```
GET /health
```

### Get Categories
```
GET /categories
```

Returns all waste categories with colors and examples.

### Classify Waste
```
POST /classify
Content-Type: multipart/form-data

file: <image_file>
```

**Response:**
```json
{
  "success": true,
  "data": {
    "object": "Plastic water bottle",
    "category": "Plastic",
    "color": "#f1c40f",
    "confidence": "High",
    "instruction": "Dispose in plastic recycling bin"
  }
}
```

## Environment Variables

**Backend (.env):**
```
OLLAMA_MODEL=qwen3-vl:235b-cloud
OLLAMA_HOST=http://localhost:11434
MAX_IMAGE_SIZE=5242880
```

## Troubleshooting

### Ollama Connection Issues
- Ensure Ollama is running: `curl http://localhost:11434/api/tags`
- Update `OLLAMA_HOST` in `.env` if running on different machine

### Model Not Found
```bash
ollama list  # Check available models
ollama pull qwen3-vl:7b  # Pull the model
```

### Frontend API Errors
- Check CORS configuration in `backend/main.py`
- Ensure backend is running on `http://localhost:8000`
- Check browser console for detailed errors

### Image Upload Issues
- Maximum file size: 5MB
- Supported formats: JPG, PNG, WEBP
- Ensure image is readable and not corrupted

## Performance Tips

- Use `qwen3-vl:3b` for edge/low-resource systems
- Resize images before upload (auto-handled by backend)
- Cache results for repeated items
- Use GPU acceleration: Set `OLLAMA_GPU=1` if available

## Future Enhancements

- Multi-object detection
- Segment-based classification
- Mobile app (React Native)
- Local language support
- Smart bin integration
- Statistics dashboard

## License

MIT License - See LICENSE file

## Contributing

Contributions are welcome! Please submit pull requests or open issues for improvements.

---

**Version:** 1.0.0
**Last Updated:** February 2026
