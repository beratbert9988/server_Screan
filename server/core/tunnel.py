import subprocess
import threading
import time
import shutil

class TunnelManager:
    def __init__(self, token: str):
        self.token = token
        self.process = None

    def start(self):
        if not self.token:
            print("Tunnel token is empty, skipping tunnel start.")
            return

        if self.process and self.process.poll() is None:
            print("Tunnel is already running.")
            return

        cloudflared_path = shutil.which("cloudflared")
        if not cloudflared_path:
            print("cloudflared binary not found in PATH.")
            return

        cmd = [cloudflared_path, "tunnel", "run", "--token", self.token]
        
        try:
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            print(f"Cloudflared tunnel started with PID {self.process.pid}")
            
            # Start a thread to monitor output (optional, mostly for debugging)
            threading.Thread(target=self._monitor_output, daemon=True).start()
            
        except Exception as e:
            print(f"Failed to start tunnel: {e}")

    def stop(self):
        if self.process and self.process.poll() is None:
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
            print("Cloudflared tunnel stopped.")

    def _monitor_output(self):
        # Just logging stderr as cloudflared prints there
        if self.process and self.process.stderr:
            for line in self.process.stderr:
                pass # print(f"[Cloudflared] {line.decode().strip()}")
