"""
Author: Shikhar Gupta 2018229
"""
import asyncio
import websockets
from aesDecryption import AES_Decryption
from RSA import generate, encrypt, decrypt
import json
import hashlib

#crearing the method to receive the message and returns the reverse of the message
async def response(websocket, path):
        p = int(input("Enter public key parameter (prime number p): "))
        q = int(input("Enter private key parameter (prime number q): "))

        ### public and private key generation 
        key_pair = generate(p, q)
        public_key = key_pair["public"]
        private_key_server = key_pair["private"]
        public_key_server = json.dumps(public_key)

        ##### Sending public key to client
        message = await websocket.recv()
        if message == "Requesting Secret Key":
                await websocket.send(public_key_server)
        
        ##### Receiving All parameters from client
        message = await websocket.recv()
        message = json.loads(message)
        digital_signature_client = message["client_sign"]
        secret_key = message["encrypted_secret_key"]
        client_public_key = message["client_public_key"]
        ciphertext = message["ciphertext"]

        ##### decrypting secret key using server public key
        key = decrypt(private_key_server, secret_key)

        ##### drcrypting ciphertext
        dec = AES_Decryption(key)
        plaintext = dec.AES_Decrypt(ciphertext)

        # ##### drcrypting msg digest from digital signature.
        client_digest = decrypt(client_public_key, digital_signature_client)

        ##### creating digest and digital signature for verification
        digest = hashlib.sha256(plaintext.to_bytes(2, "big")).hexdigest()

        print("Decrypted Secret Key ", key)
        print("Decrypted Message ", plaintext)
        print("Message Digest ", digest)
        print("Intermediate Verification Code ", digital_signature_client)
        if client_digest == digest:
                print("Signature Verified")
        else:
                print("Signature not Verified")
        print()
        print("Submitted by -- Shikhar Gupta 2018229")
        exit()

                
# server starts in localhost at port 1234
start_server = websockets.serve(response, 'localhost', 1234)

#asyncio methods to start server and run forever
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
