import socket
import time
import logging
import random
import os

# Configure logging
logging.basicConfig(filename='server_log.txt', level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')

# Server port
PORT = 8001

def handle_client(conn):
    logging.info(f"Client connected from {conn.getpeername()}")

    # Receive request
    try:
        data = conn.recv(1024).decode()
        logging.info(f"Received request:\n{data}")
    except Exception as e:
        logging.error(f"Error receiving request: {e}")
        return

    # Parse request to extract requested file
    lines = data.splitlines()
    request_line = lines[0]
    method, path, protocol = request_line.split()
    file_path = path[1:]  # Remove leading slash

    # Process request (simulate 50% error)
    error_50_chance = random.random() < 0.5
    if error_50_chance:
        response = create_error_response(500, "Something went wrong")
        logging.info(f"Responding with error: {response}")
    else:
        # Check if file exists and is accessible
        if os.path.exists(file_path) and os.access(file_path, os.R_OK):
            try:
                with open(file_path, 'rb') as f:
                    file_content = f.read()
                response = create_response(200, "OK", file_content)
                logging.info(f"Responding with success: {response}")
            except Exception as e:
                logging.error(f"Error reading file {file_path}: {e}")
                response = create_error_response(500, "Internal Server Error")
        else:
            response = create_error_response(404, "Not Found")
            logging.info(f"File not found or inaccessible: {file_path}")

    # Send response
    try:
        conn.sendall(response.encode())
    except Exception as e:
        logging.error(f"Error sending response: {e}")

    # Close connection
    conn.close()
    logging.info(f"Client disconnected")

def create_error_response(status_code, message):
    return f"HTTP/1.1 {status_code} {message}\r\n" \
           f"Content-Type: text/html\r\n\r\n" \
           f"<h1>Error {status_code}: {message}</h1>"

def create_response(status_code, message, content):
    return f"HTTP/1.1 {status_code} {message}\r\n" \
           f"Content-Type: text/html\r\n\r\n" \
           f"{content}"

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', PORT))
        s.listen()
        logging.info(f"Server listening on port {PORT}")

        while True:
            conn, addr = s.accept()
            logging.info(f"Client connected from {addr}")
            handle_client(conn)

if __name__ == "__main__":
    main()
