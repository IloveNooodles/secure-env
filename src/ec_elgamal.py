from Crypto.Util.number import bytes_to_long, long_to_bytes, getRandomInteger
from ecdsa import ellipticcurve
from typing import Tuple

class ECElgamal:
    def __init__(self) -> None:
        """ 
        ECC p521 based on https://neuromancer.sk/std/nist/P-521
        """
        self.p = 0x01ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        self.a = 0x01fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffc
        self.b = 0x0051953eb9618e1c9a1f929a21a0b68540eea2da725b99b315f3b8b489918ef109e156193951ec7e937b1652c0bd3bb1bf073573df883d2c34f1ef451fd46b503f00
        # Cofactor
        self.h = 0x1

        self.EC = ellipticcurve.CurveFp(self.p, self.a, self.b, self.h)

        # order
        self.n = 0x01fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffa51868783bf2f966b7fcc0148f709a5d03bb5c9b8899c47aebb6fb71e91386409

        # Generator x, y
        self.generator_point = (0x00c6858e06b70404e9cd9e3ecb662395b4429c648139053fb521f828af606b4d3dbaa14b5e77efe75928fe1dc127a2ffa8de3348b3c1856a429bf97e7e31c2e5bd66, 0x011839296a789a3bc0045c8a5fb42c7d1bd998f54449579b446817afbd17273e662c97ee72995ef42640c550b9013fad0761353c7086a272c24088be94769fd16650)
        self.G = ellipticcurve.PointJacobi(self.EC, self.generator_point[0], self.generator_point[1], 1, self.n)

        # Private
        self.x = None
        
        # Public 
        self.Q = None
    
    def generate_key_from_input(self) -> None:
        """ 
        User input the password 

        Generate private and public key
        """
        # Get Input (secret key)
        text = input("Insert your password: ")
        text = text.encode("utf-8")
        text_as_long = bytes_to_long(text) % self.n
        
        # Get secret key
        self.x = text_as_long 

        # public
        self.Q = self.x * self.G

    def get_public_key(self) -> Tuple[bytes, bytes]:
        """ 
        Return the public key of the ec elgamal 
        """
        assert(self.Q != None)

        x, y = self.Q.x(), self.Q.y()
        return (x, y)

    def is_point_on_curve(self, x, y):
        """ 
        Check if x y in the curve
        """
        return self.EC.contains_point(x, y)

    def get_eliptic_curve(self):
        return self.EC

    def encrypt(self, message: bytes):
        """  
        Encrypt message

        Returns tuple of poin
        """
        # Generate random integer
        k = getRandomInteger(self.n.bit_length())
        C1 = self.G * k

        # Only interested in X part
        C2 = ((self.Q * k).x() + bytes_to_long(message)) % self.p

        return (C1, C2)

    def decrypt(self, C1, C2) -> bytes:
        message = C2 - (C1 * self.x).x()
        message = message % self.p
        return long_to_bytes(message)

def main():
  a = ECElgamal()
  a.generate_key_from_input()
  c1, c2 = a.encrypt(b"awfawefawfwa")

if __name__ == "__main__":
    main()