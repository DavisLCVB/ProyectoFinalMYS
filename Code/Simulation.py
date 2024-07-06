from NAGenerator import NAGenerator, SEED, MULTIPLIER, MODULUS
from BetaGenerator import *
import pandas as pd


# Clase que representa un servidor
class Server:
    def __init__(self, gen: Generator) -> None:
        self.gen = gen
        self.end = 0


# Clase que representa un arreglo de servidores
class ServiceArray:
    def __init__(self, servers: list[Server] = None) -> None:
        self.servers = servers
        self.end = 0

    def min_server(self):
        min = 100000000
        imin = 0
        for i, serv in enumerate(self.servers):
            if min > serv.end:
                min = serv.end
                imin = i
        return imin, min


# Variable que representa los servidores de procesamiento de documentos
servers = ServiceArray(
    [
        Server(BetaGen(0.821, 1.47)),
        Server(BetaGen(0.774, 1.6)),
        Server(BetaGen(0.925, 1.98)),
        Server(BetaGen(1.65, 0.408)),
        Server(BetaGen(0.713, 1.13)),
    ]
)
# Variable que representa el generador de números aleatorios
rand = NAGenerator(SEED, MULTIPLIER, MODULUS)
# Variable que representa el generador de arribos
arrival = BetaGen(0.76, 3.53)
# Variable que representa el servidor de distribución
distribution = Server(BetaGen(2.5, 7.65))
# Variable que representa el servidor de Derivación
derivation = Server(ExponentialGen(0.173))


# Número de ejecuciones
runs = 30
# Tiempo de simulación
time = 0
# Datos de la simulación
data = {
    "Iteración": [],
    "NA's Arribo": [],
    "Arribo": [],
    "T. de Llegada": [],
    "NA's Distribución": [],
    "T. Distribución": [],
    "Inicio Distribución": [],
    "Fin Distribución": [],
    "NA's Servidor 1": [],
    "Inicio Servidor 1": [],
    "Fin Servidor 1": [],
    "NA's Servidor 2": [],
    "Inicio Servidor 2": [],
    "Fin Servidor 2": [],
    "NA's Servidor 3": [],
    "Inicio Servidor 3": [],
    "Fin Servidor 3": [],
    "NA's Servidor 4": [],
    "Inicio Servidor 4": [],
    "Fin Servidor 4": [],
    "NA's Servidor 5": [],
    "Inicio Servidor 5": [],
    "Fin Servidor 5": [],
    "NA's Derivación": [],
    "T. de Derivación": [],
    "Inicio Derivación": [],
    "Fin Derivación": [],
    "Cola Distribución": [],
    "Cola Servidor": [],
    "Cola Derivación": [],
}


def get_time_serv(init_t, index):
    serv: Server = servers.servers[index]
    t_serv, nas = serv.gen.get_rand(rand)
    servers.servers[index].end = init_t + t_serv
    return servers.servers[index].end, nas

def update_serv_arr(index, init, end, nas):
    for i, _ in enumerate(servers.servers):
        if i != index:
            data[f"NA's Servidor {i+1}"].append("")
            data[f"Inicio Servidor {i+1}"].append(0)
            data[f"Fin Servidor {i+1}"].append(0)
        else:
            data[f"NA's Servidor {i+1}"].append(str(nas))
            data[f"Inicio Servidor {i+1}"].append(init)
            data[f"Fin Servidor {i+1}"].append(end)

# Simulación
for run in range(runs):
    # Arribo
    inter_arr_t, arr_nas = arrival.get_rand(rand)  # T. de inter Arribo y NA's
    time += inter_arr_t
    # Tiempo de llegada
    arr_t = time
    # Distribución
    dis_t, dis_nas = distribution.gen.get_rand(rand)  # T. Distribución y NA's
    i_dis_t = max(arr_t, distribution.end)  # T. de inicio de distribución
    e_dist_t = i_dis_t + dis_t  # T. de fin de distribución
    distribution.end = e_dist_t # Actualizar el fin del servidor de distribución
    q_dis = i_dis_t - arr_t  # T. de cola de Distribución
    # Servidor
    in_serv, e_min = servers.min_server()  # Indice de servidor y fin mínimo
    i_serv_t = max(e_min, e_dist_t)  #  Inicio de servicio
    e_serv_t, ser_nas = get_time_serv(i_serv_t, in_serv)  # Fin del servidor y NA's
    q_serv = i_serv_t - e_dist_t  # Cola del servidor
    # Derivación
    der_t, der_nas = derivation.gen.get_rand(rand) # T. de derivación y NA's
    i_der_t = max(e_serv_t, derivation.end) # T. de inicio de derivación
    e_der_t = i_der_t + der_t # T. de fin de distribución
    derivation.end = e_der_t # Actualiza el fin del servidor de derivación
    q_der = i_der_t - e_serv_t # Cola de derivación
    # Guardado de datos
    data["Iteración"].append(run)
    data["NA's Arribo"].append(str(arr_nas))
    data["Arribo"].append(inter_arr_t)
    data["T. de Llegada"].append(arr_t)
    data["NA's Distribución"].append(str(dis_nas))
    data["T. Distribución"].append(dis_t)
    data["Inicio Distribución"].append(i_dis_t)
    data["Fin Distribución"].append(e_dist_t)
    data["NA's Derivación"].append(str(der_nas))
    data["T. de Derivación"].append(der_t)
    data["Inicio Derivación"].append(i_der_t)
    data["Fin Derivación"].append(e_der_t)
    data["Cola Distribución"].append(q_dis)
    data["Cola Servidor"].append(q_serv)
    data["Cola Derivación"].append(q_der)
    update_serv_arr(in_serv, i_serv_t, e_serv_t, ser_nas)



dataframe = pd.DataFrame(data)
print(dataframe)
dataframe.to_excel("output.xlsx", index=False)
