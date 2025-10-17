# solution.py
import sys
import socket
import struct

# --- Constants ---
FILE_NAME = "data.bin"
# The format must match the one used to create the file.
RECORD_FORMAT = "20si"
# Calculate the size of a single record to navigate the file.
RECORD_SIZE = struct.calcsize(RECORD_FORMAT)


def get_record(line_num):
    """Reads a specific record from the binary file."""
    try:
        with open(FILE_NAME, "rb") as f:
            # Calculate the position of the desired record
            offset = (line_num - 1) * RECORD_SIZE
            f.seek(offset)
            data = f.read(RECORD_SIZE)

            # Check if the read was successful and returned enough bytes
            if not data or len(data) < RECORD_SIZE:
                print(f"Error: Line {line_num} is out of bounds or file is corrupt.")
                sys.exit(1)

            # Unpack the binary data into Python objects
            unpacked_data = struct.unpack(RECORD_FORMAT, data)

            # Decode the byte string and remove null padding
            domain = unpacked_data[0].decode("utf-8").strip("\x00")
            port = unpacked_data[1]
            return domain, port

    except FileNotFoundError:
        print(f"Error: Data file '{FILE_NAME}' not found. Please create it first.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        sys.exit(1)


def main():
    """Main function to parse arguments and execute commands."""
    # Case: No arguments -> Output hostname
    if len(sys.argv) == 1:
        try:
            print(socket.gethostname())
        except Exception as e:
            print(f"Error: Could not get hostname: {e}")
        return

    # For other cases, exactly two arguments are required
    if len(sys.argv) != 3:
        print("Usage:")
        print(f"  python {sys.argv[0]} port <line>")
        print(f"  python {sys.argv[0]} domain <line>")
        print(f"  python {sys.argv[0]} (for local hostname)")
        sys.exit(1)

    command = sys.argv[1]
    try:
        line = int(sys.argv[2])
        if line <= 0:
            raise ValueError("Line number must be positive")
    except ValueError:
        print("Error: <line> must be a positive integer.")
        sys.exit(1)

    # Fetch the data for the specified line
    domain, port = get_record(line)

    if command == "domain":
        # Resolve the domain to an IP address
        try:
            ip_address = socket.gethostbyname(domain)
            print(ip_address)
        except socket.gaierror:
            print(f"Error: Domain '{domain}' could not be resolved.")

    elif command == "port":
        # Find the well-known service for a given port
        try:
            service_name = socket.getservbyport(port)
            print(service_name)
        except OSError:
            print(f"Error: Port {port} does not correspond to a known service.")

    else:
        print(f"Error: Unknown command '{command}'. Use 'port' or 'domain'.")


if __name__ == "__main__":
    main()
