#################################################
####  Generador de Números PseudoAleatorios  ####
#################################################

# Clase de generador de números por método multipplicativo congruencial
import math


class NAGenerator:
    def __init__(self, seed, multiplier, modulus):
        self.seed = seed
        self.multiplier = multiplier
        self.modulus = modulus
        self.current = seed

    def next(self):
        self.current = (self.multiplier * self.current) % self.modulus
        return self.current

    def get_sequence(self, n):
        sequence = []
        for _ in range(n):
            sequence.append(self.next())
        return sequence


# Función para convertir los números al rango adecuado
def to_dec(num):
    if num == 0:
        return 0
    dig_num = math.floor(math.log10(abs(num))) + 1
    dec = num / (10**dig_num)
    return dec


# Parámetros elegidos para el generador
SEED = 962274
MULTIPLIER = 916041
MODULUS = 989249


def main():
    # Instanciando generador
    gen = NAGenerator(SEED, MULTIPLIER, MODULUS)

    # Número de na's a generar
    N = 2000000

    # Secuencia de números aleatorios
    na_sec = gen.get_sequence(N)
    print(len(na_sec))

    with open("numbers.txt", "w") as f:
        for i, num in enumerate(na_sec):
            f.write(f"{round(to_dec(num), 4)}\n")

if __name__ == "__main__":
    main()