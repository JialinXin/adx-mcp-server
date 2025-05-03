import requests
import threading
import time

SSE_URL = "http://127.0.0.1:8080/sse/"
MSG_URL = "http://127.0.0.1:8080/messages/"
SESSION_ID = "test-session"
QUERY = "show table BillingUsage_Daily schema"

def listen_to_sse():
    print("Connecting to SSE stream...")
    with requests.get(SSE_URL, params={"session_id": SESSION_ID}, stream=True) as resp:
        if resp.status_code != 200:
            print("Failed to connect:", resp.status_code)
            return
        for line in resp.iter_lines():
            if line:
                decoded = line.decode("utf-8")
                print("🔔 SSE:", decoded)

def send_message():
    time.sleep(100)  # Wait for SSE to connect
    payload = {
        "session_id": SESSION_ID,
        "input": QUERY
    }
    print(f"Sending message to MCP: {payload}")
    response = requests.post(MSG_URL, json=payload)
    print("📬 Response status:", response.status_code)
    print("📬 Response body:", response.text)

if __name__ == "__main__":
    # Start SSE listener in background thread
    sse_thread = threading.Thread(target=listen_to_sse, daemon=True)
    sse_thread.start()

    # Send input to /messages
    send_message()

    # Keep main thread alive to receive events
    time.sleep(10)
