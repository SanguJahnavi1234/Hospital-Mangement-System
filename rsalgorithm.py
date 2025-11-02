from sympy import randprime
import math

# --- Helper Functions ---
def find_coprime(n):
    for i in range(2, n):
        if math.gcd(n, i) == 1:
            return i

def modinv_extended_euclidean(x, y, z):
    q = x[2] // y[2]
    if y[2] == 1:
        return y[1] + z if y[1] < 0 else y[1]
    t = [x[i] - y[i] * q for i in range(len(x))]
    return modinv_extended_euclidean(y, t, z)

def ascii_encode(text):
    return [ord(c) for c in text]

def ascii_decode(codes):
    return "".join(chr(i) for i in codes)

# --- RSA Key Generation ---
def generate_keys():
    p = randprime(1000, 3000)
    q = randprime(1000, 3000)
    n = p * q
    phi = (p - 1) * (q - 1)
    d = find_coprime(phi)
    x = [1, 0, phi]
    y = [0, 1, d]
    e = modinv_extended_euclidean(x, y, phi)
    return (e, n), (d, n)

# --- Encryption ---
def encrypt(text, public_key):
    e, n = public_key
    ascii_vals = ascii_encode(text)
    cipher = [pow(char, e, n) for char in ascii_vals]
    return cipher

# --- Decryption ---
def decrypt(cipher, private_key):
    d, n = private_key
    ascii_vals = [pow(c, d, n) for c in cipher]
    return ascii_decode(ascii_vals)

# --- Sample Run ---
if __name__ == "__main__":
    public_key, private_key = generate_keys()
    print("Public Key:", public_key)
    print("Private Key:", private_key)

    message = input("Enter message to encrypt: ")