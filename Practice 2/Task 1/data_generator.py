# create_test_file.py
import struct

# Data to be written: (domain, port)
# The domain string must be converted to bytes.
records = [
    (b"google.com", 80),
    (b"elte.hu", 443),
    (b"example.com", 22),
    (b"nonexistent12345.xyz", 9999),  # For testing errors
]

# Format string: 20s for a 20-byte string, 'i' for a standard integer.
record_format = "20si"

try:
    with open("data.bin", "wb") as f:
        for domain, port in records:
            # Pad the domain with null bytes to ensure it's 20 bytes long
            padded_domain = domain.ljust(20, b"\0")
            packed_data = struct.pack(record_format, padded_domain, port)
            f.write(packed_data)
    print("✅ data.bin created successfully.")
except IOError as e:
    print(f"❌ Error creating file: {e}")
