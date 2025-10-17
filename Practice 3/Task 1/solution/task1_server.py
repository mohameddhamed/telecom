import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # ipv4, TCP

server_addr = ("", 10001)  # ('localhost',10000) <- igy csak localhoston fogad

sock.bind(server_addr)
sock.listen(1)
# sock.settimeout(1.0)	# windowson

while True:
    try:
        print("Waiting...")
        client_socket, client_addr = sock.accept()

        print("Connected: ", client_addr)

        data = client_socket.recv(16)
        print("Received:", data.decode())
        if data:
            client_socket.send("Hello Client!".encode())
        else:
            print("Disconnected")

        client_socket.close()

    #  except socket.timeout:
    #    pass
    except KeyboardInterrupt:
        sock.close()
        break
