import socket
import json
import threading

def create_message(request_type, **kwargs):
    message = {"request_type": request_type}
    message.update(kwargs)
    return json.dumps(message)

def listen_for_updates(client_socket):
    while True:
        try:
            response = client_socket.recv(4096).decode('utf-8')
            if response:
                print("\nServer response:", response)
                print("Enter your bid amount or 'quit' to exit: ", end='', flush=True)
            else:
                break
        except Exception as e:
            print(f"Error receiving message from server: {e}")
            break

def connect_to_server(server_ip, server_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))
    return client_socket

def send_message(client_socket, message):
    try:
        client_socket.sendall(message.encode('utf-8'))
    except Exception as e:
        print(f"Error sending message to server: {e}")

if __name__ == "__main__":
    server_ip = input("Enter the server IP address: ")
    server_port = int(input("Enter the server port: "))
    client_socket = connect_to_server(server_ip, server_port)
    
    # Start listening for updates in a separate thread
    threading.Thread(target=listen_for_updates, args=(client_socket,), daemon=True).start()

    try:
        join_message = create_message("JOIN")
        send_message(client_socket, join_message)
        
        while True:
            bid_amount = input("Enter your bid amount or 'quit' to exit: ")
            if bid_amount.lower() == 'quit':
                break
            try:
                bid_message = create_message("BID", bid_amount=int(bid_amount))
                send_message(client_socket, bid_message)
            except ValueError:
                print("Please enter a valid number.")
    finally:
        client_socket.close()
# 129.210.245.76