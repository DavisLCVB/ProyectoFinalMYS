from NAGenerator import NAGenerator, SEED, MULTIPLIER, MODULUS
from Generators import *
import pandas as pd
import matplotlib.pyplot as plt
from Objects import *


# Variable que representa los servidores de procesamiento de documentos
servers = ServiceArray(
    [
        Server(BetaGen(0.821, 1.47)),
        Server(BetaGen(0.774, 1.6)),
        Server(BetaGen(0.925, 1.98)),
        Server(WeibullGen(1.65, 0.408)),
        Server(BetaGen(0.713, 1.13)),
        Server(WeibullGen(1.65, 0.408)),
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
runs = 70000
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
    "NA's Servidor 6": [],
    "Inicio Servidor 6": [],
    "Fin Servidor 6": [],
    "Cola Distribución": [],
    "Cola Servidor": [],
    "Cola Total": [],
    "Documentos en Cola": [],
    "Promedio Movil de Tiempo en Cola": [],
    "Promedio Movil de Documentos en Cola": []
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
    elif index == 3 or index == 5:
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
    data[f"Replica {i + 1} TCola"] = []
for i in range(rep):
    data[f"Replica {i + 1} DCola"] = []
if rep > 0:
    data["Medias por Corrida en TCola"] = []
    data["Medias por Corrida en DCola"] = []

# Réplicas
for i in range(rep):
    suma = 0
    time = 0
    suma2 = 0
    servers.reset()
    distribution.reset()
    derivation.reset()
    docs.reset()
    for run in range(runs):
        # Arribo
        inter_arr_t, arr_nas = arrival.get_rand(rand)  # T. de inter Arribo y NA's
        inter_arr_t = -0.001 + 1.961 * inter_arr_t
        time += inter_arr_t
        # Tiempo de llegada
        arr_t = time
        # Distribución
        dis_t, dis_nas = distribution.gen.get_rand(rand)  # T. Distribución y NA's
        dis_t = -0.001 + 0.261 * dis_t
        i_dis_t = max(arr_t, distribution.end)  # T. de inicio de distribución
        e_dis_t = i_dis_t + dis_t  # T. de fin de distribución
        distribution.end = e_dis_t  # Actualizar el fin del servidor de distribución
        q_dis = i_dis_t - arr_t  # T. de cola de Distribución
        # Servidor
        in_serv, e_min = servers.min_server()  # Indice de servidor y fin mínimo
        i_serv_t = max(e_min, e_dis_t)  # Inicio de servicio
        e_serv_t, ser_nas = get_time_serv(i_serv_t, in_serv)  # Fin del servidor y NA's
        q_serv = i_serv_t - e_dis_t  # Cola del servidor
        q_der = 0
        suma += q_der + q_dis + q_serv
        docs.add(i_dis_t)
        docs.update(time)
        suma2 += docs.count
        data[f"Replica {i + 1} TCola"].append(suma / (run + 1))
        data[f"Replica {i + 1} DCola"].append(suma2 / (run + 1))
        if i == rep - 1:
            data["Iteración"].append(run + 1)
            data["NA's Arribo"].append(str(arr_nas))
            data["Arribo"].append(inter_arr_t)
            data["T. de Llegada"].append(arr_t)
            data["NA's Distribución"].append(str(dis_nas))
            data["T. Distribución"].append(dis_t)
            data["Inicio Distribución"].append(i_dis_t)
            data["Fin Distribución"].append(e_dis_t)
            data["Cola Distribución"].append(q_dis)
            data["Cola Servidor"].append(q_serv)
            data["Cola Total"].append(q_der + q_dis + q_serv)
            data["Documentos en Cola"].append(docs.count)
            data["Promedio Movil de Tiempo en Cola"].append(suma / (run + 1))
            data["Promedio Movil de Documentos en Cola"].append(suma2 / (run + 1))
            update_serv_arr(in_serv, i_serv_t, e_serv_t, ser_nas)

if rep > 0:
    data["Replica 15 TCola"] = data["Promedio Movil de Tiempo en Cola"]
    data["Replica 15 DCola"] = data["Promedio Movil de Documentos en Cola"]

    x = [i + 1 for i in range(runs)]
    for key, value in data.items():
        if key.startswith("Replica") and key.endswith("TCola"):
            plt.plot(x, value, label=f"{key}")

    plt.title("Estabilización de las repeticiones")
    plt.xlabel = "Nro Corridas"
    plt.ylabel = "Promedio móvil de la cola"
    plt.legend()
    plt.show()

    plt.clf()
    for key, value in data.items():
        if key.startswith("Replica") and key.endswith("DCola"):
            plt.plot(x, value, label=f"{key}")

    plt.title("Estabilización de las repeticiones")
    plt.xlabel = "Nro Corridas"
    plt.ylabel = "Promedio móvil de documentos en cola"
    plt.legend()
    plt.show()


def welch_method(_data, window_size):
    half_window = window_size // 2
    moving_avg = []

    for i in range(len(_data)):
        start = max(0, i - half_window)
        end = min(len(_data), i + half_window + 1)
        window_data = _data[start:end]
        moving_avg.append(np.mean(window_data))

    return np.array(moving_avg)


if rep > 0:
    for i in range(runs):
        sum_ins = 0
        for j in range(rep):
            sum_ins += data[f"Replica {j + 1} TCola"][i]
        data["Medias por Corrida en TCola"].append(sum_ins / rep)

    fig, axs = plt.subplots(2, 2, figsize=(12, 10))

    for i in [3, 5, 10, 19]:
        data[f"Welch w={i} TCola"] = welch_method(data["Medias por Corrida en TCola"], i)

    axs[0, 0].plot(x, data[f"Welch w=3 TCola"], label=f"w=3")
    axs[0, 0].set_title(f"Welch w=3")
    axs[0, 0].legend()

    axs[0, 1].plot(x, data[f"Welch w=5 TCola"], label=f"w=5")
    axs[0, 1].set_title(f"Welch w=5")
    axs[0, 1].legend()

    axs[1, 0].plot(x, data[f"Welch w=10 TCola"], label=f"w=7")
    axs[1, 0].set_title(f"Welch w=10")
    axs[1, 0].legend()

    axs[1, 1].plot(x, data[f"Welch w=19 TCola"], label=f"w=9")
    axs[1, 1].set_title(f"Welch w=19")
    axs[1, 1].legend()

    plt.tight_layout()
    plt.show()

    for i in range(runs):
        sum_ins = 0
        for j in range(rep):
            sum_ins += data[f"Replica {j + 1} DCola"][i]
        data["Medias por Corrida en DCola"].append(sum_ins / rep)

    fig, axs = plt.subplots(2, 2, figsize=(12, 10))

    for i in [3, 5, 10, 19]:
        data[f"Welch w={i} DCola"] = welch_method(data["Medias por Corrida en DCola"], i)

    axs[0, 0].plot(x, data[f"Welch w=3 DCola"], label=f"w=3")
    axs[0, 0].set_title(f"Welch w=3")
    axs[0, 0].legend()

    axs[0, 1].plot(x, data[f"Welch w=5 DCola"], label=f"w=5")
    axs[0, 1].set_title(f"Welch w=5")
    axs[0, 1].legend()

    axs[1, 0].plot(x, data[f"Welch w=10 DCola"], label=f"w=7")
    axs[1, 0].set_title(f"Welch w=10")
    axs[1, 0].legend()

    axs[1, 1].plot(x, data[f"Welch w=19 DCola"], label=f"w=9")
    axs[1, 1].set_title(f"Welch w=19")
    axs[1, 1].legend()

    plt.tight_layout()
    plt.show()

dataframe = pd.DataFrame(data)
dataframe.to_excel("output.xlsx", index=False)
