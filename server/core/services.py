import subprocess

def get_services():
    try:
        # List all loaded units (active or failed)
        cmd = ["systemctl", "list-units", "--type=service", "--all", "--no-pager", "--plain"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        services = []
        for line in result.stdout.splitlines()[1:]:
            parts = line.split()
            if len(parts) >= 4 and parts[0].endswith('.service'):
                # Basic parsing: unit load active sub description...
                services.append({
                    "unit": parts[0],
                    "load": parts[1],
                    "active": parts[2],
                    "sub": parts[3],
                    "description": " ".join(parts[4:])
                })
        return services
    except Exception as e:
        return []

def manage_service(service_name: str, action: str):
    if action not in ["start", "stop", "restart", "status"]:
        return False, "Invalid action"
    
    try:
        # This requires permissions!
        cmd = ["systemctl", action, service_name]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            return True, f"Service {service_name} {action}ed successfully"
        else:
            return False, result.stderr.strip() or "Command failed"
    except Exception as e:
        return False, str(e)
