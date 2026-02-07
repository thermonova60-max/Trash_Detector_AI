import requests
import json

try:
    r = requests.get('http://localhost:4040/api/tunnels')
    data = r.json()
    
    print("\n" + "="*60)
    print("🌍 NGROK TUNNELS")
    print("="*60)
    
    if 'tunnels' in data and len(data['tunnels']) > 0:
        for tunnel in data['tunnels']:
            print(f"✅ Public URL: {tunnel['public_url']}")
            print(f"   Protocol: {tunnel['proto']}")
            print(f"   Local: {tunnel['config']['addr']}")
    else:
        print("⏳ No tunnels found. Ngrok may still be initializing...")
        
    print("="*60 + "\n")
except Exception as e:
    print(f"❌ Error: {e}")
    print("Make sure ngrok is running on port 8000")
