import socket
import hashlib

import rsa


def start_server():
    # Create a TCP/IP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the address and port
    server_address = ('localhost', 65432)
    server_socket.bind(server_address)

    # Listen for incoming connections
    server_socket.listen(1)
    print("Server is listening on port 65432...")

    while True:
        # Wait for a connection
        connection, client_address = server_socket.accept()
        try:
            print(f"Connection from {client_address} established.")
            # Receive the data from the client
            data = connection.recv(1024)
            public_key, private_key = rsa.newkeys(2048)
            ciphertext = rsa.encrypt(data, public_key)
            connection.sendall(ciphertext.encode())
        finally:
            connection.close()

if __name__ == "__main__":
    start_server()
