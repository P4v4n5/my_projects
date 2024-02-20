import socket
import sys

# run: python udpPackServer.py

# Constants
DATA_LENGTH = 9
PORT = 3002
BUFFER_SIZE = 1024
ERROR_MESSAGES = {
    200: "OK",
    400: "Bad Request",
    401: "Integer overflow",
    402: "Unknown error",
}


def udp_server():
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    bind_to_local(udp_socket)
    while True:
        try:
            data, addr = udp_socket.recvfrom(BUFFER_SIZE)
            print("Connection From:", addr)
            result, status_code = process_request(data)
            senddata = pack(result, status_code)
            udp_socket.sendto(senddata, addr)
        except KeyboardInterrupt:
            print("\nServer stopped.")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")


def bind_to_local(udp_socket):
    try:
        local_ip = socket.gethostbyname(socket.gethostname())
    except socket.gaierror:
        local_ip = "127.0.0.1"

    udp_socket.bind((local_ip, PORT))
    print(f"{local_ip} accepting datagram at port {PORT}")


def process_request(data):
    try:
        num1, num2, op = unpack(data)
        result = process_operation(num1, num2, op)
        return result, 200
    except ValueError as e:
        print(f"Data error: {e}")
        return ERROR_MESSAGES[400], 400
    except OverflowError as e:
        print(f"Arithmetic overflow: {e}")
        return ERROR_MESSAGES[401], 402
    except Exception as e:
        print(f"Unexpected error: {e}")
        return ERROR_MESSAGES[402], 403


def unpack(data):
    # input data format shall be like
    # | num1(4bytes) | num2(4bytes) | op(1byte) |
    if len(data) != DATA_LENGTH:
        raise ValueError("Invalid data")
    num1 = socket.ntohl(int.from_bytes(data[0:4], "big"))
    num2 = socket.ntohl(int.from_bytes(data[4:8], "big"))
    num1 = unsigned_to_signed(num1)
    num2 = unsigned_to_signed(num2)
    operator = data[8:9].decode()
    return num1, num2, operator


def process_operation(num1, num2, op):
    if op == "+":
        result = num1 + num2
    elif op == "-":
        result = num1 - num2
    elif op == "*":
        result = num1 * num2
    elif op == "/":
        if num2 == 0:
            raise ValueError("Division by zero")
        result = num1 // num2
    else:
        raise ValueError("Invalid operator")

    # Check for integer overflow
    if result.bit_length() > 31:
        raise OverflowError("Integer overflow")

    return result


def pack(result, status_code):
    packdata = bytearray(socket.htonl(status_code).to_bytes(4, "big"))
    if status_code != 200:
        packdata += ERROR_MESSAGES[status_code].encode()
    else:
        result = signed_to_unsigned(result)
        packdata += bytearray(socket.htonl(result).to_bytes(4, "big"))
    return packdata


def signed_to_unsigned(num):
    return num & 0xFFFFFFFF


def unsigned_to_signed(num):
    if num >= 2**31:
        num -= 2**32
    return num


if __name__ == "__main__":
    udp_server()
