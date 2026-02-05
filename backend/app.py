from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import requests
import base64
import cgi

PORT = 8000
OLLAMA_MODEL = "qwen3-vl:235b-cloud"
OLLAMA_HOST = "http://localhost:11434"

CATEGORY_COLORS = {
    "Wet": "#2ecc71", "Dry": "#3498db", "Plastic": "#f1c40f",
    "Metal": "#95a5a6", "Glass": "#1abc9c", "E-Waste": "#9b59b6",
    "Hazardous": "#e74c3c", "Unknown": "#7f8c8d"
}

HTML_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TrashCollector AI</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }
        .header h1 { font-size: 36px; margin-bottom: 10px; }
        .header p { opacity: 0.9; font-size: 16px; }
        .status-bar {
            background: #f8f9fa;
            padding: 15px 30px;
            display: flex;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 10px;
            border-bottom: 1px solid #eee;
            font-size: 14px;
        }
        .status-item { display: flex; gap: 8px; }
        .status-label { color: #666; }
        .status-value { font-weight: bold; color: #333; }
        .status-active { color: #2ecc71; }
        .content { padding: 40px; }
        .upload-area {
            border: 3px dashed #667eea;
            border-radius: 15px;
            padding: 60px 40px;
            text-align: center;
            background: #f8f9ff;
            cursor: pointer;
            transition: all 0.3s;
        }
        .upload-area:hover { background: #eef1ff; border-color: #764ba2; }
        .upload-icon { font-size: 64px; margin-bottom: 20px; }
        .upload-text { font-size: 18px; color: #333; margin-bottom: 10px; }
        .upload-hint { font-size: 14px; color: #666; }
        #fileInput { display: none; }
        .btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 15px 40px;
            font-size: 16px;
            font-weight: bold;
            border-radius: 50px;
            cursor: pointer;
            margin-top: 20px;
            transition: transform 0.3s, box-shadow 0.3s;
        }
        .btn:hover { transform: translateY(-2px); box-shadow: 0 10px 25px rgba(102,126,234,0.4); }
        .btn:disabled { opacity: 0.6; cursor: not-allowed; transform: none; }
        .preview { margin-top: 30px; text-align: center; }
        .preview img { max-width: 300px; max-height: 300px; border-radius: 10px; box-shadow: 0 5px 20px rgba(0,0,0,0.2); }
        .result {
            margin-top: 30px;
            padding: 30px;
            background: #f8f9fa;
            border-radius: 15px;
            display: none;
        }
        .result.show { display: block; animation: fadeIn 0.5s; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
        .result-header { font-size: 14px; color: #666; text-transform: uppercase; margin-bottom: 10px; }
        .result-object { font-size: 24px; font-weight: bold; color: #333; margin-bottom: 20px; }
        .result-category {
            display: inline-block;
            padding: 15px 30px;
            border-radius: 50px;
            color: white;
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 20px;
        }
        .result-instruction {
            background: white;
            padding: 20px;
            border-radius: 10px;
            border-left: 4px solid #667eea;
            font-size: 16px;
            color: #333;
        }
        .categories {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
            gap: 10px;
            margin-top: 30px;
            padding-top: 30px;
            border-top: 1px solid #eee;
        }
        .category {
            padding: 15px 10px;
            border-radius: 10px;
            text-align: center;
            font-size: 12px;
            font-weight: 600;
            color: white;
        }
        .loading { display: none; text-align: center; padding: 40px; }
        .loading.show { display: block; }
        .spinner {
            width: 50px; height: 50px;
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        .error { color: #e74c3c; background: #fdf0f0; padding: 15px; border-radius: 10px; margin-top: 20px; display: none; }
        .error.show { display: block; }
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
                <span class="status-value">qwen3-vl:235b-cloud</span>
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
                <div class="category" style="background:#2ecc71">Wet</div>
                <div class="category" style="background:#3498db">Dry</div>
                <div class="category" style="background:#f1c40f;color:#333">Plastic</div>
                <div class="category" style="background:#95a5a6">Metal</div>
                <div class="category" style="background:#1abc9c">Glass</div>
                <div class="category" style="background:#9b59b6">E-Waste</div>
                <div class="category" style="background:#e74c3c">Hazardous</div>
                <div class="category" style="background:#7f8c8d">Unknown</div>
            </div>
        </div>
    </div>
    
    <script>
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


def classify_image(image_base64):
    prompt = """Analyze this image and identify the waste item. Classify it into ONE category:
Wet, Dry, Plastic, Metal, Glass, E-Waste, Hazardous, or Unknown.

Respond ONLY in this JSON format:
{"object": "item name", "category": "Category", "instruction": "how to dispose"}"""

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
