import socket

def start_client(host='localhost', port=12345):
    # Create a TCP/IP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the server's address and port
    client_socket.connect((host, port))

    try:
        message = input("Enter a message to send to the server: ")
        client_socket.sendall(message.encode())
        
        # Wait for a response from the server
        response = client_socket.recv(1024)
        print(f"Server response: {response.decode()}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client_socket.close()
        print("Connection closed.")

if __name__ == "__main__":
    start_client()
