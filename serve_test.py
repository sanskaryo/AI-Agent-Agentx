from http.server import HTTPServer, SimpleHTTPRequestHandler
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CustomHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory="test_website", **kwargs)

def run(server_class=HTTPServer, handler_class=CustomHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logger.info(f"Starting server on port {port}")
    httpd.serve_forever()

if __name__ == '__main__':
    run() 