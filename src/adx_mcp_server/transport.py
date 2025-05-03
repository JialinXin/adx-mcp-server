#!/usr/bin/env python
from fastapi import Request
from mcp.server.sse import SseServerTransport
from .app import app, mcp

transport = SseServerTransport("/messages/")

@app.get("/sse/")
async def sse_endpoint(request: Request):
    async with transport.connect_sse(request.scope, request.receive, request._send) as streams:
        await mcp._mcp_server.run(
            streams[0], streams[1], mcp._mcp_server.create_initialization_options()
        )

app.mount("/messages", transport.handle_post_message)
