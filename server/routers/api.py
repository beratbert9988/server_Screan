from fastapi import APIRouter, Depends, HTTPException, Header
from pydantic import BaseModel
from ..core.system import get_processes, kill_process, get_system_stats, shutdown_system, reboot_system
from ..core.terminal import execute_command
from ..core.services import get_services, manage_service
from ..core.config import config

router = APIRouter()

# Security Dependency
def verify_token(x_token: str = Header(...)):
    if x_token != config['server']['auth_token']:
        raise HTTPException(status_code=401, detail="Invalid Auth Token")

# Models on routers to avoid circular imports or messy structure for this size
class KillRequest(BaseModel):
    pid: int

class CommandRequest(BaseModel):
    command: str

@router.get("/system/stats", dependencies=[Depends(verify_token)])
def stats():
    return get_system_stats()

@router.post("/system/shutdown", dependencies=[Depends(verify_token)])
def shutdown():
    success, msg = shutdown_system()
    if not success:
        raise HTTPException(status_code=500, detail=msg)
    return {"message": msg}

@router.post("/system/reboot", dependencies=[Depends(verify_token)])
def reboot():
    success, msg = reboot_system()
    if not success:
        raise HTTPException(status_code=500, detail=msg)
    return {"message": msg}

@router.get("/processes", dependencies=[Depends(verify_token)])
def list_processes():
    return get_processes()

@router.post("/processes/kill", dependencies=[Depends(verify_token)])
def kill_proc(req: KillRequest):
    success, msg = kill_process(req.pid)
    if not success:
        raise HTTPException(status_code=400, detail=msg)
    return {"message": msg}

@router.post("/terminal/execute", dependencies=[Depends(verify_token)])
def exec_cmd(req: CommandRequest):
    # Security Warning: This allows executing ANY command.
    return execute_command(req.command)

@router.get("/services", dependencies=[Depends(verify_token)])
def list_svc():
    return get_services()

@router.post("/services/{name}/{action}", dependencies=[Depends(verify_token)])
def manage_svc(name: str, action: str):
    success, msg = manage_service(name, action)
    if not success:
        raise HTTPException(status_code=400, detail=msg)
    return {"message": msg}
