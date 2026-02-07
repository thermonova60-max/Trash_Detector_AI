from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import requests
import base64
import cgi
import os
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
    prompt = """Identify the main item and classify it: Wet, Dry, Plastic, Metal, Glass, E-Waste, Hazardous, Biowaste, Sprays, Unknown.
    Also detect if these e-waste items are present (1 if yes, 0 if no):
    mobile, laptop, tablet, battery, charger, wire, circuit_board, motherboard, hard_disk, keyboard, mouse, monitor, cpu, power_supply, other
    
JSON only: {"object": "main item name", "category": "Category", "instruction": "disposal instructions", "items": [{"name": "item", "count": 0/1}, ...]}""" 

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
        
        # Format items with clean names
        items = data.get("items", [])
        if isinstance(items, list):
            for item in items:
                if "name" in item:
                    item["name"] = item["name"].replace("_", " ").title()
        
        return {
            "success": True,
            "object": data.get("object", "Unknown item"),
            "category": category,
            "color": CATEGORY_COLORS[category],
            "instruction": data.get("instruction", "Check local guidelines"),
            "items": items
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
            try:
                # Get the directory where app.py is located
                base_dir = os.path.dirname(os.path.abspath(__file__))
                html_file = os.path.join(base_dir, 'index.html')
                
                # Read and serve the HTML file
                with open(html_file, 'rb') as f:
                    html_bytes = f.read()
                
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.send_header('Content-Length', str(len(html_bytes)))
                self.end_headers()
                try:
                    self.wfile.write(html_bytes)
                except (ConnectionAbortedError, BrokenPipeError):
                    pass  # Client disconnected, ignore
            except FileNotFoundError:
                self.send_response(500)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b"<h1>500 Error</h1><p>index.html not found</p>")
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
        elif self.path == "/favicon.ico":
            # Respond with 204 No Content for favicon (prevents 404 error)
            self.send_response(204)
            self.end_headers()
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
                    response_json = json.dumps(result).encode()
                    
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.send_header("Content-Length", str(len(response_json)))
                    self.end_headers()
                    self.wfile.write(response_json)
                else:
                    error_response = json.dumps({"success": False, "error": "Invalid request"}).encode()
                    self.send_response(400)
                    self.send_header("Content-type", "application/json")
                    self.send_header("Content-Length", str(len(error_response)))
                    self.end_headers()
                    self.wfile.write(error_response)
            except (ConnectionAbortedError, BrokenPipeError):
                pass  # Browser closed connection, ignore
            except Exception as e:
                try:
                    error_response = json.dumps({"success": False, "error": str(e)}).encode()
                    self.send_response(500)
                    self.send_header("Content-type", "application/json")
                    self.send_header("Content-Length", str(len(error_response)))
                    self.end_headers()
                    self.wfile.write(error_response)
                except (ConnectionAbortedError, BrokenPipeError):
                    pass
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
