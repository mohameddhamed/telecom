import socket
import sys
from input_timeout import readInput
from socket import socket, AF_INET, SOCK_STREAM, timeout, error

username = sys.argv[1]


def prompt(nl):
    if nl:
        print("")
    print("<" + username + ">")


server_address = ("localhost", 10000)

client = socket(AF_INET, SOCK_STREAM)

client.connect(server_address)
client.sendall(username.encode())
client.settimeout(1.0)
prompt(False)

while True:
    try:
        data = client.recv(200)
        if not data:
            print("Server down")
            sys.exit()
        else:
            print(data.decode())
            sys.stdout.flush()
            prompt(False)
    except SystemExit as m:
        client.close()
        break
    except timeout:
        pass
    except error as e:
        print("Error", e)
        break

    try:
        msg = readInput()
        msg = msg.strip()
        if msg != "":
            client.sendall(msg.encode())
            prompt(True)
    except timeout:
        pass
    except error as e:
        print(e)
        break
