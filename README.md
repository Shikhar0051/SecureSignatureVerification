# Secure Signature Verification
This project ensures secure encryption and decryption of plaintext to secure cyphertext and vice-versa using AES Encryption. And maintains a secure connection between client and server using the RSA algorithm.
The project also requires Web Socket programming to generate a local server between the server and the client on the local system.

# Assumptions for this project
1) The Plaintext and cipher key should be Integer.<br>
2) The Public and private key parameters (p and q) should be distinct prime numbers for both server and client.<br>
3) For a secure RSA Implementation, p and q should be selected greater than 100.<br>
4) WebSocketServer.py should be run before WebSocketClient.py.<br>

# Theory
#### AES Algorithm
This is a 2 round AES Algorithm that encrypts and decrypts the plaintext (integers only). The key needs to be an integer value. 
AES_Encryption and AES_Decryption are the main classes that take keys when asked for objects to be created. The __init__() for both calls keyExpansion() that expands the key.
The Object then calls the AES_Encrypt function for the client and AES_Decrypt function for the server and then the process carries as it requires to be for encrypting and decrypt function similarly. 
The encryption goes for two rounds and returns ciphertext for Encryption and plaintext for decryption. All the mid functions prints the data as stated in the standard output file provided.

#### RSA ALGORITHM
RSA is a public-key cryptosystem that is widely used for secure data transmission. It is also one of the oldest.
The entered parameters p and q will be used to generate the public key (e, n) and private key (d, n) for the server and client using the generate().
The encrypt and decrypt functions are written in such a way that they could handle the encryption and decryption for both the integer value and digest.

#### Flow of Project
<ul>
  <li>
    Client inputs: Message, Secret Key, Public and Private key parameters for Client
  </li>
  <li>
    Server Inputs: Public and Private key parameters for Server. 
  </li>
Message Flow: <br>
  <li>
    Client requests for public key of server.
  </li>
  <li>
    Server sends the public key.
  </li>
  <li>
    Client sends Ciphertext, Encrypted secret key, Client Signature, Client public key.
  </li>
Client side computation:<br>
  <li>
    Create Client signature through RSA algorithm, taking Digest from Hash algorithm and client private key as input.
  </li>
  <li>
    Create Ciphertext through the AES variant, taking Message and Secret key as input.
  </li>
  <li>
    Encrypt Secret key with RSA algorithm, taking Secret key and Server Public key as input.
  </li>
Server side Computation:<br>
  <li>
    Decrypt Secret key using RSA algorithm 
  </li>
  <li>
    Decrypt ciphertext using AES variant
  </li>
  <li>
    Create message digest
  </li>
  <li>
    Verify Client Signature
  </li>
</ul>
<br>
![flow](https://user-images.githubusercontent.com/48147323/116243064-2d273d00-a784-11eb-9526-dbd5fe5ec3ba.jpg)

# Result
![output](https://user-images.githubusercontent.com/48147323/116242628-bab65d00-a783-11eb-8133-f8bb341ffdc3.png)
