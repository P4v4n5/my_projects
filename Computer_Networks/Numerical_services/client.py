# maintainer: pavankumarrs099@gmail.com

# import socket
#
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect((socket.gethostname(), 1234))
#
# full_msg = ""
# while True:
#     msg = s.recv(8)
#     if len(msg) <= 0:
#         break
#     full_msg += msg.decode("utf-8")
#
# print(full_msg)

import socket
import json

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 1234))

def send_request(data):
    s.send(json.dumps(data).encode("utf-8"))

def receive_response():
    return json.loads(s.recv(1024).decode("utf-8"))

try:
    num1 = int(input("Enter the first number: "))
    num2 = int(input("Enter the second number: "))
    operator = input("Enter the operator (+, -, *, /): ")

    request_data = {
        "num1": num1,
        "num2": num2,
        "operator": operator
    }

    send_request(request_data)
    response = receive_response()

    if "result" in response:
        print(f"Result: {response['result']}")
    elif "error" in response:
        print(f"Error: {response['error']}")

except Exception as e:
    print(f"Error: {str(e)}")

finally:
    s.close()
