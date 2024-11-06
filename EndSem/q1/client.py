import socket

def start_client(file_data):
    # Create a TCP/IP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the server's address and port
    server_address = ('localhost', 65432)
    client_socket.connect(server_address)

    try:
        # Send data to the server
        client_socket.sendall(file_data)
        print("Sent data")

        # Receive the encrypted message from the server
        received_message = client_socket.recv(4096)  # Increased buffer size
        print(f"Received Encrypted Message: {received_message}")  # Display as bytes
    finally:
        client_socket.close()

if __name__ == "__main__":
    # Open the file in binary mode
    with open("file.txt", 'rb') as f:
        file_data = f.read()
    
    # Start the client with the binary file data
    start_client(file_data)
