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

    def test_relations(self):
        i1 = ecc.ECPoint(0, 0, 1)
        i2 = ecc.ECPoint(1, 2, 1)
        assert (self.ec.add(i1, i2) == i1)
        assert (self.ec.add(i1, i2) == i2)
