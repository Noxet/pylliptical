#!/usr/bin/env python3

class ECPoint():
    
    def __init__(self, x, y, inf=0):
        self.x = x
        self.y = y
        self.inf = inf

    def __eq__(self, other):
        if (self.inf == 1) and (other.inf == 1):
            return True

        return (self.x == other.x) and (self.y == other.y)

    def __repr__(self):
        if self.inf == 1:
            return 'O'
        return '({}, {})'.format(self.x, self.y)

    def __hash__(self):
        return hash(str(self))


class EllipticCurve():

    def __init__(self, p, g, a, b):
        """ A curve is defined by
            p: The finite field Fp
            g: The base point (generator) for the group
            a, b: Curve parameters, Y^2 = X^3 + aX + b
        """
        self.p = p
        self.g = g
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
            raise Exception('Modular inverse does not exist')
        else:
            return x % m

    def add(self, p1, p2):
        """ Adds two points P1 = (x1, y1) and P2 = (x2, y2) on the given curve. """
        # special case if one point is O (identity)
        if p1.inf == 1 and p2.inf == 1:
            return ECPoint(0, 0, 1)
        if p1.inf == 1:
            return p2
        if p2.inf == 1:
            return p1

        if p1.x != p2.x:
            lam = ((p2.y - p1.y) * self.modinv((p2.x - p1.x) % self.p, self.p)) % self.p
        else:
            if (p1 == self.neg(p2)):
                return ECPoint(0, 0, 1)
            if (p1.y == 0):
                return ECPoint(0, 0, 1)
            
            # point doubling
            lam = ((3*p1.x**2 + self.a) * self.modinv(2 * p1.y, self.p)) % self.p


        x3 = (lam**2 - p1.x - p2.x) % self.p
        y3 = ((p1.x - x3) * lam - p1.y) % self.p
        return ECPoint(x3, y3)

    def neg(self, p):
        """ Calculate the additive inverse of a point P1, -P1. """
        return ECPoint(p.x, self.p - p.y)

    def sub(self, p1, p2):
        """ Subtract P2 from P1, i.e., P1 - P2 = P1 + (-P2). """
        return self.add(p1, self.neg(p2))

    def mul(self, p, m):
        """ Multiply a point P with a constant m, using double-and-add. """
        result = ECPoint(0, 0, 1)
        addend = p

        while m:
            if m & 1:
                result = self.add(result, addend)

            # double the point
            addend = self.add(addend, addend)
            m >>= 1

        return result
