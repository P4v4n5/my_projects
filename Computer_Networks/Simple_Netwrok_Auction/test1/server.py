import math
import socket
import json
import threading
import time
import logging
from datetime import date, timedelta

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

today = date.today()
day_after_tomorrow = today + timedelta(days=2)
day_after_tomorrow_date = day_after_tomorrow.strftime("%m/%d/%Y")

clients = set()
join_set = set()
highest_bid = 0
highest_bidder = None
chant = 0
last_bid_time = None
bid_lock = threading.Lock()
is_closed = False

MESSAGE = {
    200: 'OK',
    400: 'Bad Request',
    503: 'Service Unavailable'
}

status_msg = {
    "request_type": "STATUS",
    "status": "OPEN",
    "highest_bid": highest_bid,
    "highest_bidder": highest_bidder,
    "chant": 0,
    "n_clients": 0,
    "next_auction": day_after_tomorrow_date
}

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def handle_request(client_address, request):
    global highest_bid, highest_bidder, chant, last_bid_time
    request_json = json.loads(request.split('\r\n\r\n')[-1])
    data = None
    status_code = 200

    if request_json["request_type"] == "JOIN":
        data = status_msg
        join_set.add(client_address)
    elif request_json["request_type"] == "BID":
        new_bid = request_json.get("bid_amount")
        if new_bid is not None:
            with bid_lock:
                if new_bid > highest_bid and not is_closed and client_address in join_set:
                    highest_bid = new_bid
                    highest_bidder = client_address
                    last_bid_time = time.time()
                    chant = 0
                    data = {"request_type": "BID_ACK", "bid_status": "ACCEPTED"}
                else:
                    data = {"request_type": "BID_ACK", "bid_status": "REJECTED"}
                    status_code = 400
        else:
            status_code = 400
            data = {"error": "Missing bid amount"}

    return build_http_response(status_code, data);


def build_http_response(status_code, data):
    body = json.dumps(data)
    return (
        f"HTTP/1.1 {status_code} {MESSAGE[status_code]}\r\n"
        "Content-Type: application/json\r\n"
        f"Content-Length: {len(body)}\r\n"
        "\r\n"
        f"{body}"
    )


def broadcast_status():
    global highest_bid, highest_bidder, clients, chant, last_bid_time, is_closed
    while True:
        time.sleep(0.01)
        with (bid_lock):
            tmp = time.time()
            if last_bid_time is None or math.floor((time.time() - last_bid_time) / 10) <= chant or is_closed:
                continue
            if chant < 3:
                chant += 1
            status_msg.update({
                "highest_bid": highest_bid,
                "highest_bidder": highest_bidder,
                "n_clients": len(clients),
                "chant": chant
            })

            if chant == 3:
                is_closed = True
                close_msg = {"request_type": "CLOSE", "highest_bid": highest_bid, "highest_bidder": highest_bidder}
                response = build_http_response(503, close_msg)
                for client in clients:
                    try:
                        client.sendall(response.encode('utf-8'))
                        client.close()
                    except Exception as e:
                        logger.error(f"Error broadcasting to {client}: {e}")
                        clients.remove(client)
                logger.info('Auction End')
                break

            for client in clients:
                try:
                    response = build_http_response(200, status_msg)
                    client.sendall(response.encode('utf-8'))
                except Exception as e:
                    logger.error(f"Error broadcasting to {client}: {e}")
                    clients.remove(client)


def handle_client_connection(client_socket, client_address):
    global highest_bid, highest_bidder, clients
    logger.info(f"New connection from {client_address}")
    with bid_lock:
        clients.add(client_socket)
    try:
        while True:
            data = client_socket.recv(1024).decode('utf-8')
            response = handle_request(client_address, data)
            client_socket.sendall(response.encode('utf-8'))
    except Exception as e:
        logger.error(f"Error handling connection from {client_address}: {e}")
    finally:
        with bid_lock:
            clients.remove(client_socket)
        client_socket.close()
        logger.info(f"Connection closed for {client_address}")


def start_server(host='127.0.0.1', port=8000):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen()
    logger.info(f"Listening on {host}:{port}")

    broadcast_thread = threading.Thread(target=broadcast_status)
    broadcast_thread.start()

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            client_thread = threading.Thread(target=handle_client_connection, args=(client_socket, client_address))
            client_thread.start()
    except KeyboardInterrupt:
        logger.info("Caught keyboard interrupt, exiting")
    finally:
        server_socket.close()


if __name__ == '__main__':
    start_server()
