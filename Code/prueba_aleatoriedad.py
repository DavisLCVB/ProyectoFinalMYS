class MultiplicativeCongruentialGenerator:
    def __init__(self, seed, multiplier, modulus):
        self.seed = seed
        self.multiplier = multiplier
        self.modulus = modulus
        self.current = seed

    def next(self):
        self.current = (self.multiplier * self.current) % self.modulus
        return self.current

    def get_random_sequence(self, n):
        sequence = []
        for _ in range(n):
            sequence.append(self.next())
        return sequence


a=916041
m=989249
X0=962274

gen = MultiplicativeCongruentialGenerator(a, m, X0)

ransec = gen.get_random_sequence(10000)

k = 100

split = 10000/k

frecO = [0 for _ in range(k)]

for num in ransec:
    for i in range(k):
        if num <= (i*split):
            frecO[i] += 1

frecE = [split for _ in range(k)]

Xo = 0
for i in range(k):
    Xo += ((frecO[i]-frecE[i])**2)/frecE[i]

XoC = 9767.536767

if(Xo < XoC):
    print("No hay diferencias significativas")
    with open("numeros_aleatorios.txt", 'w') as f:
        for num in ransec:
            f.write(f"{num}\n")
else:
    print("Hay diferencias significativas")

