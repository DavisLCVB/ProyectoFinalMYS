import random as rd
import math as ma
x = 0
y = 0
alpha = 0.2
beta = 0.3
while x + y <= 1:
    u = rd.uniform(0,1)
    x = ma.pow(u, 1/alpha)
    v = rd.uniform(0,1)
    y = ma.pow(v, 1/beta)

res = x /(x+y)

print(res)