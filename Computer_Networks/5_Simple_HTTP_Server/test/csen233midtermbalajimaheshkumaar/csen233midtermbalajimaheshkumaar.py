"""
Name - Mahesh Kumaar Balaji
Email - mbalaji@scu.edu
"""


import socket
import random
import traceback
from logger import Logger, LoggingLevel
from payload import HttpRequest, HttpResponse


SERVER_HOST = "localhost"
PORT_NUMBER = random.randint(10000, 60000)
MAXIMUM_ALLOWED_CONNECTIONS = 1
PAGES_TO_BE_SERVED = ["index.html", "NotFound.html"]


def getRandomFile() -> str:
    randomNumber: int = random.randint(1, 100)
    randomNumber = randomNumber % 2
    return PAGES_TO_BE_SERVED[randomNumber]


def getTextFileContents(file_name: str) -> str:
    with open(file_name, "r") as my_file:
        file_contents = "".join(my_file.readlines())
    return file_contents


if __name__ == "__main__":
    log_file = Logger.set_configuration("f")
    server_socket = None
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((SERVER_HOST, PORT_NUMBER))
        server_socket.listen(MAXIMUM_ALLOWED_CONNECTIONS)
        Logger.logentry("==========================================================")
        Logger.logentry(f"Web server is listening at {SERVER_HOST}:{PORT_NUMBER}.")
        print(f"Web server is listening at {SERVER_HOST}:{PORT_NUMBER}.")
        while True:
            client_socket, client_address = server_socket.accept()
            Logger.logentry(f"A new client - {client_address} has connected to the server.")
            received_data = client_socket.recv(2048)
            received_string = received_data.decode()
            httpRequest = HttpRequest()
            httpRequest.parse(received_string)
            Logger.logentry(f"New request received from {client_address}:>\n{received_string}")
            httpResponse = HttpResponse()
            if httpRequest.RequestMethod.upper() == "GET":
                FileName = getRandomFile()
                FileContents = getTextFileContents(FileName)
                if FileName == PAGES_TO_BE_SERVED[0]:
                    httpResponse.StatusCode = "200"
                    httpResponse.StatusMessage = "OK"
                else:
                    httpResponse.StatusCode = "404"
                    httpResponse.StatusMessage = "Not Found"
                httpResponse.Headers.update({"Content-Type": "text/html"})
                httpResponse.Body = FileContents
            else:
                httpResponse.StatusCode = "405"
                httpResponse.StatusMessage = "Not Allowed"
                httpResponse.Headers.update({"Content-Type": "text/plain"})
                httpResponse.Body = "The HTTP method requested is not currently allowed by the server."
            response_string = str(httpResponse)
            client_socket.sendall(response_string.encode())
            Logger.logentry(f"Response being sent back:>\n{response_string}")
            Logger.logentry("==========================================================")
            client_socket.close()
    except KeyboardInterrupt:
        Logger.logentry("'EXIT' command received :> Shutting down the server now.")
    except socket.error:
        Logger.logentry(f"Client has disconnected from the server.")
    except Exception as global_ex:
        Logger.logentry(f"Exception occurred while processing HTTP requests from client: {global_ex}", LoggingLevel.CRITICAL)
        traceback.print_exc()
    finally:
        if server_socket is not None:
            server_socket.close()
