#################################################################
####  Prueba de Promedios para los números pseudoaleatorios  ####
#################################################################

#Imports
from scipy.stats import norm
import numpy as np
# Leer los números
na_nums = []
with open("numbers.txt", "r") as f:
    for line in f:
        na_nums.append(float(line.strip()))

N = len(na_nums)
x = sum(na_nums)/N
s = np.std(na_nums)
ALPHA = 0.05

Li = 1/2-(norm.ppf((1-ALPHA/2), loc=x, scale=s))
Ls = 1/2+(norm.ppf((1-ALPHA/2), loc=x, scale=s))

print(f"Rango: < {Li} ; {Ls} >")
if 0.5 > Li and 0.5 < Ls:
    print("0.5 se encuentra en el rango\nSe acepta H0")
else:
    print("0.5 no se encuentra en el rango\nSe rechaza H0")

