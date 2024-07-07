from NAGenerator import NAGenerator, SEED, MULTIPLIER, MODULUS
from Generators import *
import pandas as pd
import matplotlib.pyplot as plt


# Clase que representa un servidor
class Server:
    def __init__(self, gen: Generator) -> None:
        self.gen = gen
        self.end = 0

    def reset(self):
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

    def reset(self):
        for serv in self.servers:
            serv.reset()


class Doc:
    def __init__(self):
        self.end = 0


class DocsArray:
    def __init__(self):
        self.count = 0
        self.docs = []

    def update(self, time):
        for doc in self.docs:
            if doc.end <= time:
                self.docs.remove(doc)
                self.count -= 1

    def add(self, end):
        self.docs.append(Doc())
        self.docs[-1].end = end
        self.count += 1

    def reset(self):
        self.count = 0
        self.docs = []


# Variable que representa los servidores de procesamiento de documentos
servers = ServiceArray(
    [
        Server(BetaGen(0.821, 1.47)),
        Server(BetaGen(0.774, 1.6)),
        Server(BetaGen(0.925, 1.98)),
        Server(WeibullGen(1.65, 0.408)),
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

docs = DocsArray()

# Número de ejecuciones
runs = 81815
# Réplicas
rep = 15
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
    # "NA's Derivación": [],
    # "T. de Derivación": [],
    # "Inicio Derivación": [],
    # "Fin Derivación": [],
    "Cola Distribución": [],
    "Cola Servidor": [],
    # "Cola Derivación": [],
    "Cola Total": [],
    "Documentos en Cola": [],
    "Promedio Móvil": [],
    "Promedio Docs en Cola": []
}
# Suma
suma = 0
suma2 = 0


def get_time_serv(init_t, index):
    serv: Server = servers.servers[index]
    t_serv, nas = serv.gen.get_rand(rand)
    if index == 0:
        t_serv = -0.001 + 5.89 * t_serv
    elif index == 1:
        t_serv = -0.001 + 7 * t_serv
    elif index == 2:
        t_serv = -0.001 + 7 * t_serv
    elif index == 3:
        t_serv = -0.001 + t_serv
    elif index == 4:
        t_serv = -0.001 + 6 * t_serv
    servers.servers[index].end = init_t + t_serv
    return servers.servers[index].end, nas


def update_serv_arr(index, init, end, nas):
    for i, _ in enumerate(servers.servers):
        if i != index:
            data[f"NA's Servidor {i + 1}"].append("")
            data[f"Inicio Servidor {i + 1}"].append(0)
            data[f"Fin Servidor {i + 1}"].append(0)
        else:
            data[f"NA's Servidor {i + 1}"].append(str(nas))
            data[f"Inicio Servidor {i + 1}"].append(init)
            data[f"Fin Servidor {i + 1}"].append(end)


for i in range(rep):
    data[f"Replica {i + 1}"] = []

data["Valores medios de replicas"] = []

# Réplicas
for i in range(rep - 1):
    suma = 0
    time = 0
    servers.reset()
    distribution.reset()
    derivation.reset()
    for run in range(runs):
        # Arribo
        inter_arr_t, arr_nas = arrival.get_rand(rand)  # T. de inter Arribo y NA's
        inter_arr_t = -0.001 + 1.961 * inter_arr_t
        time += inter_arr_t
        # Tiempo de llegada
        arr_t = time
        # Distribución
        dis_t, dis_nas = distribution.gen.get_rand(rand)  # T. Distribución y NA's
        dist_t = -0.001 + 0.261 * dis_t
        i_dis_t = max(arr_t, distribution.end)  # T. de inicio de distribución
        e_dist_t = i_dis_t + dis_t  # T. de fin de distribución
        distribution.end = e_dist_t  # Actualizar el fin del servidor de distribución
        q_dis = i_dis_t - arr_t  # T. de cola de Distribución
        # Servidor
        in_serv, e_min = servers.min_server()  # Indice de servidor y fin mínimo
        i_serv_t = max(e_min, e_dist_t)  # Inicio de servicio
        # i_serv_t = max(e_min, arr_t)
        e_serv_t, ser_nas = get_time_serv(i_serv_t, in_serv)  # Fin del servidor y NA's
        q_serv = i_serv_t - e_dist_t  # Cola del servidor
        # q_serv = i_serv_t - arr_t
        # Derivación
        # der_t, der_nas = derivation.gen.get_rand(rand)  # T. de derivación y NA's
        # der_t = -0.001 + der_t
        # i_der_t = max(e_serv_t, derivation.end)  # T. de inicio de derivación
        # e_der_t = i_der_t + der_t  # T. de fin de distribución
        # derivation.end = e_der_t  # Actualiza el fin del servidor de derivación
        # q_der = i_der_t - e_serv_t  # Cola de derivación
        q_der = 0
        suma += q_der + q_dis + q_serv
        data[f"Replica {i + 1}"].append(suma / (run + 1))

suma = 0
suma2 = 0
time = 0
servers.reset()
distribution.reset()
derivation.reset()

# Simulación
for run in range(runs):
    # Arribo
    inter_arr_t, arr_nas = arrival.get_rand(rand)  # T. de inter Arribo y NA's
    inter_arr_t = -0.001 + 1.961 * inter_arr_t
    time += inter_arr_t
    # Tiempo de llegada
    arr_t = time
    # Distribución
    dis_t, dis_nas = distribution.gen.get_rand(rand)  # T. Distribución y NA's
    dist_t = -0.001 + 0.261 * dis_t
    i_dis_t = max(arr_t, distribution.end)  # T. de inicio de distribución
    e_dist_t = i_dis_t + dis_t  # T. de fin de distribución
    distribution.end = e_dist_t  # Actualizar el fin del servidor de distribución
    q_dis = i_dis_t - arr_t  # T. de cola de Distribución
    # Servidor
    in_serv, e_min = servers.min_server()  # Indice de servidor y fin mínimo
    i_serv_t = max(e_min, e_dist_t)  # Inicio de servicio
    # i_serv_t = max(e_min, arr_t)
    e_serv_t, ser_nas = get_time_serv(i_serv_t, in_serv)  # Fin del servidor y NA's
    q_serv = i_serv_t - e_dist_t  # Cola del servidor
    # q_serv = i_serv_t - arr_t
    # Derivación
    # der_t, der_nas = derivation.gen.get_rand(rand)  # T. de derivación y NA's
    # der_t = -0.001 + der_t
    # i_der_t = max(e_serv_t, derivation.end)  # T. de inicio de derivación
    # e_der_t = i_der_t + der_t  # T. de fin de distribución
    # derivation.end = e_der_t  # Actualiza el fin del servidor de derivación
    # q_der = i_der_t - e_serv_t  # Cola de derivación
    q_der = 0
    suma += q_der + q_dis + q_serv
    docs.add(i_dis_t)
    docs.update(time)
    suma2 += docs.count
    # suma += q_serv
    # Guardado de datos
    data["Iteración"].append(run + 1)
    data["NA's Arribo"].append(str(arr_nas))
    data["Arribo"].append(inter_arr_t)
    data["T. de Llegada"].append(arr_t)
    data["NA's Distribución"].append(str(dis_nas))
    data["T. Distribución"].append(dis_t)
    data["Inicio Distribución"].append(i_dis_t)
    data["Fin Distribución"].append(e_dist_t)
    # data["NA's Derivación"].append(str(der_nas))
    # data["T. de Derivación"].append(der_t)
    # data["Inicio Derivación"].append(i_der_t)
    # data["Fin Derivación"].append(e_der_t)
    data["Cola Distribución"].append(q_dis)
    data["Cola Servidor"].append(q_serv)
    # data["Cola Derivación"].append(q_der)
    data["Cola Total"].append(q_der + q_dis + q_serv)
    data["Documentos en Cola"].append(docs.count)
    data["Promedio Móvil"].append(suma / (run + 1))
    data["Promedio Docs en Cola"].append(suma2 / (run + 1))
    update_serv_arr(in_serv, i_serv_t, e_serv_t, ser_nas)

data["Replica 15"] = data["Promedio Móvil"]

x = [i + 1 for i in range(runs)]
for key, value in data.items():
    if key.startswith("Replica"):
        plt.plot(x, value, label=f"{key}")

plt.title("Estabilización de las repeticiones")
plt.xlabel = "Nro Corridas"
plt.ylabel = "Promedio móvil de la cola"
plt.legend()
plt.show()


def welch_method(data, window_size):
    half_window = window_size // 2
    moving_avg = []

    for i in range(len(data)):
        start = max(0, i - half_window)
        end = min(len(data), i + half_window + 1)
        window_data = data[start:end]
        moving_avg.append(np.mean(window_data))

    return np.array(moving_avg)


for i in range(runs):
    sum_ins = 0
    for j in range(rep):
        sum_ins += data[f"Replica {j + 1}"][i]
    data["Valores medios de replicas"].append(sum_ins / rep)

fig, axs = plt.subplots(2, 2, figsize=(12, 10))

for i in [3, 5, 10, 19]:
    data[f"Welch w={i}"] = welch_method(data["Valores medios de replicas"], i)

axs[0, 0].plot(x, data[f"Welch w=3"], label=f"w=3")
axs[0, 0].set_title(f"Welch w=3")
axs[0, 0].legend()

axs[0, 1].plot(x, data[f"Welch w=5"], label=f"w=5")
axs[0, 1].set_title(f"Welch w=5")
axs[0, 1].legend()

axs[1, 0].plot(x, data[f"Welch w=10"], label=f"w=7")
axs[1, 0].set_title(f"Welch w=10")
axs[1, 0].legend()

axs[1, 1].plot(x, data[f"Welch w=19"], label=f"w=9")
axs[1, 1].set_title(f"Welch w=19")
axs[1, 1].legend()

plt.tight_layout()
plt.show()

dataframe = pd.DataFrame(data)
# dataframe.to_csv("output.csv", index=False)
dataframe.to_excel("output.xlsx", index=False)
