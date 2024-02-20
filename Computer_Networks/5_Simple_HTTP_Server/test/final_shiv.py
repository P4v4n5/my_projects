import socket
import time
import logging
import random

# Configure logging
logging.basicConfig(filename='serverfinal.txt', level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')

# Server port
PORT = 8000

def handle_client(conn):
    PORT = 8000
    logging.info(f"Client connected from {conn.getpeername()}")

    # Receive request
    try:
        data = conn.recv(1024).decode()
        logging.info(f"Received request:\n{data}")
    except Exception as e:
        logging.error(f"Error receiving request: {e}")
        return

    # Process request (ignore client file, simulate 50% error)
    error_50_chance = random.random() < 0.5
    if error_50_chance:
        response = create_error_response(404, "Not Found")
        logging.info(f"Responding with error: {response}")
    else:
        # Replace with your actual file handling logic
        file_content = "This is the sample HTML file"
        response = create_response(200, "OK", file_content)
        logging.info(f"Responding with success: {response}")

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
        print(f"Server URL: http://localhost:{PORT}/")

        while True:
            conn, addr = s.accept()
            logging.info(f"Client connected from {addr}")
            handle_client(conn)

if __name__ == "__main__":
    main()
