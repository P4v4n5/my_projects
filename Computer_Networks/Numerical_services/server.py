# maintainer: pavankumarrs099@gmail.com

# import socket
#
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.bind((socket.gethostname(), 1234))
# s.listen(5)
#
# while True:
#     clientsocket, address = s.accept()
#     print(f"Connection from {address} is established!!")
#     clientsocket.send(bytes("welcome to the server", "utf-8"))
#     clientsocket.close()

import socket
import json

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 1234))
s.listen(5)


def perform_operation(data):
    try:
        num1 = data["num1"]
        num2 = data["num2"]
        operator = data["operator"]

        if operator == "+":
            result = num1 + num2
        elif operator == "-":
            result = num1 - num2
        elif operator == "*":
            result = num1 * num2
        elif operator == "/":
            if num2 == 0:
                raise ValueError("Division by zero error")
            result = num1 / num2
        else:
            raise ValueError("Invalid operator")

        return {"result": result}

    except Exception as e:
        return {"error": str(e)}


while True:
    clientsocket, address = s.accept()
    print(f"Connection from {address} is established!!")

    try:
        data = json.loads(clientsocket.recv(1024).decode("utf-8"))
        response = perform_operation(data)
        clientsocket.send(json.dumps(response).encode("utf-8"))
    except Exception as e:
        error_response = {"error": str(e)}
        clientsocket.send(json.dumps(error_response).encode("utf-8"))

    clientsocket.close()
