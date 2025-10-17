import socket
from select import select
import queue
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR, error

server_address = ("", 10000)

server = socket(AF_INET, SOCK_STREAM)
server.settimeout(1.0)
server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

server.bind(server_address)

server.listen(5)

inputs = [server]

msg_q = queue.Queue()
username = {}

while inputs:
    timeout = 1
    readable, writeable, exceptable = select(inputs, inputs, inputs, timeout)

    if not (readable or writeable or exceptable):
        continue

    for s in readable:
        try:
            if s is server:
                client, client_addr = s.accept()
                client.setblocking(1)
                name = client.recv(20).decode().strip()
                print("Client connected: ", name, client_addr)
                username[client] = name
                inputs.append(client)
                msg_q.put((name, "has logged in"))
            else:
                data = s.recv(200).strip()
                if data:
                    msg_q.put((username[s], data.decode()))
                else:
                    print("Client disconnected")
                    msg_q.put((username[s], "has logged out"))
                    inputs.remove(s)
                    if s in writeable:
                        writeable.remove(s)
                    s.close()
        except error as m:
            print("Error", m)
            inputs.remove(s)
            if s in writeable:
                writeable.remove(s)
            s.close()

    while not msg_q.empty():
        try:
            next_msg = msg_q.get_nowait()
            print("msg", next_msg)
        except Queue.Empty:
            break
        else:
            for s in writeable:
                if not username[s] == next_msg[0]:
                    s.sendall(("[" + next_msg[0] + "] " + next_msg[1]).encode())
                    print("Send", username[s])
