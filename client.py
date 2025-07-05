import socket
import threading

HOST = "192.168.0.25"
PORT = 9898

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect((HOST, PORT))

nickname = input("Insert your nickname: ")
socket.send(nickname.encode("utf-8"))

def hear():
    try:
        while True:
            msg = socket.recv(1024).decode("utf-8")
            print(msg)
    except:
        print("Connection with server closed")

def talk():
    while True:
        msg = input()
        socket.send(msg.encode("utf-8"))

threading.Thread(target=hear, daemon=True).start()
talk()



