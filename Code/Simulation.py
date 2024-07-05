from NAGenerator import NAGenerator, SEED, MULTIPLIER, MODULUS
from generatorBeta import BetaGen
import pandas as pd

class Servidor:
    def __init__(self, alpha, beta) -> None:
        self.dist = BetaGen(alpha, beta)
        self.enable = False
        self.fin = 0

na = NAGenerator(SEED, MULTIPLIER, MODULUS)

servs = []
servs.append(Servidor(0.821, 1.47))
servs.append(Servidor(0.774, 1.6))
servs.append(Servidor(0.925, 1.98))
servs.append(Servidor(1.65, 0.408))
servs.append(Servidor(0.713, 1.13))

docs = BetaGen(0.76, 3.53)

dist = BetaGen(2.5, 7.65)


nCorr = 30


def sel_serv(na, ld, d):
    min = 100000000
    imin = 0
    cola = 0
    nasstr : str
    for i, serv in enumerate(servs):
        if min > serv.fin:
            min = serv.fin
            imin = i
    if(min > ld):
        nf, nas1 = servs[imin].dist.get_rand(na) 
        servs[imin].fin += nf
        cola =  min - ld
        nasstr = str(nas1)
    else:
        nf2, nas2 = servs[imin].dist.get_rand(na)
        servs[imin].fin = ld + nf2
        nasstr = str(nas2)
    d.append(nasstr) #7
    for i in range(len(servs)):
        if i != imin:
            d.extend([0,0]) #8, 9, 10, 11
        else:
            init = ld if cola == 0 else min
            d.extend([init, servs[i].fin]) # 12
    return cola

temp = 0
head = ["Nro", "NA1", "Inter-llegada", "T. de LLegada", "NA2", "T. de Dist", "NAS Ser", "S1 I", "S1 F", "S2 I", "S2 F", "S3 I ", "S3 F", "S4 I", "S4 F", "S5 I", "S5 F", "Cola"]
row = []
data = []
for i in range(nCorr):
    row.append(i) #1
    doc, nas = docs.get_rand(na)
    nas = str(nas)
    row.append(nas) #2
    row.append(doc) #2
    temp += doc
    row.append(temp) #4
    dis, nas2 = dist.get_rand(na)
    nas2 = str(nas2)
    row.append(nas2) #5
    row.append(dis) #6
    cola = sel_serv(na, temp + dis, row) + dis
    row.append(cola) #13
    data.append(row)
    row = []

dataframe = pd.DataFrame(data, columns=head)
print(dataframe)
dataframe.to_excel("output.xlsx", index=False)

