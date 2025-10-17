"""
Binary File Reader - Student Assignment

Task Description:
Given a binary file with the following structure: Domain (20s), port (i)
Write a python script supporting the following command line arguments:
- port <line>: outputs what service belongs to the port of the line given as parameter
- domain <line>: outputs the resolved IP address of the domain of the line given as parameter
- If there is no parameter, outputs the host's name
"""

# solution.py
import sys
import socket
import struct

# --- Constants ---
FILE_NAME = "data.bin"
# The format must match the one used to create the file.
# Format: 20-character string + signed integer
RECORD_FORMAT = "20si"
# Calculate the size of a single record to navigate the file.
# This helps us jump directly to any record position
RECORD_SIZE = struct.calcsize(RECORD_FORMAT)

def get_record(line_num):
    """Reads a specific record from the binary file."""
    try:
        with open(FILE_NAME, "rb") as f:
            # TODO: Calculate the position of the desired record
            # Hint: multiply (line_num - 1) by the record size to get byte offset
            
            # TODO: Move the file pointer to the calculated position
            
            # TODO: Read exactly one record worth of bytes from current position
            
            # TODO: Check if the read was successful and returned enough bytes
            # If not enough data was read, the line number is out of bounds
            
            # TODO: Unpack the binary data into Python objects
            # Use struct.unpack() with the RECORD_FORMAT
            
            # TODO: Decode the byte string and remove null padding
            # The first element is bytes that need to be decoded to UTF-8
            # Remove any null characters (\x00) used for padding
            
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
            # TODO: Get and print the local machine's hostname
            # Use socket module function to retrieve hostname
            
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
            # TODO: Use socket module to convert domain name to IP address
            # Store result in ip_address variable
            
            print(ip_address)
        except socket.gaierror:
            print(f"Error: Domain '{domain}' could not be resolved.")

    elif command == "port":
        # Find the well-known service for a given port
        try:
            # TODO: Use socket module to find service name for the given port number
            # Store result in service_name variable
            
            print(service_name)
        except OSError:
            print(f"Error: Port {port} does not correspond to a known service.")

    else:
        print(f"Error: Unknown command '{command}'. Use 'port' or 'domain'.")

if __name__ == "__main__":
    main()