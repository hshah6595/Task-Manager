import json
import socket
import subprocess
import threading
import time

class TaskRequest:
    def __init__(self, command, timeout):
        self.command = command
        self.timeout = timeout

    @staticmethod
    def from_json(json_data):
        data = json.loads(json_data)
        return TaskRequest(data["command"], data.get("timeout"))

class TaskResult:
    def __init__(self, command, executed_at, duration_ms, exit_code, output, error):
        self.command = command
        self.executed_at = executed_at
        self.duration_ms = duration_ms
        self.exit_code = exit_code
        self.output = output
        self.error = error

    def to_json(self):
        return json.dumps({
            "command": self.command,
            "executed_at": self.executed_at,
            "duration_ms": self.duration_ms,
            "exit_code": self.exit_code,
            "output": self.output,
            "error": self.error
        })

# using the subprocess to execute the request
def execute_task(request):
    start_time = time.time()
    try:
        if not request.timeout:
            result = subprocess.run(request.command, capture_output=True, text=True)
        else:
            result = subprocess.run(request.command, capture_output=True, text=True, timeout=request.timeout / 1000)
        exit_code = result.returncode
        output = result.stdout
        error = result.stderr if exit_code != 0 else ""
    except subprocess.TimeoutExpired:
        exit_code = -1
        output = ""
        error = "timeout exceeded"
    except Exception as e:
        exit_code = -1
        output = ""
        error = str(e)
    end_time = time.time()
    duration_ms = (end_time - start_time) * 1000
    return TaskResult(request.command, int(start_time), duration_ms, exit_code, output, error)

# logic of handling request and sending response
def handle_request(request_str, client_socket):
    request = TaskRequest.from_json(request_str)
    result = execute_task(request)
    response_data = result.to_json().encode("utf-8")
    client_socket.sendall(response_data + b"\n")

# read the request and execute in parallel
def handle_client(client_socket, client_address):
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            request_list = data.decode("utf-8").strip().split("\n")
            for request_str in request_list:
                threading.Thread(target=handle_request, args=(request_str, client_socket)).start()
    except Exception as e:
        print("Error:", e)
    finally:
        client_socket.close()

# open socket and listen to incoming connection request
def main():
    host, port = "127.0.0.1", 3000
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(10)
    print("Server is listening on port 3000...")

    while True:
        client_socket, client_address = server_socket.accept()
        print("Accepted connection from:", client_address)
        threading.Thread(target=handle_client, args=(client_socket, client_address)).start()

if __name__ == "__main__":
    main()