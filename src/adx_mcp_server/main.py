#!/usr/bin/env python
import sys
import dotenv
from adx_mcp_server.app import app
from adx_mcp_server.config import config
from adx_mcp_server import tools, transport
import uvicorn

def setup_environment() -> bool:
    dotenv.load_dotenv()
    if not config.cluster_url or not config.database:
        print("Missing ADX config.")
        return False
    return True

if __name__ == "__main__":
    if not setup_environment():
        sys.exit(1)
    
    #app.include_router(router)
    print("Starting server...")
    uvicorn.run(app, host="127.0.0.1", port=8080)
