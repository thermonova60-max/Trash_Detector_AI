# API Documentation

## Base URL
```
http://localhost:8000
```

## Endpoints

### 1. Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "model": "qwen3-vl:235b-cloud",
  "categories": ["Wet", "Dry", "Plastic", "Metal", "Glass", "E-Waste", "Hazardous", "Unknown"]
}
```

### 2. Get Root Info
```http
GET /
```

**Response:**
```json
{
  "name": "TrashCollector AI API",
  "version": "1.0.0",
  "status": "active"
}
```

### 3. Get All Categories
```http
GET /categories
```

**Response:**
```json
{
  "categories": [
    {
      "name": "Wet",
      "color": "#2ecc71",
      "examples": ["Food scraps", "Fruit peels", "Vegetable waste"]
    },
    {
      "name": "Dry",
      "color": "#3498db",
      "examples": ["Paper", "Cardboard", "Newspaper"]
    },
    ...
  ]
}
```

### 4. Classify Waste
```http
POST /classify
Content-Type: multipart/form-data
```

**Parameters:**
- `file` (required): Image file (JPG, PNG, WEBP)
- Maximum size: 5MB

**Example using cURL:**
```bash
curl -X POST \
  -F "file=@path/to/image.jpg" \
  http://localhost:8000/classify
```

**Success Response (200):**
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

**Error Response (400/500):**
```json
{
  "success": false,
  "error": "Error message"
}
```

## Response Fields

| Field | Type | Description |
|-------|------|-------------|
| object | string | Identified waste object |
| category | string | Waste category (Wet, Dry, Plastic, etc.) |
| color | string | Hex color code for category |
| confidence | string | Confidence level (High, Medium, Low) |
| instruction | string | Disposal instruction |

## Category Reference

| Category | Color | Use Case |
|----------|-------|----------|
| Wet | #2ecc71 | Food scraps, organic waste |
| Dry | #3498db | Paper, cardboard |
| Plastic | #f1c40f | Bottles, bags, wrappers |
| Metal | #95a5a6 | Cans, foil, metal items |
| Glass | #1abc9c | Bottles, jars, glass items |
| E-Waste | #9b59b6 | Batteries, chargers, electronics |
| Hazardous | #e74c3c | Chemical waste, medical waste |
| Unknown | #7f8c8d | Unable to classify |

## Rate Limiting

No rate limiting applied. For production deployments, consider implementing:
- Request throttling
- API key authentication
- Usage quotas

## CORS Policy

Currently allows all origins (`*`). For production, update in `backend/main.py`:
```python
allow_origins=["https://yourdomain.com"]
```

## Error Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 400 | Bad request (invalid image format/size) |
| 500 | Server error (Ollama connection, processing) |

## Testing

### Python
```python
import requests

url = "http://localhost:8000/classify"
with open("image.jpg", "rb") as f:
    files = {"file": f}
    response = requests.post(url, files=files)
    print(response.json())
```

### JavaScript
```javascript
const formData = new FormData();
formData.append('file', imageFile);

fetch('http://localhost:8000/classify', {
  method: 'POST',
  body: formData
})
.then(res => res.json())
.then(data => console.log(data));
```

### cURL
```bash
curl -X POST -F "file=@test.jpg" http://localhost:8000/classify
```

## Performance Notes

- Response time: 5-30 seconds (depending on model and image size)
- Concurrent requests: Limited by system resources
- GPU acceleration: Significantly improves performance
- Batch processing: Not yet implemented (planned feature)
