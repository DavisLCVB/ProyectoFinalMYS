import pandas as pd

#Previamente, realizar la simulacion con numero de corridas optimas = 112001 y replicas = 15
#Se debe exportar el dataframe resultante como csv
df = pd.read_csv('output.csv')

data = {
    "TC_Inicio de lote": [],
    "TC_Fin de lote": [],
    "DC_Inicio de lote": [],
    "DC_Fin de lote": []
}

band = False

var_params = {"TC": {"name": "TC", "variable": "Cola Total", "min": 22000},
              "DC": {"name": "DC", "variable": "Documentos en Cola", "min": 1947}}

for var in var_params.keys():
    for i in range(var_params[var]["min"], len(df.index)-1):
        if not band:
            data[f"{var_params[var]["name"]}_Inicio de lote"].append(df["T. de Llegada"][i-1])
            band = True
        else:
            if df[var_params[var]["variable"]][i] == 0 and df[var_params[var]["variable"]][i+1] != 0:
                data[f"{var_params[var]["name"]}_Fin de lote"].append(df["T. de Llegada"][i])
                band = False

    band = False
    data[f"{var_params[var]["name"]}_Fin de lote"].append(df["T. de Llegada"][len(df.index)-1])

df_tc = pd.DataFrame(data, columns=["TC_Inicio de lote", "TC_Fin de lote"])
df_tc.to_excel('regenerativo_tc.xlsx', index=False)
df_dc = pd.DataFrame(data, columns=["DC_Inicio de lote", "DC_Fin de lote"])
df_dc.to_excel('regenerativo_dc.xlsx', index=False)