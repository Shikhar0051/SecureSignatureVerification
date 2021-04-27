"""
Author: Shikhar Gupta 2018229
"""
import asyncio
import websockets
from aesEncryption import AES_Encryption
from RSA import generate, encrypt, decrypt
import json
import hashlib



# method to send and reveive from the server
async def message():
    async with websockets.connect("ws://localhost:1234") as socket:
        msg = int(input("Input Plaintext : "))
        key = int(input("Input Cipher key : "))
        p = int(input("Enter public key parameter (prime number p): "))
        q = int(input("Enter private key parameter (prime number q): "))
        
        ##### public private key generation
        key_pair = generate(p, q)
        public_key_client = key_pair["public"]
        private_key_client = key_pair["private"]

        ##### receiving server public key
        print("Initializing Secure connection")
        try:
            await socket.send("Requesting Secret Key")
            server_public_key = await socket.recv()
            server_public_key = json.loads(server_public_key)
        except Exception as e:
            print("Connection Failed")

        ###### AES cipher text generation
        cipher = AES_Encryption(key)
        ciphertext = cipher.AES_Encrypt(msg)
        
        ###### secret key encryption using server public key
        encrypted_secret_key = encrypt(server_public_key, key)

        ##### digest and digital signature generation
        digest = hashlib.sha256(msg.to_bytes(2, "big")).hexdigest()
        digital_signature_client = encrypt(private_key_client, digest)
        
        print("Encrypted Secret Key ", encrypted_secret_key)
        print("Cipher Text ", ciphertext)
        print("Digest ", digest)
        print("Digital Signature ", digital_signature_client)

        ##### sending information to server as serialized code
        msg_to_server = {
            "ciphertext" : int(ciphertext),
            "encrypted_secret_key" : encrypted_secret_key,
            "client_sign" : digital_signature_client,
            "client_public_key" : public_key_client
        }
        msg_to_server = json.dumps(msg_to_server)
        
        await socket.send(msg_to_server)
        print()
        print("Submitted by -- Shikhar Gupta 2018229")

asyncio.get_event_loop().run_until_complete(message())



    
