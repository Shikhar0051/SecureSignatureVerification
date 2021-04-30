"""
Author - Shikhar Gupta 2018229
"""
sBox = [0xa, 0x5, 0x9, 0xb, 0x1, 0x7, 0x8, 0xf,
        0x6, 0x0, 0x2, 0x3, 0xc, 0x4, 0xd, 0xe]

s_Box  = [0x9, 0x4, 0xa, 0xb, 0xd, 0x1, 0x8, 0x5,
         0x6, 0x2, 0x0, 0x3, 0xc, 0xe, 0xf, 0x7]

class AES_Decryption:
    def __init__(self, key):
        self.expanded_key = self.keyExpansion(key)
        

    def keyExpansion(self, key):
        w = [None] * 6
        """Generate the three round keys"""
        def sub2Nib(b):
            """Swap each nibble and substitute it using sBox"""
            return s_Box[b >> 4] + (s_Box[b & 0x0f] << 4)
     
        Rcon1, Rcon2 = 0b10000000, 0b00110000
        w[0] = (key & 0xff00) >> 8
        w[1] = key & 0x00ff
        w[2] = w[0] ^ Rcon1 ^ sub2Nib(w[1])
        w[3] = w[2] ^ w[1]
        w[4] = w[2] ^ Rcon2 ^ sub2Nib(w[3])
        w[5] = w[4] ^ w[3]
        return w
    
    def mult(self, p1, p2):
        p = 0
        while p2:
            if p2 & 0b1:
                p ^= p1
            p1 <<= 1
            if p1 & 0b10000:
                p1 ^= 0b11
            p2 >>= 1
        return p & 0b1111

    def shiftRows(self, s):
        return [s[0], s[1], s[3], s[2]]

    def sub4NibList(self, sbox, s):
        """Nibble substitution function"""
        return [sbox[e] for e in s]

    def mixColumns(self, s):
        return [self.mult(9, s[0]) ^ self.mult(2, s[2]), self.mult(9, s[1]) ^ self.mult(2, s[3]),
                self.mult(9, s[2]) ^ self.mult(2, s[0]), self.mult(9, s[3]) ^ self.mult(2, s[1])]  

    def intToVec(self, n):
        """Convert a 2-byte integer into a 4-element vector"""
        return [n >> 12, (n >> 4) & 0xf, (n >> 8) & 0xf,  n & 0xf]
    
    
    def AES_Decrypt(self, ciphertext, sBox = sBox):
        no_of_rounds = 2

        def fun(state):
            state=[format(s,'04b') for s in state]
            state=eval('0b' + state[0]+state[1]+state[2]+state[3])
            return state
        
        genertated_key=self.expanded_key
        #print("Round Key : ", genertated_key)
        temp=eval('0b'+ format(genertated_key[4],'08b')+format(genertated_key[5],'08b'))
        state=ciphertext^temp
        state=self.intToVec(state)
        
        state = self.shiftRows(state)
        #print("After Round 1 InvShift Rows : ", state)
        
        state=self.sub4NibList(sBox, state)
        #print("After Round 1 InvSubstitute Nibbles : ", state)
        
        state=[state[0],state[2],state[1],state[3]]
        
        
        temp=eval('0b'+ format(genertated_key[2],'08b')+format(genertated_key[3],'08b'))
        state=fun(state)^temp
        #print("Round 1 Result: ", state)

        
        state=self.intToVec(state)
        state = self.mixColumns(state)
        #print("After Round 1 InvMix Columns : ", state)
        
        state = self.shiftRows(state)
        #print("After Round 2 InvShift Rows : ", state)
        
        state=self.sub4NibList(sBox, state)
        #print("After Round 2 InvSubstitute Nibbles : ", state)
        
        state=[state[0],state[2],state[1],state[3]]
        temp=eval('0b'+ format(genertated_key[0],'08b')+format(genertated_key[1],'08b'))
        plain_text=fun(state)^temp
        #print("Round 2 Result: ", state)
        
        plaintext = format(plain_text,'08b')
        return int(plaintext, 2)
