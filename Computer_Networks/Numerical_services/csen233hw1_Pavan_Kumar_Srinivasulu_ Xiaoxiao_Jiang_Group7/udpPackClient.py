import socket
import argparse
import sys


# runing foramt: python udpPackClient.py --port <port> --host <host> --num1 <int> --num2 <int> --op <["+","-","/","*"]>
def udp_client(server_host, server_port, num1, num2, operator):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_address = (server_host, server_port)

        try:
            senddata = pack(num1, num2, operator)
            client_socket.sendto(senddata, server_address)
            data, _ = client_socket.recvfrom(1024)
            unpack(data)
        finally:
            client_socket.close()
    except OverflowError as e:
        print(f"Invalid input: {e}")
    except socket.error as e:
        print(f"Network error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


def pack(num1, num2, operator):
    try:
        num1 = signed_to_unsigned(num1)
        num2 = signed_to_unsigned(num2)
        packdata = bytearray(socket.htonl(num1).to_bytes(4, "big"))
        packdata += bytearray(socket.htonl(num2).to_bytes(4, "big"))
        packdata += operator.encode()
        return packdata
    except OverflowError:
        raise OverflowError()


def unpack(data):
    try:
        resStatusCode = socket.ntohl(int.from_bytes(data[0:4], "big"))
        if resStatusCode != 200:
            error_message = data[4:].decode()
            print("Server Error:", error_message)
            return
        result = socket.ntohl(int.from_bytes(data[4:8], "big"))
        result = unsigned_to_signed(result)
        print("Server response:", result)
        return result
    except ValueError as e:
        raise ValueError(f"Error unpacking data: {e}")


def signed_to_unsigned(num):
    return num & 0xFFFFFFFF


def unsigned_to_signed(num):
    if num >= 2**31:
        num -= 2**32
    return num


def int32_type(x):
    x = int(x)
    if -(2**31) <= x <= 2**31 - 1:
        return x
    raise argparse.ArgumentTypeError(f"{x} is out of the 32-bit integer range")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Client for performing basic arithmetic operations over UDP."
    )
    parser.add_argument(
        "--host", required=True, help="Hostname or IP address of the server"
    )
    parser.add_argument(
        "--port", required=True, type=int, help="Port number of the server"
    )
    parser.add_argument("--num1", required=True, type=int32_type, help="First number")
    parser.add_argument("--num2", required=True, type=int32_type, help="Second number")
    parser.add_argument(
        "--operator",
        required=True,
        choices=["+", "-", "*", "/"],
        help="Arithmetic operator",
    )

    try:
        args = parser.parse_args()
        udp_client(args.host, args.port, args.num1, args.num2, args.operator)
    except ValueError as e:
        print(f"Input error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)
