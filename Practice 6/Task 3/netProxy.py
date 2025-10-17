import sys
import socket

# --- Configuration ---
TARGET_HOST = sys.argv[1]
PROXY_PORT = int(sys.argv[2])
TARGET_PORT = 80  # Standard HTTP port
BUFFER_SIZE = 4096
FORBIDDEN_STRING = b"SzamHalo"

# A pre-made HTTP 404 response to send when content is blocked.
HTTP_404_RESPONSE = b"""\
HTTP/1.1 404 Not Found\r\n\
Content-Type: text/html\r\n\
Connection: close\r\n\
\r\n\
<html>\
<body>\
<h1>404 Not Found</h1>\
<p>Content blocked by SzamHalo proxy.</p>\
</body>\
</html>
"""

# --- Main Proxy Logic ---

# TODO 1: Create the main TCP listening socket for the proxy.
# Use socket.AF_INET and socket.SOCK_STREAM.
listen_sock = # ...

# This allows you to restart the proxy server quickly.
listen_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# TODO 2: Bind the listening socket to the proxy's address ('localhost') and port.
# ...

# TODO 3: Set the socket to listen for incoming connections.
# ...

print(f"Proxy server listening on localhost:{PROXY_PORT}")
print(f"Forwarding requests to {TARGET_HOST}:{TARGET_PORT}")

while True:
    try:
        # TODO 4: Accept a new connection from a client (the web browser).
        # .accept() returns a new socket for the connection and the client's address.
        browser_sock, browser_addr = # ...
        print(f"Accepted connection from {browser_addr}")

        # Handle the connection in a 'with' block for automatic cleanup.
        with browser_sock:
            # --- Step 1: Receive the request from the browser ---
            # TODO 5: Receive the browser's full HTTP request.
            # HTTP requests can be larger than our buffer, so receive in a loop.
            # A simple approach is to receive one chunk, as browsers usually
            # send the request in a single packet for simple GETs.
            request_data = # ...

            if not request_data:
                continue

            print(f"-> Received request from browser:\n---\n{request_data.decode(errors='ignore')}---")

            # --- Step 2: Forward the request to the target server ---
            
            # TODO 6: Create a new client socket to connect to the target web server.
            server_sock = # ...

            with server_sock:
                # TODO 7: Connect this new socket to the TARGET_HOST on TARGET_PORT.
                # ...

                # TODO 8: Send the browser's original request to the target server.
                # ...

                # --- Step 3: Receive the response from the target server ---
                # TODO 9: Receive the server's full response.
                # This response could be large, so you might need a loop. For this
                # exercise, receiving one large chunk is often sufficient.
                response_data = # ...
                
                print(f"<- Received response from server (size: {len(response_data)} bytes)")

                # --- Step 4: The Filtering Logic ---

                # TODO 10: Check if the forbidden bytestring is in the server's response.
                if # ...:
                    # If it is, send our custom 404 error page to the browser.
                    print("!!! Forbidden string found! Sending 404 to browser.")
                    # TODO 11: Send the HTTP_404_RESPONSE to the browser_sock.
                    # ...
                else:
                    # If not, forward the server's original response to the browser.
                    print("   Forwarding original response to browser.")
                    # TODO 12: Send the original response_data to the browser_sock.
                    # ...

    except KeyboardInterrupt:
        print("\nProxy server shutting down.")
        break
    except Exception as e:
        print(f"An error occurred: {e}")

listen_sock.close()