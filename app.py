import os
import signal
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/":
            self.send_error(404, "Not Found")
            return

        file_path = os.getenv("FILE_PATH", "/var/secret/secret.txt")
        greeting = os.getenv("GREETING", "Hello World!")

        try:
            with open(file_path, 'r') as file:
                file_content = file.read()
                response = f"File content:\n{file_content}\nServer hostname: {get_hostname()}\n"
        except Exception:
            response = f"{greeting}\nServer hostname: {get_hostname()}\n"

        self.send_response(200)
        self.end_headers()
        self.wfile.write(response.encode('utf-8'))

def get_hostname():
    try:
        return os.uname().nodename
    except Exception:
        return "Unknown"

def handle_signals(server):
    def signal_handler(sig, frame):
        print(f"Received signal: {sig}. Shutting down gracefully...")
        server.shutdown()
        print("Server has been closed.")
        sys.exit(0)
    return signal_handler

def run():
    port = 3000
    server_address = ('', port)
    httpd = HTTPServer(server_address, RequestHandler)
    
    signal.signal(signal.SIGINT, handle_signals(httpd))
    signal.signal(signal.SIGTERM, handle_signals(httpd))

    print(f"Server is running on http://localhost:{port}")
    print(f"File path is set to: {os.getenv('FILE_PATH', '/var/secret/secret.txt')}")
    httpd.serve_forever()

if __name__ == "__main__":
    run()