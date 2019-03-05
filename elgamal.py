#!/usr/bin/env python3

from random import randint
from ecc import EllipticCurve, ECPoint

def keygen():
    # use the secp256k1 curve
    p = int('FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F', 16)
    a = 0
    b = 7
    g = ECPoint(int('79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798', 16), 
        int('483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8', 16))
    G = EllipticCurve(p, g, a, b)

    # generate private key
    x = randint(1, p)
    h = G.mul(g, x)

    return (x, G, g, p, h)


def encrypt(m, G, g, p, h):
    """
    Encryption of plaintext m.

    Parameters
    ----------
    m: The message, a point on the curve
    G: The curve
    g: The curve base point
    p: The order of the field
    h: Public part of the shared secret
    """

    y = randint(1, p)
    c1 = G.mul(g, y)
    s = G.mul(h, y)         # h*y = g*xy
    c2 = G.add(m, s)
    return (c1, c2)


def decrypt(c, x, G):
    """
    Decryption of ciphertext c.
    
    Parameters
    ----------
    c: The ciphertext tuple, (c1, c2)
    x: The private key
    G: The curve
    """
        
    c1, c2 = c
    s = G.mul(c1, x)
    m = G.sub(c2, s)
    return m


if __name__ == '__main__':
    x, G, g, p, h = keygen()
    m = G.random_point()
    print('Message:\t{}'.format(m))

    c = encrypt(m, G, g, p, h)
    mp = decrypt(c, x, G)
    print('Decrypted:\t{}'.format(mp))
    assert m == mp
