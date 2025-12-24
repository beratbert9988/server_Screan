import psutil
import time
import subprocess

def get_system_stats():
    return {
        "cpu_percent": psutil.cpu_percent(interval=1),
        "ram_percent": psutil.virtual_memory().percent,
        "ram_used": psutil.virtual_memory().used,
        "ram_total": psutil.virtual_memory().total,
        "disk_percent": psutil.disk_usage('/').percent
    }

def get_processes():
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent']):
        try:
            p_info = proc.info
            processes.append(p_info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    # Sort by CPU usage descending
    return sorted(processes, key=lambda p: p['cpu_percent'] or 0, reverse=True)

def kill_process(pid: int):
    try:
        proc = psutil.Process(pid)
        proc.kill()
        return True, "Process killed"
    except psutil.NoSuchProcess:
        return False, "Process not found"
    except psutil.AccessDenied:
        return False, "Access denied"
    except Exception as e:
        return False, str(e)

def shutdown_system():
    try:
        # Linux specific
        subprocess.run(["shutdown", "now"], check=True)
        return True, "Shutting down..."
    except Exception as e:
        return False, str(e)

def reboot_system():
    try:
        # Linux specific
        subprocess.run(["reboot"], check=True)
        return True, "Rebooting..."
    except Exception as e:
        return False, str(e)
