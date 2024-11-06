import rsa
import socket
import hashlib
from Crypto.PublicKey import DSA
from Crypto.Signature import DSS
from Crypto.Hash import SHA256

# Generate RSA public and private keys (for encryption/decryption)
public_key_rsa, private_key_rsa = rsa.newkeys(2048)

# Generate DSA keys (for signing/verifying)
private_key_dsa = DSA.generate(2048)
public_key_dsa = private_key_dsa.publickey()

def verify_signature(public_key, message_hash, signature):
    # Verifies the message hash against the received signature using DSA public key
    verifier = DSS.new(public_key, 'fips-186-3')
    try:
        verifier.verify(message_hash, signature)
        return True
    except ValueError:
        return False

def start_server():
    # Create a TCP/IP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the address and port
    server_address = ('localhost', 12345)
    server_socket.bind(server_address)

    # Listen for incoming connections
    server_socket.listen(1)
    print("Server is listening on port 12345...")

    while True:
        # Wait for a connection
        connection, client_address = server_socket.accept()
        try:
            print(f"Connection from {client_address} established.")

            # Send the RSA public key to the client for encryption
            public_key_data = public_key_rsa.save_pkcs1()  # Export the RSA public key as bytes
            connection.sendall(public_key_data)
            print("RSA public key sent to client.")

            # Receive the hashed message from the client
            received_hash = connection.recv(1024)
            print(f"Received hash: {received_hash.hex()}")

            # Receive the signature from the client
            received_signature = connection.recv(2048)
            print(f"Received signature: {received_signature.hex()}")

            # Receive the encrypted data from the client
            data = b""
            while True:
                chunk = connection.recv(2048)
                if not chunk:
                    break
                data += chunk

            # Decrypt the received message
            decrypted_message = rsa.decrypt(data, private_key_rsa)
            decrypted_message_str = decrypted_message.decode('utf-8')  # Decode the message to string
            print(f"Decrypted message: {decrypted_message_str}")

            # Verify the received hash matches the decrypted message
            computed_hash = hashlib.md5(decrypted_message).hexdigest().encode()  # MD5 hash encoded to bytes
            if received_hash == computed_hash:
                print("Hashes match. Message integrity verified.")
            else:
                print("Hashes do not match. Message may be tampered.")

            # Verify the digital signature with the DSA public key
            message_hash_obj = SHA256.new(decrypted_message)
            is_verified = verify_signature(public_key_dsa, message_hash_obj, received_signature)
            if is_verified:
                print("Signature is valid.")
            else:
                print("Signature is invalid.")

        except Exception as e:
            print(f"An error occurred: {e}")

        finally:
            connection.close()
            print("Connection closed.")

if __name__ == "__main__":
    start_server()
