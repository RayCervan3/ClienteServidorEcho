import socket
import threading


def wlan_ip():
    import subprocess
    result = subprocess.run('ipconfig', stdout=subprocess.PIPE, text=True).stdout.lower()
    scan = 0
    for i in result.split('\n'):
        if 'wireless' in i: scan = 1
        if scan:
            if 'ipv4' in i: return i.split(':')[1].strip()


IP = wlan_ip() 
PORT = 5555
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        try:
            msg = conn.recv(SIZE).decode(FORMAT)
            conn.send(msg.encode(FORMAT))
            print("|bytes:" + str(len(msg)) + "| cliente:" + str(addr[0]) + " |mensaje:" + msg)
        except:
            print(f"Cliente: {addr} desconectado")
            break
    conn.close()
    

def conexion():
    print("[STARTING] Server is starting...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING] Server is listening on {IP}:{PORT}")
    while True:
        conn, addr = server.accept()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


conexion()
