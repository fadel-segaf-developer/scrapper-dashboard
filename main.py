from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.responses import FileResponse
from threading import Thread
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import webview
import asyncio
import uvicorn
from scraper import scrape_a, scrape_b, post_c
import webview.platforms.edgechromium as edge


app = FastAPI()
@app.get("/")
async def serve_index():
    return FileResponse("web/index.html")

# Mount static files correctly
app.mount("/static", StaticFiles(directory="web"), name="static")

# Track connected clients
active_clients = []

@app.websocket("/ws/files")
async def file_watcher_ws(websocket: WebSocket):
    await websocket.accept()
    active_clients.append(websocket)

    try:
        while True:
            await asyncio.sleep(60)  # keep connection alive
    except WebSocketDisconnect:
        active_clients.remove(websocket)

# File Watcher Handler
class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, folder: Path):
        self.folder = folder

    def on_created(self, event):
        if event.is_directory:
            return
        filename = Path(event.src_path).name
        print(f"[📁] New file detected: {filename}")
        try:
            asyncio.run(send_file_update(f"📁 New file detected: {filename}"))
        except Exception as e:
            print(f"[❌] Failed to send over WebSocket: {e}")

# Async push to all connected WebSocket clients
async def send_file_update(message: str):
    for client in active_clients:
        try:
            await client.send_json({"message": message})
        except:
            pass  # skip dead clients

# Start file observer
def start_watcher():
    path = Path("ScrappedFiles")
    path.mkdir(exist_ok=True)
    observer = Observer()
    handler = FileChangeHandler(path)
    observer.schedule(handler, str(path), recursive=False)
    observer.start()

# Uvicorn Runner
def start_fastapi():
    start_watcher()
    uvicorn.run(app, host="127.0.0.1", port=5000, log_level="info")

@app.get("/api/get_a")
async def get_a():
    return JSONResponse(content={"result": scrape_a()})

@app.get("/api/get_b")
async def get_b():
    return JSONResponse(content={"result": scrape_b()})

@app.post("/api/post_c")
async def do_post():
    post_c()
    return JSONResponse(content={"status": "success"})

if __name__ == '__main__':
    Thread(target=start_fastapi, daemon=True).start()
    webview.create_window("Scraper Dashboard", "http://127.0.0.1:5000", frameless=True, width=1280, height=720, min_size=(1280, 720))
    webview.start(gui='edgechromium', debug=True)