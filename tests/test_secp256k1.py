#!/usr/bin/env python3

from context import ecc

class TestSecp256k1:

    """ Create the secp256k1 curve Y^2 = X^3 + 7. """
    p = int('FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F', 16)
    a = 0
    b = 7
    g = ecc.ECPoint(int('79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798', 16), 
        int('483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8', 16))
    ec = ecc.EllipticCurve(p, g, a, b)
    # order of group
    n = int('FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141', 16)

    def test_generator(self):
        # the order is such that nP = 0
        assert self.ec.mul(self.g, self.n) == ecc.ECPoint(0, 0, 1)

    def test_arithmetic(self):
        p1 = self.ec.random_point()
        assert self.ec.add(p1, self.ec.neg(p1)) == self.ec.identity()
        
        p2 = self.ec.random_point()
        p3 = self.ec.add(p1, p2)
        assert self.ec.is_valid(p3) == True

