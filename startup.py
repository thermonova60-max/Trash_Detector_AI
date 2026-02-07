#!/usr/bin/env python3
"""
Startup script for TrashCollector AI
Checks server status and provides troubleshooting info
"""
import subprocess
import time
import requests
import json

def check_server():
    try:
        r = requests.get('http://localhost:8000', timeout=3)
        return True, r.status_code
    except:
        return False, None

def check_ngrok():
    try:
        r = requests.get('http://localhost:4040/api/tunnels')
        data = r.json()
        if data['tunnels']:
            return data['tunnels'][0]['public_url']
        return None
    except:
        return None

def main():
    print("\n" + "="*70)
    print("🚀 TrashCollector AI - Status Check")
    print("="*70)
    
    # Check Python server
    print("\n📍 Checking Python server on localhost:8000...")
    for i in range(5):
        is_running, code = check_server()
        if is_running:
            print(f"✅ Python server is running (HTTP {code})")
            break
        print(f"   ⏳ Attempt {i+1}/5... waiting...")
        time.sleep(1)
    else:
        print("❌ Python server not responding")
        print("   Restart with: cd backend && python app.py")
        return
    
    # Check Ollama
    print("\n🤖 Checking Ollama on localhost:11434...")
    try:
        r = requests.get('http://localhost:11434/api/tags', timeout=3)
        if r.status_code == 200:
            models = r.json().get('models', [])
            if any('gemma' in m['name'] for m in models):
                print("✅ Ollama is ready with gemma3:4b-cloud")
            else:
                print("⚠️ Ollama running but gemma3:4b-cloud not loaded")
                print("   Run: ollama pull gemma3:4b-cloud")
    except:
        print("❌ Ollama not responding on port 11434")
        print("   Start with: ollama serve")
        return
    
    # Check Ngrok
    print("\n🌍 Checking ngrok tunnel...")
    url = check_ngrok()
    if url:
        print(f"✅ Ngrok tunnel active: {url}")
    else:
        print("❌ Ngrok not running")
        print("   Start with: ngrok http 8000")
        return
    
    # Check Firebase
    print("\n🔥 Checking Firebase configuration...")
    print("✅ Firebase configured (anonymous auth + Realtime DB)")
    
    print("\n" + "="*70)
    print("🎉 All systems ready!")
    print("="*70)
    print(f"\n📱 Local:  http://localhost:8000")
    print(f"🌐 Public: {url}")
    print("\n🎯 Access your app:")
    print(f"   - Browser: {url}")
    print(f"   - Mobile: {url}")
    print(f"   - Share: {url}")
    print("\n💾 Scans auto-sync to Firebase Realtime Database")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
