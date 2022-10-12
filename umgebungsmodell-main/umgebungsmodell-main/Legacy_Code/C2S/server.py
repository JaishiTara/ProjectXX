import socket
import threading

HOST = "127.0.0.1"
PORT = 65432
ADDR = (HOST, PORT)
FORMAT = "utf-8"
DISSCONNECT_MESSAGE = "!Disconnect"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
message = None


def handle_client(conn, addr):
    print(f"New Connection {addr} connected.")
    connected = True
    while connected:
        msg = conn.recv(1024).decode(FORMAT)
        if msg == DISSCONNECT_MESSAGE:
            connected = False
        print(msg)

        return
    conn.close()


def start():
    server.listen()
    print(f"Server is listening on {HOST}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTION] {threading.active_count() -1}")


print("Starting server...")
start()
