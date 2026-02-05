# Setup Instructions

## Development Environment

### 1. Install Required Tools

#### Python
- Download from [python.org](https://www.python.org/)
- Version: 3.10 or higher
- Windows: Use installer with "Add Python to PATH" option

#### Node.js
- Download from [nodejs.org](https://nodejs.org/)
- Version: 18 LTS or higher

#### Ollama
- Download from [ollama.ai](https://ollama.ai)
- Provides local LLM inference

#### Docker (Optional but Recommended)
- Download from [docker.com](https://docker.com)
- For containerized deployment

### 2. Backend Setup

```bash
cd backend
python -m venv venv
```

Activate virtual environment:
- **Windows:** `venv\Scripts\activate`
- **macOS/Linux:** `source venv/bin/activate`

Install dependencies:
```bash
pip install -r requirements.txt
```

### 3. Ollama Model Setup

Start Ollama service, then pull the model:
```bash
ollama pull qwen3-vl:235b-cloud
```

Verify model is loaded:
```bash
ollama list
```

### 4. Frontend Setup

```bash
cd frontend
npm install
```

### 5. Environment Configuration

Backend (.env):
```bash
cd backend
cp .env.example .env
# Edit .env with your configuration
```

### 6. Running the Application

**Terminal 1 - Ollama:**
```bash
ollama serve
```

**Terminal 2 - Backend:**
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
python main.py
```

**Terminal 3 - Frontend:**
```bash
cd frontend
npm start
```

Access at: `http://localhost:3000`

## Docker Setup

Build and run with Docker Compose:
```bash
cd docker
docker-compose up -d
```

Access:
- Frontend: `http://localhost:3000`
- Backend: `http://localhost:8000`
- Ollama: `http://localhost:11434`

## Verify Installation

```bash
# Backend health check
curl http://localhost:8000/health

# Test classification (with an image file)
curl -X POST -F "file=@test-image.jpg" http://localhost:8000/classify
```

## Troubleshooting

### Module not found error
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Port already in use
- Change port in `main.py` or `package.json`
- Or stop conflicting process

### Ollama not responding
- Ensure Ollama service is running
- Check `OLLAMA_HOST` environment variable
- Default: `http://localhost:11434`

## Model Alternatives

For different hardware:
- **High Performance:** `qwen3-vl:235b-cloud` (default)
- **Standard:** `qwen3-vl:7b`
- **Lightweight:** `qwen3-vl:3b`
- **Stable Fallback:** `qwen2.5-vl`

Change in `.env`:
```
OLLAMA_MODEL=qwen3-vl:235b-cloud
```

Then pull the model:
```bash
ollama pull qwen3-vl:235b-cloud
```
