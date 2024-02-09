import socket
import json
import threading
import time

class AuctionServer:
    def __init__(self, host='0.0.0.0', port=0):
        self.server_address = (host, port)
        self.clients = {}
        self.auction_state = {
            "highest_bid": 0,
            "highest_bidder": None,
            "n_clients": 0,
            "chant": None,
            "status": "OPEN",
            "next_auction": None  # Set this to the Unix timestamp of the next auction or leave as None
        }
        self.lock = threading.Lock()
        self.broadcast_thread = threading.Thread(target=self.broadcast_highest_bid, daemon=True)
        self.last_bid_time = None

    # IP / Port
    def start(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(self.server_address)
        self.sock.listen()
        server_ip = socket.gethostbyname(socket.gethostname())
        print(f"Server listening on {server_ip}:{self.sock.getsockname()[1]}")
        
        self.broadcast_thread.start()
        
        try:
            while True:
                client, address = self.sock.accept()
                threading.Thread(target=self.handle_client, args=(client, address)).start()
        finally:
            self.sock.close()

    def broadcast_highest_bid(self):
        broadcast_count = 0
        while True:
            time.sleep(10)  # 10 second
            with self.lock:
                if self.last_bid_time and (time.time() - self.last_bid_time >= 30):
                    # 30 sec count if no new bid
                    self.auction_state["status"] = "CLOSED"
                    self.broadcast_status("CLOSE")
                    break
                elif self.last_bid_time:
                    broadcast_count += 1
                    self.auction_state["chant"] = broadcast_count
                else:
                    self.auction_state["chant"] = None
                self.broadcast_status("STATUS")


    def broadcast_status(self, message_type):
        for client in self.clients.values():
            try:
                status_message = json.dumps({"request_type": message_type, **self.auction_state})
                client.sendall(status_message.encode('utf-8'))
            except Exception as e:
                print(f"Error broadcasting message: {e}")

    def handle_client(self, client, address):
        with client:
            self.clients[address] = client
            self.auction_state["n_clients"] = len(self.clients)
            try:
                while True:
                    data = client.recv(1024)
                    if not data:
                        break
                    self.process_message(data.decode('utf-8'), client, address)
            finally:
                del self.clients[address]
                self.auction_state["n_clients"] = len(self.clients)

    def process_message(self, message, client, address):
        try:
            message_data = json.loads(message)
            request_type = message_data.get("request_type")
            if request_type == "JOIN":
                self.handle_join(client, address)
            elif request_type == "BID":
                self.handle_bid(message_data, client, address)
        except json.JSONDecodeError:
            client.sendall("HTTP/1.1 400 Bad Request\r\n\r\n".encode('utf-8'))

    def handle_join(self, client, address):
        client.sendall(json.dumps({"request_type": "STATUS", **self.auction_state}).encode('utf-8'))

    def handle_bid(self, message_data, client, address):
        with self.lock:
            bid_amount = message_data.get("bid_amount")
            if bid_amount and bid_amount > self.auction_state['highest_bid']:
                self.auction_state["highest_bid"] = bid_amount
                self.auction_state["highest_bidder"] = str(address[0])
                self.auction_state["chant"] = 1
                self.last_bid_time = time.time()
                response = {"request_type": "BID_ACK", "bid_status": "ACCEPTED"}
            else:
                response = {"request_type": "BID_ACK", "bid_status": "REJECTED"}
            client.sendall(json.dumps(response).encode('utf-8'))

if __name__ == "__main__":
    server = AuctionServer()
    server.start()
