import math as ma
from NAGenerator import NAGenerator, to_dec
import numpy as np


class Generator:
    def __init__(self) -> None:
        pass

    def get_rand(self, na: NAGenerator):
        pass


class BetaGen(Generator):
    def __init__(self, alpha, beta) -> None:
        super().__init__()
        self.alpha = alpha
        self.beta = beta

    def get_rand(self, na: NAGenerator):
        nas = []
        a = self.beta + self.alpha
        b = 0
        if min(self.alpha, self.beta) <= 1:
            b = 1 / min(self.alpha, self.beta)
        else:
            b = ma.sqrt((a - 2) / (2 * self.alpha * self.beta - a))
        c = self.alpha + (1 / b)
        while True:
            u1 = to_dec(na.next())
            u2 = to_dec(na.next())
            v = b * ma.log(u1 / (1 - u1))
            w = self.alpha * ma.exp(v)
            nas.extend([u1, u2])
            if a * ma.log(a / (self.beta + w)) + c * v - ma.log(4) < ma.log(
                    ma.pow(u1, 2) * u2
            ):
                break
        return w / (self.beta + w), nas


class ExponentialGen(Generator):
    def __init__(self, lambd) -> None:
        super().__init__()
        self.lambd = lambd

    def get_rand(self, na: NAGenerator):
        nas = []
        x = 0
        while x == 0:
            _na = to_dec(na.next())
            x = -1 / self.lambd * ma.log(_na)
            nas.append(_na)
        return x, nas


class WeibullGen(Generator):
    def __init__(self, scale, shape):
        super().__init__()
        self.scale = scale
        self.shape = shape

    def get_rand(self, na: NAGenerator):
        u1 = to_dec(na.next())
        nas = [u1]
        return self.scale * (-np.log(1 - u1)) ** (1 / self.shape), nas
