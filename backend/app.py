from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import requests
import base64
import cgi
from io import BytesIO

PORT = 8000
OLLAMA_MODEL = "gemma3:4b-cloud"  # Cloud model
OLLAMA_HOST = "http://localhost:11434"
MAX_IMAGE_SIZE = 512  # Resize images for speed

CATEGORY_COLORS = {
    "Wet": "linear-gradient(135deg, #059669 0%, #047857 100%)",
    "Dry": "linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%)",
    "Plastic": "linear-gradient(135deg, #f59e0b 0%, #d97706 100%)",
    "Metal": "linear-gradient(135deg, #6b7280 0%, #374151 100%)",
    "Glass": "linear-gradient(135deg, #14b8a6 0%, #0d9488 100%)",
    "E-Waste": "linear-gradient(135deg, #8b5cf6 0%, #6d28d9 100%)",
    "Hazardous": "linear-gradient(135deg, #ef4444 0%, #dc2626 100%)",
    "Biowaste": "linear-gradient(135deg, #84cc16 0%, #65a30d 100%)",
    "Sprays": "linear-gradient(135deg, #06b6d4 0%, #0891b2 100%)",
    "Unknown": "linear-gradient(135deg, #6b7280 0%, #1f2937 100%)"
}

HTML_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TrashCollector AI</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        :root {
            --primary: #16a34a;
            --secondary: #22c55e;
            --accent: #4ade80;
        }
        body {
            font-family: 'Segoe UI', Roboto, 'Helvetica Neue', sans-serif;
            background: linear-gradient(135deg, #064e3b 0%, #065f46 50%, #047857 100%);
            min-height: 100vh;
            padding: 20px;
            transition: background 0.6s ease;
            position: relative;
            overflow-x: hidden;
        }
        body::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: radial-gradient(circle at 20% 50%, rgba(22, 163, 74, 0.15) 0%, transparent 50%),
                        radial-gradient(circle at 80% 80%, rgba(34, 197, 94, 0.15) 0%, transparent 50%);
            pointer-events: none;
            z-index: -1;
        }
        .container {
            max-width: 850px;
            margin: 0 auto;
            background: linear-gradient(135deg, rgba(5, 46, 22, 0.85) 0%, rgba(6, 78, 59, 0.9) 100%);
            border-radius: 25px;
            box-shadow: 0 25px 50px rgba(0, 0, 0, 0.5), 0 0 1px rgba(255, 255, 255, 0.1) inset;
            overflow: hidden;
            border: 1px solid rgba(74, 222, 128, 0.2);
            backdrop-filter: blur(10px);
        }
        .header {
            background: linear-gradient(135deg, #16a34a 0%, #22c55e 100%);
            color: white;
            padding: 50px 40px;
            text-align: center;
            position: relative;
            overflow: hidden;
        }
        .header::before {
            content: '';
            position: absolute;
            top: -50%;
            right: -50%;
            width: 400px;
            height: 400px;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
            border-radius: 50%;
        }
        .header h1 { font-size: 42px; margin-bottom: 10px; font-weight: 800; letter-spacing: -1px; position: relative; z-index: 1; }
        .header p { opacity: 0.95; font-size: 16px; font-weight: 300; position: relative; z-index: 1; }
        .status-bar {
            background: linear-gradient(90deg, rgba(22, 163, 74, 0.15) 0%, rgba(34, 197, 94, 0.15) 100%);
            padding: 20px 30px;
            display: flex;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 15px;
            border-bottom: 1px solid rgba(74, 222, 128, 0.2);
            font-size: 14px;
        }
        .status-item { display: flex; gap: 10px; align-items: center; }
        .status-label { color: #86efac; font-weight: 500; }
        .status-value { font-weight: 700; color: #dcfce7; }
        .status-active { color: #10b981; font-weight: 800; }
        .content { padding: 50px 40px; }
        .upload-area {
            border: 2px dashed #16a34a;
            border-radius: 20px;
            padding: 70px 40px;
            text-align: center;
            background: linear-gradient(135deg, rgba(22, 163, 74, 0.1) 0%, rgba(34, 197, 94, 0.1) 100%);
            cursor: pointer;
            transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
        }
        .upload-area:hover {
            background: linear-gradient(135deg, rgba(22, 163, 74, 0.2) 0%, rgba(34, 197, 94, 0.2) 100%);
            border-color: #22c55e;
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(22, 163, 74, 0.3);
        }
        .upload-icon { font-size: 70px; margin-bottom: 20px; display: block; }
        .upload-text { font-size: 20px; color: #dcfce7; margin-bottom: 10px; font-weight: 600; }
        .upload-hint { font-size: 14px; color: #86efac; }
        #fileInput { display: none; }
        .btn {
            background: linear-gradient(135deg, #16a34a 0%, #22c55e 100%);
            color: white;
            border: none;
            padding: 16px 50px;
            font-size: 16px;
            font-weight: 700;
            border-radius: 50px;
            cursor: pointer;
            margin-top: 30px;
            transition: all 0.3s;
            box-shadow: 0 10px 30px rgba(22, 163, 74, 0.4);
        }
        .btn:hover:not(:disabled) { 
            transform: translateY(-3px);
            box-shadow: 0 15px 50px rgba(22, 163, 74, 0.6);
        }
        .btn:disabled { opacity: 0.5; cursor: not-allowed; }
        .preview { margin-top: 40px; text-align: center; }
        .preview img { max-width: 320px; max-height: 320px; border-radius: 20px; box-shadow: 0 20px 50px rgba(22, 163, 74, 0.4); }
        .result {
            margin-top: 40px;
            padding: 40px;
            background: linear-gradient(135deg, rgba(22, 163, 74, 0.15) 0%, rgba(34, 197, 94, 0.15) 100%);
            border-radius: 20px;
            display: none;
            border: 1px solid rgba(74, 222, 128, 0.3);
        }
        .result.show { display: block; animation: slideUp 0.6s cubic-bezier(0.34, 1.56, 0.64, 1); }
        @keyframes slideUp { from { opacity: 0; transform: translateY(30px); } to { opacity: 1; transform: translateY(0); } }
        .result-header { font-size: 12px; color: #86efac; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 12px; font-weight: 700; }
        .result-object { font-size: 28px; font-weight: 800; color: #f0fdf4; margin-bottom: 25px; }
        .result-category {
            display: inline-block;
            padding: 18px 40px;
            border-radius: 50px;
            color: white;
            font-size: 18px;
            font-weight: 700;
            margin-bottom: 25px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
            transition: all 0.3s;
        }
        .result-category:hover { transform: scale(1.05); }
        .result-instruction {
            background: rgba(5, 46, 22, 0.95);
            padding: 25px;
            border-radius: 15px;
            border-left: 5px solid #16a34a;
            font-size: 16px;
            color: #dcfce7;
            line-height: 1.6;
        }
        .categories {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(85px, 1fr));
            gap: 15px;
            margin-top: 40px;
            padding-top: 40px;
            border-top: 1px solid rgba(74, 222, 128, 0.2);
        }
        .category {
            padding: 20px 15px;
            border-radius: 15px;
            text-align: center;
            font-size: 12px;
            font-weight: 700;
            color: white;
            transition: all 0.3s;
            cursor: default;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        }
        .category:hover { transform: translateY(-5px); box-shadow: 0 15px 40px rgba(0, 0, 0, 0.4); }
        .loading { display: none; text-align: center; padding: 50px 40px; }
        .loading.show { display: block; }
        .spinner {
            width: 60px; height: 60px;
            border: 4px solid rgba(22, 163, 74, 0.2);
            border-top: 4px solid #16a34a;
            border-right: 4px solid #22c55e;
            border-radius: 50%;
            animation: spin 0.8s linear infinite;
            margin: 0 auto 20px;
        }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        .loading p { color: #dcfce7; font-weight: 600; }
        .error { 
            color: #fca5a5;
            background: linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(220, 38, 38, 0.1) 100%);
            padding: 18px;
            border-radius: 15px;
            margin-top: 20px;
            display: none;
            border-left: 4px solid #ef4444;
            font-weight: 600;
        }
        .error.show { display: block; animation: slideUp 0.4s; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>TrashCollector AI</h1>
            <p>Smart Waste Segregation System</p>
        </div>
        
        <div class="status-bar">
            <div class="status-item">
                <span class="status-label">Model:</span>
                <span class="status-value">gemma3:4b-cloud</span>
            </div>
            <div class="status-item">
                <span class="status-label">Status:</span>
                <span class="status-value status-active">Active</span>
            </div>
        </div>
        
        <div class="content">
            <div class="upload-area" id="uploadArea">
                <div class="upload-icon">📷</div>
                <div class="upload-text">Drop image here or click to upload</div>
                <div class="upload-hint">Supports: JPG, PNG, WEBP (max 5MB)</div>
                <input type="file" id="fileInput" accept="image/*">
            </div>
            
            <div class="preview" id="preview"></div>
            
            <div style="text-align: center;">
                <button class="btn" id="classifyBtn" disabled>Classify Waste</button>
            </div>
            
            <div class="loading" id="loading">
                <div class="spinner"></div>
                <p>Analyzing image with AI...</p>
            </div>
            
            <div class="error" id="error"></div>
            
            <div class="result" id="result">
                <div class="result-header">Object Identified</div>
                <div class="result-object" id="resultObject">-</div>
                <div class="result-header">Waste Category</div>
                <div class="result-category" id="resultCategory">-</div>
                <div class="result-header">Disposal Instructions</div>
                <div class="result-instruction" id="resultInstruction">-</div>
            </div>
            
            <div class="categories">
                <div class="category" style="background: linear-gradient(135deg, #059669 0%, #047857 100%)">🟢 Wet</div>
                <div class="category" style="background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%)">🔵 Dry</div>
                <div class="category" style="background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%)">🟡 Plastic</div>
                <div class="category" style="background: linear-gradient(135deg, #6b7280 0%, #374151 100%)">⚪ Metal</div>
                <div class="category" style="background: linear-gradient(135deg, #14b8a6 0%, #0d9488 100%)">🔷 Glass</div>
                <div class="category" style="background: linear-gradient(135deg, #8b5cf6 0%, #6d28d9 100%)">🟣 E-Waste</div>
                <div class="category" style="background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%)">🔴 Hazard</div>
                <div class="category" style="background: linear-gradient(135deg, #84cc16 0%, #65a30d 100%)">🌱 Bio</div>
                <div class="category" style="background: linear-gradient(135deg, #06b6d4 0%, #0891b2 100%)">💨 Sprays</div>
                <div class="category" style="background: linear-gradient(135deg, #6b7280 0%, #1f2937 100%)">⚫ Unknown</div>
            </div>
        </div>
    </div>
    
    <script>
        const categoryBgMap = {
            "Wet": "linear-gradient(135deg, #059669 0%, #047857 100%)",
            "Dry": "linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%)",
            "Plastic": "linear-gradient(135deg, #f59e0b 0%, #d97706 100%)",
            "Metal": "linear-gradient(135deg, #6b7280 0%, #374151 100%)",
            "Glass": "linear-gradient(135deg, #14b8a6 0%, #0d9488 100%)",
            "E-Waste": "linear-gradient(135deg, #8b5cf6 0%, #6d28d9 100%)",
            "Hazardous": "linear-gradient(135deg, #ef4444 0%, #dc2626 100%)",
            "Biowaste": "linear-gradient(135deg, #84cc16 0%, #65a30d 100%)",
            "Sprays": "linear-gradient(135deg, #06b6d4 0%, #0891b2 100%)",
            "Unknown": "linear-gradient(135deg, #6b7280 0%, #1f2937 100%)"
        };

        const uploadArea = document.getElementById('uploadArea');
        const fileInput = document.getElementById('fileInput');
        const preview = document.getElementById('preview');
        const classifyBtn = document.getElementById('classifyBtn');
        const loading = document.getElementById('loading');
        const error = document.getElementById('error');
        const result = document.getElementById('result');
        
        let selectedFile = null;
        
        uploadArea.addEventListener('click', () => fileInput.click());
        fileInput.addEventListener('change', (e) => { if (e.target.files.length) handleFile(e.target.files[0]); });
        
        function handleFile(file) {
            if (!file.type.startsWith('image/')) { showError('Please select an image file'); return; }
            if (file.size > 5 * 1024 * 1024) { showError('File size must be less than 5MB'); return; }
            
            selectedFile = file;
            const reader = new FileReader();
            reader.onload = (e) => {
                preview.innerHTML = '<img src="' + e.target.result + '" alt="Preview">';
                classifyBtn.disabled = false;
                result.classList.remove('show');
                error.classList.remove('show');
            };
            reader.readAsDataURL(file);
        }
        
        classifyBtn.addEventListener('click', async () => {
            if (!selectedFile) return;
            
            loading.classList.add('show');
            result.classList.remove('show');
            error.classList.remove('show');
            classifyBtn.disabled = true;
            
            const formData = new FormData();
            formData.append('file', selectedFile);
            
            try {
                const response = await fetch('/classify', { method: 'POST', body: formData });
                const data = await response.json();
                
                if (data.success) {
                    document.getElementById('resultObject').textContent = data.object;
                    document.getElementById('resultCategory').textContent = data.category;
                    document.getElementById('resultCategory').style.background = data.color;
                    document.getElementById('resultInstruction').textContent = data.instruction;
                    result.classList.add('show');
                    
                    // Change background gradient based on category
                    const bgGradient = categoryBgMap[data.category] || categoryBgMap["Unknown"];
                    document.body.style.background = bgGradient;
                } else {
                    showError(data.error || 'Classification failed');
                }
            } catch (err) {
                showError('Error: ' + err.message);
            } finally {
                loading.classList.remove('show');
                classifyBtn.disabled = false;
            }
        });
        
        function showError(msg) {
            error.textContent = msg;
            error.classList.add('show');
        }
    </script>
</body>
</html>"""


def resize_image(image_data, max_size=MAX_IMAGE_SIZE):
    """Resize image for faster processing"""
    try:
        from PIL import Image
        img = Image.open(BytesIO(image_data))
        img.thumbnail((max_size, max_size))
        output = BytesIO()
        img.save(output, format='JPEG', quality=85)
        return output.getvalue()
    except:
        return image_data  # Return original if resize fails


def classify_image(image_base64):
    prompt = """Identify item and classify: Wet, Dry, Plastic, Metal, Glass, E-Waste, Hazardous, Unknown.
JSON only: {"object": "name", "category": "Cat", "instruction": "dispose"}"""

    try:
        resp = requests.post(
            f"{OLLAMA_HOST}/api/generate",
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "images": [image_base64],
                "stream": False
            },
            timeout=120
        )
        resp.raise_for_status()
        text = resp.json().get("response", "")
        
        if "```" in text:
            text = text.split("```")[1].replace("json", "").strip()
        
        data = json.loads(text)
        category = data.get("category", "Unknown")
        if category not in CATEGORY_COLORS:
            category = "Unknown"
        
        return {
            "success": True,
            "object": data.get("object", "Unknown item"),
            "category": category,
            "color": CATEGORY_COLORS[category],
            "instruction": data.get("instruction", "Check local guidelines")
        }
    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "Ollama not running. Start with: ollama serve"}
    except json.JSONDecodeError:
        return {"success": False, "error": "Could not parse AI response"}
    except Exception as e:
        return {"success": False, "error": str(e)}


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path == "":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(HTML_PAGE.encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/classify":
            try:
                content_type = self.headers.get("Content-Type")
                if "multipart/form-data" in content_type:
                    form = cgi.FieldStorage(
                        fp=self.rfile,
                        headers=self.headers,
                        environ={"REQUEST_METHOD": "POST", "CONTENT_TYPE": content_type}
                    )
                    file_item = form["file"]
                    image_data = file_item.file.read()
                    image_data = resize_image(image_data)  # Compress for speed
                    image_base64 = base64.b64encode(image_data).decode("utf-8")
                    
                    result = classify_image(image_base64)
                    
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps(result).encode())
                else:
                    self.send_response(400)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps({"success": False, "error": "Invalid request"}).encode())
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        print(f"[{self.address_string()}] {args[0]}")


if __name__ == "__main__":
    print("\n" + "="*50)
    print("  TrashCollector AI")
    print("="*50)
    print(f"\n  Open: http://localhost:{PORT}")
    print(f"  Model: {OLLAMA_MODEL}")
    print("\n  Press Ctrl+C to stop\n")
    
    server = HTTPServer(("", PORT), Handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
