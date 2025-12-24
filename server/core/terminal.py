import subprocess

def execute_command(command: str):
    try:
        # Run command and capture output
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True, 
            timeout=10
        )
        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        }
    except subprocess.TimeoutExpired:
        return {"error": "Command execution timed out"}
    except Exception as e:
        return {"error": str(e)}
