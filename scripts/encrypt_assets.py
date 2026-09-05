#!/usr/bin/env python3
"""
Usage: python encrypt_assets.py <password>
Encrypts all files in images/ (non-recursive) and audio/
"""
import sys
import os
import base64
import hashlib
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

password = sys.argv[1]

dirs = [
    ('images', False),  # non-recursive
    ('audio',  False),
    ('videos', False),
]

def encrypt_file(input_path, password):
    plaintext = open(input_path, 'rb').read()
    salt      = get_random_bytes(32)
    nonce     = get_random_bytes(12)
    key       = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 600_000, dklen=32)
    cipher    = AES.new(key, AES.MODE_GCM, nonce=nonce, mac_len=16)
    ciphertext, tag = cipher.encrypt_and_digest(plaintext)
    payload   = base64.b64encode(salt + nonce + tag + ciphertext).decode()
    open(input_path + '.enc', 'w').write(payload)
    print(f'  Encrypted: {input_path}')

for directory, recursive in dirs:
    if not os.path.isdir(directory):
        print(f'Skipping {directory}/ (not found)')
        continue
    print(f'\nProcessing {directory}/')
    for entry in os.scandir(directory):
        if not entry.is_file():
            continue
        if entry.name.endswith('.enc'):
            continue  # don't encrypt already-encrypted files
        if os.path.exists(entry.path + '.enc'):
            print(f'  Skipping (already encrypted): {entry.path}')
            continue
        encrypt_file(entry.path, password)
        
print('\nDone.')