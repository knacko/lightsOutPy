import math
from sympy import mod_inverse


def mod(x, modulus):
    numer, denom = x.as_numer_denom()
    return numer * mod_inverse(denom, modulus) % modulus


def polarToCart(dist, angle):
    angle = math.radians(angle)
    x = int(dist * math.cos(angle))
    y = int(dist * math.sin(angle))
    return x, y