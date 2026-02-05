# TrashCollector AI - Startup Guide

Smart Waste Segregation System using Vision AI

---

## Quick Start (3 Steps)

### Step 1: Start Ollama
```bash
ollama serve
```
Keep this terminal open.

### Step 2: Start the App
Open a **new terminal**:
```bash
cd backend
python app.py
```

### Step 3: Open Browser
Go to: **http://localhost:8000**

---

## First Time Setup

### Prerequisites
1. **Python 3.10+** - [Download](https://python.org)
2. **Ollama** - [Download](https://ollama.ai/download)

### Install the Vision Model
```bash
ollama pull qwen3-vl:235b-cloud
```

---

## Usage

1. Open http://localhost:8000
2. Click the upload area or drag & drop an image
3. Click **"Classify Waste"**
4. Get results:
   - Object identified
   - Waste category
   - Disposal instructions

---

## Waste Categories

| Category | Examples |
|----------|----------|
| 🟢 Wet | Food scraps, vegetables, fruit peels |
| 🔵 Dry | Paper, cardboard, cloth |
| 🟡 Plastic | Bottles, containers, wrappers |
| ⚪ Metal | Cans, foil, utensils |
| 🔵 Glass | Bottles, jars, mirrors |
| 🟣 E-Waste | Phones, batteries, cables |
| 🔴 Hazardous | Chemicals, medicines, paint |

---

## Troubleshooting

### "Ollama not running" error
Start Ollama first:
```bash
ollama serve
```

### Port 8000 already in use
Windows PowerShell:
```powershell
Get-NetTCPConnection -LocalPort 8000 | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force }
python app.py
```

### Model not found
```bash
ollama pull qwen3-vl:235b-cloud
```

### Slow first response
Normal! First request loads the model (30-60 seconds). Subsequent requests are faster.

---

## Configuration

Edit `backend/app.py`:
```python
PORT = 8000                              # Server port
OLLAMA_MODEL = "qwen3-vl:235b-cloud"     # Vision model
OLLAMA_HOST = "http://localhost:11434"   # Ollama address
```

---

## API

### POST /classify
Upload an image to classify waste.

```python
import requests

with open("trash.jpg", "rb") as f:
    r = requests.post("http://localhost:8000/classify", files={"file": f})
    print(r.json())
```

Response:
```json
{
  "success": true,
  "object": "Plastic bottle",
  "category": "Plastic",
  "color": "#f1c40f",
  "instruction": "Rinse and place in recycling bin"
}
```

---

## File Structure

```
Trash_Detector_AI/
├── backend/
│   └── app.py      # The entire application
└── STARTUP.md      # This guide
```

**That's it. One file. Pure Python.**
