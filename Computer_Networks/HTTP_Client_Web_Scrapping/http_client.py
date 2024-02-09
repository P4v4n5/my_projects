import socket
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def fetch_web_object(host, path="/html"):
    # Connect to the web server using TCP
    try:
        with socket.create_connection((host, 80), timeout=50) as s:
            # Construct HTTP request
            request = f"GET {path} HTTP/1.1\r\nHost: {host}\r\n\r\n"

            # Send the request
            s.sendall(request.encode())

            # Receive and log the response
            response = s.recv(4096).decode()
            logging.info(f"Received response:\n{response}")

    except (socket.error, TimeoutError) as e:
        logging.error(f"Error connecting to the server: {e}")


if __name__ == "__main__":
    # Replace 'example.com' with the desired web server
    web_server = 'httpbin.org'
    fetch_web_object(web_server)


# import socket
# # import logging
# #
# # logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
#
# def fetch_web_object(host, path="/html"):
#     # Connect to httpbin.org using TCP
#     try:
#         with socket.create_connection((host, 80), timeout=5) as s:
#             # Construct HTTP request
#             request = f"GET {path} HTTP/1.1\r\nHost: {host}\r\n\r\n"
#
#             # Send the request
#             s.sendall(request.encode())
#
#             # Receive and print the response
#             response = s.recv(4096).decode()
#             print(f"Received response:\n{response}")
#
#     except (socket.error, TimeoutError) as e:
#         print(f"Error connecting to the server: {e}")
#
#
# if __name__ == "__main__":
#     # Use httpbin.org as the web server
#     web_server = 'httpbin.org'
#     fetch_web_object(web_server)

