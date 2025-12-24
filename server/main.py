from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .routers import api
from .core.config import config
from .core.tunnel import TunnelManager
import uvicorn

tunnel_manager = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    global tunnel_manager
    if config['tunnel']['enabled']:
        print("Starting Cloudflared Tunnel...")
        tunnel_manager = TunnelManager(config['tunnel']['cloudflared_token'])
        tunnel_manager.start()
    
    yield
    
    # Shutdown
    if tunnel_manager:
        print("Stopping Cloudflared Tunnel...")
        tunnel_manager.stop()

app = FastAPI(lifespan=lifespan, title="Server Control Panel")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api.router)

@app.get("/")
def root():
    return {"status": "online", "message": "Server Control Panel is running"}

def run():
    uvicorn.run(
        "server.main:app", 
        host=config['server']['host'], 
        port=config['server']['port'], 
        reload=False
    )

if __name__ == "__main__":
    run()
