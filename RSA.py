"""
Author: Shikhar Gupta 2018229
"""
import random
import math


def extended_euclidean(num1, num2):
    """
    This is an extension of euclid's algorithm to find gcd of two numbers
    It solves for x, y in the following equation
    num1 * x + num2 * y = gcd(num1, num2)

    @param:
        num1 = Stores variable a from multiplicative_inverse()
        num2 = Stores variable n from multiplicative_inverse()
        
    @variables:
        d, temp_x, tempy = Stores returned value from self call
    """
    if num2 == 0:
        return (num1, 1, 0)

    d, temp_x, temp_y = extended_euclidean(num2, num1 % num2)

    # TODO: see python notebook for explanation
    x, y = temp_y, temp_x - int(num1 / num2) * temp_y

    return (d, x, y)


def multiplicative_inverse(a, b, n):
    """
    Generating multiplicative inverse of given numbers (a,b modulo n).
    Thus providing the corresponding inverse for e
    
    @param:
        a = Stores e from generate function
        b = Stores 1 from generate function
        n = Stores phi from generate function
    """
    d, x, y = extended_euclidean(a, n)
    if b % d == 0:
        temp_x = (x * (b/d)) % n
        result = []
        for i in range(d):
            result.append((temp_x + i*(n/d)) % n)
        return result
    return []


def generate(p, q):
    """
    Generates the private and public key for both server and Client
    for a given set of primary parameters p and q.

    @param:
        p = Stores primary number
        q = Stores primary number

    @variables:
        e, n = public key for user(server and client)
        d, n = private key for user(server and client)
    """
    n = p*q
    phi = (p-1) * (q-1)
    e = random.randint(1, phi)
    e = 2*e + 1
    while not (math.gcd(phi, e) == 1):
        e = random.randint(1, 50000)
        e = 2*e + 1

    # It returns a list with only one item
    d = multiplicative_inverse(e, 1, phi)[0]
    return {
        "public": {
            "key":e,
            "n":n
        },
        "private": {
            "key":int(d),
            "n":n
        }
    }


def encrypt(keys, text):
    """
    encrypts the msg using key and n.
    for hash digests it extracts chars from text 
    and then char to ascii and then encrypts it. 
    
    @param:
        keys = contains key and n values for a particular user
        text = msg from user to be encrypted
    """
    key, n = keys["key"], keys["n"]
    if type(text) == str:
        result = [pow(ord(c), key, n) for c in text]
        return result
    else:
        result = pow(text, key, n)
        return int(result)


def decrypt(keys, text):
    """
    decrypts the msg using key and n.
    for encrypted hash digests it extracts elements from text 
    and then decrypts it and then converts it to char. 
    
    @param:
        keys = contains key and n values for a particular user
        text = msg from user to be encrypted
    """
    key, n = keys["key"], keys["n"]
    if type(text) == list:
        result = [chr(pow(c, key, n)) for c in text]
        return "".join(result)
    else:
        result = pow(text, key, n)
        return int(result)
