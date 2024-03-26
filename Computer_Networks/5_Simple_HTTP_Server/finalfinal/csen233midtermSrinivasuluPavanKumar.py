# Maintainer: Srinivasulu Xiaoxiao Kumar
# Email: psrinivasulu@scu.edu

import socket
import sys
import logging
import random

logging.basicConfig(filename='csen233midtermSrinivasuluPavanKumar.txt', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def create_response(status_code, content):
    response = f"HTTP/1.1 {status_code}\r\n"
    response += "Content-Type: text/html\r\n"
    response += "\r\n"
    response += content
    return response


def main():
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_port = 8200
        server_socket.bind(('', server_port))
        server_socket.listen(1)
        local_ip = socket.gethostbyname(socket.gethostname())
        logging.info(f"Server started, listening on {local_ip}:{server_port}")
        print(f"Use the URL to connect to server: http://{local_ip}:{server_port}")

        while True:
            logging.info('Waiting for connection...')
            connection_socket, addr = server_socket.accept()
            try:
                message = connection_socket.recv(1024).decode()
                # Randomly choose whether to send a normal response or an error
                if random.random() < 0.5:
                    # 50% - 200 OK response
                    response_content = "<html><body><h2>Hello!</h2><h3>This is a sample HTML.</h3></body></html>"
                    response = create_response("200 OK", response_content)
                    connection_socket.send(response.encode())
                    logging.info(f"Sent normal response to {addr}")
                    logging.info(f"Responding with success: {response}")
                else:
                    # 50% - Either 404 or 500 Error
                    if random.random() < 0.5:
                        response_content = "<html><body><h1>404 Not Found</h1></body></html>"
                        response = create_response("404 Not Found", response_content)
                        connection_socket.send(response.encode())
                        logging.error(f"Sent error response (404 Not Found) to {addr}")
                        logging.info(f"Responding with success: {response}")
                    else:
                        response_content = "<html><body><h1>500 Internal Server Error</h1></body></html>"
                        response = create_response("500 Internal Server Error", response_content)
                        connection_socket.send(response.encode())
                        logging.error(f"Sent error response (500 Internal Server Error) to {addr}")
                        logging.info(f"Responding with success: {response}")


            finally:
                connection_socket.close()
                logging.info(f"Connection with {addr} closed")

    except KeyboardInterrupt:
        logging.info("Server shutdown initiated")
        server_socket.close()
        logging.info("Server shut down")
        sys.exit()


if __name__ == "__main__":
    main()
