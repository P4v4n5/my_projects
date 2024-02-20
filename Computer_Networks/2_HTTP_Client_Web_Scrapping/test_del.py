import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("httpbin.org", 80))
sock.send(b"GET / HTTP/1.1\r\nHost:httpbin.org\r\n\r\n")
response = sock.recv(4096)
sock.close()
print(response.decode())