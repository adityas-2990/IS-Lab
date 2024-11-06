import socket

def start_server(host='localhost', port=12345):
    # Create a TCP/IP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the address and port
    server_socket.bind((host, port))

    # Listen for incoming connections
    server_socket.listen(1)
    print(f"Server listening on {host}:{port}...")

    while True:
        # Wait for a connection
        connection, client_address = server_socket.accept()
        try:
            print(f"Connection from {client_address} established.")
            while True:
                # Receive data from the client
                data = connection.recv(1024)
                if not data:
                    break
                print(f"Received: {data.decode()}")
                # Send a response back to the client
                response = "Message received"
                connection.sendall(response.encode())
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            connection.close()
            print("Connection closed.")

if __name__ == "__main__":
    start_server()
