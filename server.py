import socket
import threading

HOST = "192.168.0.25"
PORT = 9898

# This socket is AF_INET (IPv4) type, which corresponds to an internet socket.
# The SOCK_STREAM is the socket type, in this case the TCP protocol
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

clients = []
nicknames = []

def handle_user(client):
    while True:
        client_index = clients.index(client)
        client_nickname = nicknames[client_index]
        try:
            msg = client.recv(1024).decode("utf-8")
            formatted_msg = f"{client_nickname}: {msg}"
            print(formatted_msg)
            broadcast(formatted_msg)
        except:
            broadcast(f"{client} left the chat")
            nicknames.pop(client_index)
            clients.remove(client)
            client.close()



def broadcast(msg):
    for client in clients:
        client.send(msg.encode("utf-8"))



def listen():

    # listen to (up to 5) connections
    server.listen(5)
    print(f"Server listening on {HOST}:{PORT}")
    while True:

        # accept new connection
        current_socket, address = server.accept()
        client_nickname = current_socket.recv(1024).decode("utf-8")

        # load socket and nick
        nicknames.append(client_nickname)
        clients.append(current_socket)

        print(f"{client_nickname} {address} connected to the chat")
        broadcast(f"{client_nickname} {address} connected to the chat")
        
        # set thread to handle client
        thread = threading.Thread(target=handle_user, daemon=True, args=(current_socket,))
        thread.start()

listen()