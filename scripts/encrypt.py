#!/usr/bin/env python3
"""
Usage: python encrypt.py <input_file> <password>
Produces <input_file>.enc (base64: salt|nonce|tag|ciphertext)

Dependencies: pip install pycryptodome
"""
import sys, base64, hashlib
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

input_path = sys.argv[1]
password   = sys.argv[2]

plaintext = open(input_path, "rb").read()
salt      = get_random_bytes(32)
key       = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 600_000, dklen=32)
cipher    = AES.new(key, AES.MODE_GCM, mac_len=16)
nonce     = get_random_bytes(12)
cipher    = AES.new(key, AES.MODE_GCM, nonce=nonce, mac_len=16)
ciphertext, tag = cipher.encrypt_and_digest(plaintext)

print('salt:  ', salt.hex())
print('nonce: ', cipher.nonce.hex())
print('tag:   ', tag.hex())

payload = base64.b64encode(salt + nonce + tag + ciphertext).decode()
open(input_path + ".enc", "w").write(payload)
print(f"Written: {input_path}.enc")