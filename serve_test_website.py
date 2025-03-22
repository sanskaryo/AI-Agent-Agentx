import http.server
import socketserver
import os
import sys

PORT = 8080

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory="test_website", **kwargs)

def run_server():
    try:
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            print(f"Serving test website at http://localhost:{PORT}")
            httpd.serve_forever()
    except OSError as e:
        print(f"Error: Port {PORT} is already in use. Please try a different port.")
        print("You can either:")
        print("1. Kill the process using port 8080")
        print("2. Change the PORT variable to a different number")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nServer stopped by user")
        sys.exit(0)

if __name__ == "__main__":
    run_server() 