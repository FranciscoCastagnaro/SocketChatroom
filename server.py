import socket
import threading

HOST = "192.168.0.25"
PORT = 9898

# This socket is AF_INET (IPv4) type, which corresponds to an internet socket.
# The SOCK_STREAM is the socket type, in this case the TCP protocol
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

broadcast_list = []
address_nickname = {}

def handle_user(socket_con, address):
    while True:
        msg = socket_con.recv(1024).decode("utf-8")
        formatted_msg = f"{address_nickname[address]}: {msg}"
        print(formatted_msg)
        broadcast(formatted_msg)

def broadcast(msg):
    for sock in broadcast_list:
        sock.send(msg.encode("utf-8"))

server.listen(5)
print(f"Server listening on {HOST}:{PORT}")
while True:

    current_connection_socket, address = server.accept()
    address_nickname[address] = current_connection_socket.recv(1024).decode("utf-8")
    broadcast_list.append(current_connection_socket)
    print(f"{address_nickname[address]} {address} connected to the chat")
    broadcast(f"{address_nickname[address]} {address} connected to the chat")
    
    thread = threading.Thread(target=handle_user, daemon=True, args=[current_connection_socket, address])
    thread.start()
