#!/usr/bin/env python3

from context import ecc

class TestBasic:

    """ Create the curve Y^2 = X^3 + X + 3. """
    g = ecc.ECPoint(4, 1) # generator
    ec = ecc.EllipticCurve(7, g, 1, 3)

    def test_generator(self):
        s = set()
        p = self.g
        for i in range(12):
            s.add(p)
            p = self.ec.add(p, self.g)

        assert (len(s) == 6)

    def test_add(self):
        i1 = ecc.ECPoint(0, 0, 1)
        i2 = ecc.ECPoint(1, 2, 1)
        assert (self.ec.add(i1, i2) == i1)
        assert (self.ec.add(i1, i2) == i2)

        p1 = ecc.ECPoint(4, 1)
        p2 = ecc.ECPoint(6, 6)
        p3 = ecc.ECPoint(5, 0)
        assert (self.ec.add(p1, p1) == p2)
        assert (self.ec.add(p1, p2) == p3)
        assert (self.ec.add(p2, p1) == p3)

    def test_mul(self):
        p1 = ecc.ECPoint(4, 1)
        assert (self.ec.mul(p1, 2) == self.ec.add(p1, p1))
        # the order of P1 is 6
        assert (self.ec.mul(p1, 7) == p1)
