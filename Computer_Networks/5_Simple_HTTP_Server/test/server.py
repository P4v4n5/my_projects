#import socket module
from socket import *
import sys  # In order to terminate the program
import logging

logging.basicConfig(filename='csen233midtermJiangXi.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

try: 
    serverSocket = socket(AF_INET, SOCK_STREAM)
    # Prepare a server socket
    serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    filename = 'HelloWorld.html'
    serverPort = 8100
    serverSocket.bind(('', serverPort))
    serverSocket.listen(1)
    hostname = gethostname()
    local_ip = gethostbyname(hostname)
    logging.info(f"Server started, listening on {local_ip}:{serverPort}")
    print(f"Use the URL to connect to server: http://{local_ip}:{serverPort}/{filename}")

    while True:
        logging.info('Ready to serve...')
        print('Ready to serve...')
        connectionSocket, addr = serverSocket.accept()
        try:
            message = connectionSocket.recv(1024).decode()
            filename = message.split()[1]
            f = open(filename[1:])
            outputdata = f.read()
            
            # Send HTTP header line into socket
            response_header = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"
            connectionSocket.send(response_header.encode())
            
            # Send the content of the requested file to the client
            for i in range(0, len(outputdata)):
                connectionSocket.send(outputdata[i].encode())
            connectionSocket.send("\r\n".encode());
            connectionSocket.close()
            logging.info(f"Sent {filename} to {addr}")

        except IOError as e:
            # Send response message for file not found
            not_found_response = "HTTP/1.1 404 Not Found\r\n\r\n"
            connectionSocket.send(not_found_response.encode())
            connectionSocket.send("<html><body><h1>404 Not Found</h1></body></html>".encode())
            logging.warning(f"Failed to open {filename}: {e}, requested by {addr}")

        finally:
            # Close client socket
            connectionSocket.close()
            logging.info(f"Connection with {addr} closed")

except KeyboardInterrupt:
    logging.info("Server shutdown initiated")
    serverSocket.close()
    logging.info("Server shut down")
    sys.exit()
