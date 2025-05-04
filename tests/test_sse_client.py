import requests
import threading
import time

SSE_URL = "http://127.0.0.1:8080/sse/"
#MSG_URL = "http://127.0.0.1:8080/messages/"
SESSION_ID = "test-session"
QUERY = "BillingUsage_Daily | getschema"

MSG_PATH = None

def listen_to_sse():
    global MSG_PATH
    print("Connecting to SSE stream...")
    try:
        with requests.get(SSE_URL, params={"session_id": SESSION_ID}, stream=True) as resp:
            if resp.status_code != 200:
                print("Failed to connect:", resp.status_code)
                return
            print("SSE connection established")
            for line in resp.iter_lines():
                if line:
                    decoded = line.decode("utf-8")
                    print("🔔 SSE:", decoded)
                    if decoded.startswith("data: /messages"):
                        MSG_PATH = decoded.replace("data: ", "").strip()
    except requests.RequestException as e:
        print(f"SSE connection error: {e}")

def send_message():
    global MSG_PATH
    for _ in range(20):
        if MSG_PATH:
            break
        time.sleep(0.5)
    if not MSG_PATH:
        print("❌ Failed to retrieve message path from SSE stream.")
        return False

    full_url = f"http://127.0.0.1:8080{MSG_PATH}"
    payload = {
        "method": "tools/call",
        "params": {
            "name": "execute_query",
            "arguments": {
                "query": QUERY
            },
            "_meta": {
                "processToken": 0
            }
        }
    }
    initializePayload = {
        "method": "initialize"
    }
    listToolsPayload = {
        "method": "tools.list",
        "params": {}
    }


    print(f"Sending message to MCP: {payload} -> {full_url}")
    try:
        response = requests.post(full_url, json=payload)
        response.raise_for_status()
        print("📬 Response status:", response.status_code)
        print("📬 Response body:", response.text)
        return response.ok
    except requests.RequestException as e:
        print(f"Failed to send message: {e}")
        return False


if __name__ == "__main__":
    # Start SSE listener in background thread
    sse_thread = threading.Thread(target=listen_to_sse, daemon=True)
    sse_thread.start()

    # Send input to /messages
    success = send_message()

    # Keep main thread alive to receive events
    wait_time = 30  # Increased wait time to receive responses
    print(f"Waiting {wait_time} seconds for events...")
    time.sleep(wait_time)
