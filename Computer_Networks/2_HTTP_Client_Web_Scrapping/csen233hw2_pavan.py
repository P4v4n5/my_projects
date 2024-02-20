# Maintainer: Pavan Kumar Srinivasulu
# Email: psrinivasulu@scu.edu

import logging
import socket

# Set up logging with UTF-8 encoding
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler('log_file_pavan.txt', encoding='utf-8')])


def send_request(url):
    try:
        p = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        p.connect((url, 80))

        request = (
            "GET / HTTP/1.1\r\n" 
            "Host: {0}\r\n"  # httpbin.org
            "Connection: close\r\n"
            "User-Agent: MyHttpClient\r\n"
            "\r\n"
        ).format(url)

        p.send(request.encode())

        response_parts = []
        while True:
            part = p.recv(4096)
            if not part:
                break
            response_parts.append(part.decode())
        response = "".join(response_parts)

        logging.info("Response is received successfully :\n%s", response)

    except Exception as e:
        logging.error("An Error occurred: %s", e)
    finally:
        logging.info("Fetching the data completed successfully")
        print("Log file is generated in the preset working directory with file name --> log_file_pavan.txt")
        p.close()


if __name__ == "__main__":
    path = "/"  # all the content. If incase you want to fetch only html content, then path should be given as /html
    url = "httpbin.org"  # sample url
    send_request(url)
