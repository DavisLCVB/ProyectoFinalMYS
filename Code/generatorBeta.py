import random as rd
import math as ma
from NAGenerator import NAGenerator, to_dec

class BetaGen:
    def __init__(self, alpha, beta) -> None:
        self.alpha = alpha
        self.beta = beta

    def get_rand(self, na : NAGenerator):
        nas = []
        x = 0
        y = 0
        while x + y <= 1:
            a = to_dec(na.next())
            b = to_dec(na.next())
            x = ma.pow(a, 1/self.alpha)
            y = ma.pow(b, 1/self.beta)
            nas.extend([a, b])
        return x / (x + y), nas

