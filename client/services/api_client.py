import requests

class ApiClient:
    def __init__(self):
        self.base_url = ""
        self.token = ""

    def connect(self, url: str, token: str):
        # normalize url
        if not url.startswith("http"):
            url = f"http://{url}"
        self.base_url = url.rstrip("/")
        self.token = token
        
        # Test connection
        try:
            headers = {"x-token": self.token}
            resp = requests.get(f"{self.base_url}/system/stats", headers=headers, timeout=5)
            return resp.status_code == 200
        except:
            return False

    def get_stats(self):
        try:
            resp = requests.get(f"{self.base_url}/system/stats", headers={"x-token": self.token}, timeout=2)
            if resp.status_code == 200:
                return resp.json()
        except:
            pass
        return None

    def get_processes(self):
        try:
            resp = requests.get(f"{self.base_url}/processes", headers={"x-token": self.token}, timeout=5)
            if resp.status_code == 200:
                return resp.json()
        except:
            pass
        return []

    def kill_process(self, pid: int):
        try:
            resp = requests.post(
                f"{self.base_url}/processes/kill", 
                headers={"x-token": self.token}, 
                json={"pid": pid}
            )
            return resp.status_code == 200, resp.json().get("detail", "Error")
        except Exception as e:
            return False, str(e)

    def execute_command(self, command: str):
        try:
            resp = requests.post(
                f"{self.base_url}/terminal/execute", 
                headers={"x-token": self.token}, 
                json={"command": command},
                timeout=15
            )
            if resp.status_code == 200:
                return resp.json()
            return {"error": f"HTTP {resp.status_code}"}
        except Exception as e:
            return {"error": str(e)}

    def get_services(self):
        try:
            resp = requests.get(f"{self.base_url}/services", headers={"x-token": self.token}, timeout=5)
            if resp.status_code == 200:
                return resp.json()
        except:
            pass
        return []

    def manage_service(self, name: str, action: str):
        try:
            resp = requests.post(
                f"{self.base_url}/services/{name}/{action}", 
                headers={"x-token": self.token},
                timeout=10
            )
            return resp.status_code == 200, resp.json().get("detail", "Error")
        except Exception as e:
            return False, str(e)

    def shutdown_system(self):
        try:
            resp = requests.post(f"{self.base_url}/system/shutdown", headers={"x-token": self.token}, timeout=2)
            return resp.status_code == 200, resp.json().get("message", "Error")
        except Exception as e:
            return True, "Command sent"

    def reboot_system(self):
        try:
            resp = requests.post(f"{self.base_url}/system/reboot", headers={"x-token": self.token}, timeout=2)
            return resp.status_code == 200, resp.json().get("message", "Error")
        except Exception as e:
            return True, "Command sent"

# Global instance
api_client = ApiClient()
