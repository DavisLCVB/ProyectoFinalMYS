##################################################################
####  Test de Chi cuadrado para los números pseudoaleatorios  ####
##################################################################

# Imports
from scipy.stats import chi2
import numpy as np

na_numbs = []
# Lectura de los números pseudoaleatorios
with open("numbers.txt", "r") as f:
    for line in f:
        num = float(line.strip())
        na_numbs.append(num)

# Datos de los números
N = len(na_numbs)
K = 0
ALPHA = 0.05
S = []

with open("linespaces.txt", "r") as f:
    for line in f:
        ls = float(line.strip())
        S.append(ls)

print(S)
K = len(S) - 1

# Preparación de variables
obsF, _ = np.histogram(na_numbs,S)  # Frecuencia observada
expF = np.full(K, N/K) # Frecuencia esperada

print(obsF)

chi2_0 = np.sum((obsF - expF)**2/expF) # Chi cuadrada calculada
chi2_C = chi2.ppf(ALPHA,K-1) # Chi cuadrada de comparacion

#Imprimir resultados
print(f"Chi cuadrada calculada: {chi2_0}")
print(f"Chi cuadrada de comparacion: {chi2_C} con alpha={ALPHA}, grados de libertad={K-1}")

if(chi2_0 < chi2_C):
    print("No hay diferencias significativas\nSe acepta H0")
else:
    print("Se presentan diferencias significativas\nSe rechaza H0")

