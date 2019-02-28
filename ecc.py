#!/usr/bin/env python3

class EllipticCurve():

    def __init__(self, p, a, b):
        self.p = p
        self.a = a
        self.b = b

    def egcd(self, a, b):
        if a == 0:
            return (b, 0, 1)
        else:
            g, y, x = self.egcd(b % a, a)
            return (g, x - (b // a) * y, y)

    def modinv(self, a, m):
        g, x, y = self.egcd(a, m)
        if g != 1:
            raise Exception('modular inverse does not exist')
        else:
            return x % m

    def add(self, p1, p2):
        """ Adds two points P1 = (x1, y1) and P2 = (x2, y2) on the given curve. """
        if p1[0] != p2[0]:
            lam = ((p2[1] - p1[1]) * self.modinv((p2[0] - p1[0]) % self.p, self.p)) % self.p
        else:
            lam = (3*p1[0]**2 + self.a) * self.modinv(2 * p1[1], self.p)


        x3 = (lam**2 - p1[0] - p2[0]) % self.p
        y3 = ((p1[0] - x3) * lam - p1[1]) % self.p
        return (x3, y3)

    def neg(self, p):
        return (p[0], self.p - p[1])

    def sub(self, p1, p2):
        """ Subtract P2 from P1, i.e., P1 - P2 = P1 + (-P2). """
        return self.add(p1, self.neg(p2))
