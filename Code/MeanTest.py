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

Li = 1/2-(norm.ppf((1-ALPHA/2), loc=0, scale=1))
Ls = 1/2+(norm.ppf((1-ALPHA/2), loc=0, scale=1))

print(f"La media es {x}")
print(f"Rango: < {Li} ; {Ls} >")
if x > Li and x < Ls:
    print("La media es equivalente a 0.5\nSe acepta H0")
else:
    print("La media no es equivalente a 0.5\nSe rechaza H0")

