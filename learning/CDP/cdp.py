import requests
import json

def get_cdp_discovery():
    url = "http://127.0.0.1:9222/json"
    try:
        print(f"📡 Attempting to connect to Chrome at {url}...")
        response = requests.get(url, timeout=2)
        
        tabs = response.json()
        
        print(f"✅ Connected! Found {len(tabs)} open targets/tabs.\n")
        
        # Look for the first 'page' type target
        for tab in tabs:
            if tab['type'] == 'page':
                print(f"🎯 Target Found: {tab['title']}")
                print(f"🔗 WebSocket URL: {tab['webSocketDebuggerUrl']}")
                return tab['webSocketDebuggerUrl']
                
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Connection Refused.")
        print("👉 Make sure Chrome is running with: --remote-debugging-port=9222")
    except Exception as e:
        print(f"❓ An unexpected error occurred: {e}")

if __name__ == "__main__":
    ws_url = get_cdp_discovery()