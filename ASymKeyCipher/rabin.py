import random
from sympy import mod_inverse

# 1. Generate public and private keys
def generate_keys(bits=512):
    # Choose two large distinct primes p and q
    p = random_prime(bits)
    q = random_prime(bits)
    
    # Public key (n)
    n = p * q
    
    # Private key (p, q)
    return (n, p, q)

# 2. Function to generate large random primes
def random_prime(bits):
    while True:
        prime = random.getrandbits(bits)
        if prime % 4 == 3 and is_prime(prime):
            return prime

# 3. Primality check (basic)
def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

# 4. Rabin encryption: ciphertext = plaintext^2 mod n
def encrypt(plaintext, n):
    return (plaintext**2) % n

# 5. Rabin decryption (yields 4 possible results)
def decrypt(ciphertext, p, q, n):
    # Compute the modular square roots using p and q
    r_p = mod_sqrt(ciphertext, p)
    r_q = mod_sqrt(ciphertext, q)

    # Use the Chinese Remainder Theorem (CRT) to combine results
    x_p = mod_inverse(q, p) * q * r_p
    x_q = mod_inverse(p, q) * p * r_q
    r1 = (x_p + x_q) % n
    r2 = (x_p - x_q) % n
    r3 = n - r1
    r4 = n - r2

    return (r1, r2, r3, r4)

# 6. Modular square root using the Tonelli-Shanks algorithm
def mod_sqrt(a, p):
    return pow(a, (p + 1) // 4, p)

# Example Usage
if __name__ == '__main__':
    # Generate keys (using 512-bit primes for security)
    n, p, q = generate_keys(bits=512)
    
    # Message to be encrypted (must be an integer smaller than n)
    message = 42

    # Encryption
    ciphertext = encrypt(message, n)
    print(f"Ciphertext: {ciphertext}")
    
    # Decryption (gives 4 possible results)
    possible_plaintexts = decrypt(ciphertext, p, q, n)
    print(f"Possible plaintexts: {possible_plaintexts}")

    # You must know additional information to determine the correct plaintext
