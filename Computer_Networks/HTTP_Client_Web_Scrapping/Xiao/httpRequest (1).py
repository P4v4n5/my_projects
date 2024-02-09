# Author: Xiaoxiao Jiang
# Email: xjiang3@scu.edu
# Description: A simple script to send HTTP requests using sockets.

import logging
import socket

logging.basicConfig(level=logging.INFO)

URL = "neverssl.com"


def send_request():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((URL, 80))

        request = (
            "GET / HTTP/1.1\r\n"
            "Host: neverssl.com\r\n"
            "Connection: close\r\n"
            "User-Agent: MyHttpClient\r\n"
            "\r\n"
        )
        s.send(request.encode())

        response_parts = []
        while True:
            part = s.recv(4096)
            if not part:
                break
            response_parts.append(part.decode())
        response = "".join(response_parts)

        logging.info("Received response:\n%s", response)

    except Exception as e:
        logging.error("An error occurred: %s", e)
    finally:
        s.close()


if __name__ == "__main__":
    send_request()
