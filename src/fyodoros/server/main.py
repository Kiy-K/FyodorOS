from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import threading
import time
import asyncio
from fyodoros.kernel.kernel import Kernel
from fyodoros.kernel.io import APIAdapter

app = FastAPI()

# Global State
kernel = None
io_adapter = None
kernel_thread = None

class CommandRequest(BaseModel):
    command: str

def run_kernel_loop(k):
    """
    Background thread to drive the Kernel/Shell loop.
    """
    print("[Server] Starting Kernel Loop...")
    try:
        k.start() # This blocks in the shell loop
    except Exception as e:
        print(f"[Server] Kernel crashed: {e}")

@app.on_event("startup")
def startup_event():
    global kernel, io_adapter, kernel_thread

    # 1. Initialize API Adapter
    io_adapter = APIAdapter()

    # 2. Initialize Kernel with this adapter
    print("[Server] Booting Kernel...")
    kernel = Kernel(io_adapter=io_adapter)

    # 3. Start Kernel in background thread
    kernel_thread = threading.Thread(target=run_kernel_loop, args=(kernel,), daemon=True)
    kernel_thread.start()

@app.get("/health")
def health_check():
    if kernel and kernel_thread.is_alive():
        return {"status": "running", "uptime": "ok"}
    return {"status": "starting"}

@app.post("/exec")
def execute_command(req: CommandRequest):
    """
    Inject a command into the shell input stream.
    """
    if not io_adapter:
        return JSONResponse({"error": "Kernel not ready"}, status_code=503)

    # Inject command into input queue
    # The shell is blocked on io.read(), this will unblock it
    io_adapter.input(req.command)
    return {"status": "queued"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Poll for output and signals from the kernel
            if io_adapter:
                # 1. Check Output (Text)
                output = io_adapter.get_output()
                if output:
                    # Backward compatibility: Send plain text if it's text
                    # Or structured JSON? For now, we assume frontend expects text.
                    # But if we want structured...
                    # The instruction says: 'Send {"type": "text", "content": ...}'
                    await websocket.send_json({"type": "text", "content": output})

                # 2. Check Signals (Control)
                signal = io_adapter.get_signal()
                if signal:
                     await websocket.send_json({"type": "signal", "content": signal})

                if not output and not signal:
                    await asyncio.sleep(0.05)
            else:
                await asyncio.sleep(1)
    except WebSocketDisconnect:
        print("[Server] Client disconnected")
