import socket
import logging

def fetch_object_from_web_server(url, port, path):
    # Creating a logger
    logger = logging.getLogger(__name__)

    try:
        # Log start of the function
        logger.info(f"Fetching content from the web server. URL: {url}, Port: {port}")

        # Creating a TCP socket
        with socket.create_connection((url, port)) as s:
            # Constructing HTTP request
            request = f"GET {path} HTTP/1.1\r\nHost: {url}\r\nConnection: Close\r\nUser-Agent: Mozilla\r\nAccept-language: en-US\r\n\r\n"
            
            # Log sending HTTP request
            logger.info(f"Sending HTTP request:\n{request}")

            # Sending the request
            s.sendall(request.encode())

            # Receive and log the response
            buffer_size = 1024
            response_data = b""
            while True:
                chunk = s.recv(buffer_size)
                if not chunk:
                    break
                response_data += chunk
            logger.info(f"Received response:\n{response_data.decode()}")

    except socket.error as e:
        logger.error(f"Socket error: {e}")

    except Exception as e:
        logger.error(f"An error occurred: {e}")
    
    finally:
        # Log completion of the function
        logger.info("Content fetching is completed.")
        print("Log file is generated")

if __name__ == "__main__":

    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[logging.FileHandler('log_file.txt')])

    # Specifying the URL and port
    url = "www.sneaindia.com"
    port_to_use = 80
    path = '/index.php'

    # Fetching content from the web server
    fetch_object_from_web_server(url, port_to_use, path)
