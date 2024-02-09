# Maintainer: GROUP - 5 | Kalle Meghana, Srinivasulu Pavan Kumar, Liu Weihao
# Eamil_ID's: mkalle@scu.edu, psrinivasulu@scu.edu, wliu4@scu.edu

import socket
import json
import threading
import time
import logging


class AuctionServer:
    def __init__(self, host='0.0.0.0', port=0):
        self.server_address = (host, port)
        self.clients = {}
        self.auction_state = {
            "highest_bid": 0,
            "highest_bidder": None,
            "n_clients": 0,
            "chant": 0,  # Initialize chant to 0 as it should change upon auction start or new highest bid
            "status": "OPEN",
            "next_auction": None
        }
        self.lock = threading.Lock()
        self.broadcast_thread = threading.Thread(target=self.broadcast_highest_bid, daemon=True)
        self.last_bid_time = None
        self.new_bid_since_last_broadcast = False  # Track if a new highest bid has been made since the last broadcast

        # Configure logging
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    def start(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(self.server_address)
        self.sock.listen()
        server_ip = socket.gethostbyname(socket.gethostname())
        self.logger.info(f"Server listening on {server_ip}:{self.sock.getsockname()[1]}")

        self.broadcast_thread.start()

        try:
            while True:
                client, address = self.sock.accept()
                threading.Thread(target=self.handle_client, args=(client, address)).start()
        finally:
            self.sock.close()

    def broadcast_highest_bid(self):
        while True:
            time.sleep(10)  # 10 second interval for broadcasting
            with self.lock:
                if self.last_bid_time and (time.time() - self.last_bid_time >= 30):
                    self.auction_state["status"] = "WINNER"
                    self.broadcast_status("CLOSE")
                    break
                if not self.new_bid_since_last_broadcast:
                    # Increment chant by 1 only if no new highest bid since last broadcast
                    self.auction_state["chant"] += 1
                else:
                    # Reset for the next cycle
                    self.new_bid_since_last_broadcast = False
                self.broadcast_status("STATUS")

    def broadcast_status(self, message_type):
        for client in self.clients.values():
            try:
                status_message = json.dumps({"request_type": message_type, **self.auction_state})
                client.sendall(status_message.encode('utf-8'))
            except Exception as e:
                self.logger.info(f"Error broadcasting message: {e}")

    def handle_client(self, client, address):
        with client:
            self.clients[address] = client
            self.auction_state["n_clients"] = len(self.clients)
            self.logger.info('Accepting connection form {}'.format(address))
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
            # self.logger.error("Error decoding JSON from client")

    def handle_join(self, client, address):
        client.sendall(json.dumps({"request_type": "STATUS", **self.auction_state}).encode('utf-8'))

    def handle_bid(self, message_data, client, address):
        with self.lock:
            bid_amount = message_data.get("bid_amount")
            if bid_amount and bid_amount > self.auction_state['highest_bid']:
                self.auction_state["highest_bid"] = bid_amount
                self.auction_state["highest_bidder"] = str(str(address[0]) + ':' + str(address[1]))
                self.auction_state["chant"] = 1  # Reset chant to 1 on new highest bid
                self.last_bid_time = time.time()
                self.new_bid_since_last_broadcast = True  # Indicate a new bid has been placed
                response = {"request_type": "BID_ACK", "bid_status": "ACCEPTED"}
            else:
                response = {"request_type": "BID_ACK", "bid_status": "REJECTED"}
            client.sendall(json.dumps(response).encode('utf-8'))


if __name__ == "__main__":
    logging.basicConfig(filename='auction_host_LogFile_Group5.log', level=logging.DEBUG)
    server = AuctionServer()
    server.start()
