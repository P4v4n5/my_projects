import http.server
import socketserver
import random
import logging
import time

# Set up logging
log_filename = "csen233midtermWangSinYaw.log"  # Replace with your filename
logging.basicConfig(filename=log_filename, level=logging.INFO)

# Define the port number
PORT = 8100  # Replace with your chosen port number

# Define the HTTP request handler class
class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Log the timestamp of the request
        logging.info(f"Request received at {time.strftime('%Y-%m-%d %H:%M:%S')}")

        # Generate a response
        if random.random() < 0.5:
            # Reply with arbitrary contents
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"<html><body><h1>Hello, World!</h1></body></html>")
        else:
            # Return an error with 50% probability
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b"Internal Server Error")

# Start the HTTP server
with socketserver.TCPServer(("", PORT), MyHttpRequestHandler) as httpd:
    # Display the URL to connect to the server
    print(f"Server started at http://localhost:{PORT}/")

    # Serve indefinitely
    httpd.serve_forever()
