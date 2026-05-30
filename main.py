import os
import sys
import datetime
import urllib.request
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

CONFIG_PIPELINE = {
    "columnas_base": {
        "numericas": [
            'periodo_anio_mes', 'prestador_cargo_fijo', 'localidad_valor_factor_ajuste', 
            'localidad_consumo_promedio', 'eett_categoria_volumen_asignado', 'rango_ini', 
            'rango_fin', 'rango_fin_scf', 'tarifa_agua', 'tarifa_alcanta', 'eett_fec_ini_vig'
        ],
        "categoricas": [
            'periodo_estado', 'prestador_aplica_igv', 'prestador_estado', 'prestador_nombre', 
            'localidad_nombre', 'localidad_tiene_factor_ajuste', 'localidad_estado', 
            'eett_nombre', 'eett_resolucion', 'eett_estado', 'clase_nombre', 
            'categoria_nombre', 'rango_tiene_scf'
        ]
    },
    "anomalias": {
        "columnas_inyectar": [
            'prestador_cargo_fijo', 'localidad_consumo_promedio', 'tarifa_agua', 'tarifa_alcanta'
        ]
    },
    "columnas_a_eliminar": [
        "eett_fec_ini_vig",
        "periodo_anio_mes" 
    ],
    "transformaciones_numericas": {
        "promediar_listas": [
            "eett_categoria_volumen_asignado"
        ],
        "limpiar_texto": [],
        "imputar_mediana": [
            "prestador_cargo_fijo", "tarifa_agua", "tarifa_alcanta",
            "eett_categoria_volumen_asignado", "periodo_anio", "periodo_mes",
            "eett_anio_vig", "eett_mes_vig", "eett_dia_vig"
        ],
        "imputar_promedio": [
            "localidad_valor_factor_ajuste", "localidad_consumo_promedio"
        ],
        "imputar_cero": [
            "rango_ini", "rango_fin_scf"
        ],
        "imputar_extremo_superior": [
            "rango_fin"
        ]
    },
    "transformaciones_categoricas": {
        "binario": [
            "periodo_estado", "prestador_aplica_igv", "prestador_estado", 
            "localidad_tiene_factor_ajuste", "localidad_estado", "eett_estado", 
            "rango_tiene_scf", "clase_nombre", "categoria_nombre"
        ],
        "onehot": [],
        "frecuencia": [
            "prestador_nombre", "localidad_nombre", 
            "eett_nombre", "eett_resolucion"
        ]
    }
}

def obtener_ruta(*partes):
    return os.path.join(BASE_DIR, *partes)

def asegurar_dataset_descargado(ruta_destino):
    if os.path.exists(ruta_destino):
        return
    registrar_progreso(f"Descargando dataset desde {URL_DATASET}...")
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        req = urllib.request.Request(URL_DATASET, headers=headers)
        with urllib.request.urlopen(req) as response, open(ruta_destino, 'wb') as out_file:
            out_file.write(response.read())
    except Exception as error:
        registrar_progreso(f"ERROR: No se pudo descargar el dataset: {error}")
        sys.exit(1)
    registrar_progreso(f"Dataset descargado en {ruta_destino}")

def registrar_progreso(mensaje):
    marca = datetime.datetime.now().strftime('%H:%M:%S')
    linea = f"[{marca}] {mensaje}"
    with open(archivo_progreso, "a", encoding="utf-8") as f:
        f.write(linea + "\n")
    print(linea)

def auditar_datos_invalidos(df, columnas_num, columnas_cat, config):
    total_filas = len(df)
    cols_con_relleno = set()
    for clave in ("imputar_mediana", "imputar_promedio", "imputar_cero", "imputar_extremo_superior"):
        cols_con_relleno.update(config["transformaciones_numericas"].get(clave, []))

    registrar_progreso(f"=== Auditoría de Datos ({total_filas} filas) ===")

    for col in columnas_num + columnas_cat:
        tipo = "Numérica" if col in columnas_num else "Categórica"
        nulos_nativos = df[col].isna().sum()
        detalles = []

        if tipo == "Numérica":
            col_numerica = pd.to_numeric(df[col], errors='coerce')
            no_numericos = col_numerica.isna().sum() - nulos_nativos
            negativos = (col_numerica[col_numerica.notna()] < 0).sum()
            invalidos = nulos_nativos + no_numericos + negativos
            
            if nulos_nativos > 0:
                detalles.append(f"{nulos_nativos} Nulos")
            if no_numericos > 0:
                detalles.append(f"{no_numericos} No Num")
            if negativos > 0:
                detalles.append(f"{negativos} Neg")
        else:
            vacios = (df[col].astype(str).str.strip() == "").sum()
            invalidos = nulos_nativos + vacios
            
            if nulos_nativos > 0:
                detalles.append(f"{nulos_nativos} Nulos")
            if vacios > 0:
                detalles.append(f"{vacios} Vacíos")

        if col in cols_con_relleno:
            marca = "*" if invalidos > 0 else "$"
        else:
            marca = " "

        validos = total_filas - invalidos
        pct_invalidos = (invalidos / total_filas) * 100
        detalle_texto = f" | Detalle: {', '.join(detalles)}" if detalles else ""
        
        mensaje = f" -> {marca}{tipo} {col}: {validos} válidos, {invalidos} inválidos ({pct_invalidos:.2f}%)" + detalle_texto
        registrar_progreso(mensaje)

def dividir_entrenamiento_prueba(df, proporcion_prueba=0.2):
    df_shuffled = df.sample(frac=1, random_state=42).reset_index(drop=True)
    limite = int(len(df_shuffled) * (1 - proporcion_prueba))
    return df_shuffled.iloc[:limite].copy(), df_shuffled.iloc[limite:].copy()

def estandarizar_datos_fit(matriz_X):
    medias = np.mean(matriz_X, axis=0)
    desviaciones = np.std(matriz_X, axis=0)
    desviaciones = np.where(desviaciones == 0, 1e-8, desviaciones)
    return medias, desviaciones

def estandarizar_datos_transform(matriz_X, medias, desviaciones):
    return (matriz_X - medias) / desviaciones

def normalizar_texto(valor):
    if pd.isna(valor): return "desconocido"
    texto = str(valor).strip().lower()
    if texto == "" or texto in {"nan", "none", "null"}: return "desconocido"
    reemplazos = {"á":"a","é":"e","í":"i","ó":"o","ú":"u","ñ":"n"," ":"_","/":"_","-":"_",".":"_",",":"_",":":"_",";":"_","(":"",")":""}
    for original, nuevo in reemplazos.items():
        texto = texto.replace(original, nuevo)
    while "__" in texto: texto = texto.replace("__", "_")
    return texto.strip("_")[:50] or "desconocido"

def nombre_seguro_columna(valor):
    texto = normalizar_texto(valor)
    return texto[:35] if len(texto) > 35 else texto

def extraer_componentes_periodo(serie_periodo):
    periodo = pd.to_numeric(serie_periodo, errors='coerce').fillna(0).astype(int)
    anio = (periodo // 100).astype(float)
    mes = (periodo % 100).astype(float)
    mes = mes.where((mes >= 1) & (mes <= 12), 0.0)
    return anio, mes

def extraer_componentes_fecha(serie_fecha):
    def parse_fecha_sucia(valor):
        texto = "".join(filter(str.isdigit, str(valor).split('.')[0].strip()))[:8]
        if len(texto) == 8: return pd.to_datetime(texto, format="%Y%m%d", errors='coerce')
        if len(texto) in [6, 7]:
            anio, resto = texto[:4], texto[4:]
            if len(resto) == 2: mes, dia = resto[0], resto[1]
            elif len(resto) == 3:
                if int(resto[:2]) <= 12 and int(resto[2:]) > 0: mes, dia = resto[:2], resto[2:]
                else: mes, dia = resto[:1], resto[1:]
            else: return pd.NaT
            return pd.to_datetime(f"{anio}-{mes}-{dia}", errors='coerce')
        return pd.NaT
    fechas = serie_fecha.apply(parse_fecha_sucia)
    return fechas.dt.year.fillna(0).astype(float), fechas.dt.month.fillna(0).astype(float), fechas.dt.day.fillna(0).astype(float)

def procesar_listas_numericas(df, columnas):
    df_limpio = df.copy()
    for col in columnas:
        if col in df_limpio.columns:
            def promediar_cadena(valor):
                if pd.isna(valor): return np.nan
                partes = str(valor).split(',')
                numeros = []
                for p in partes:
                    limpio = "".join(c for c in p if c.isdigit() or c == '.')
                    if limpio:
                        try: numeros.append(float(limpio))
                        except ValueError: pass
                return sum(numeros) / len(numeros) if numeros else np.nan
            
            df_limpio[col] = df_limpio[col].apply(promediar_cadena)
    return df_limpio

def procesar_nuevas_caracteristicas(df):
    df_mod = df.copy()
    df_mod['periodo_anio'], df_mod['periodo_mes'] = extraer_componentes_periodo(df_mod['periodo_anio_mes'])
    df_mod['eett_anio_vig'], df_mod['eett_mes_vig'], df_mod['eett_dia_vig'] = extraer_componentes_fecha(df_mod['eett_fec_ini_vig'])
    df_mod['rango_es_abierto'] = df_mod['rango_fin'].isna().astype(float)
    
    tarifa_agua = pd.to_numeric(df_mod['tarifa_agua'], errors='coerce').fillna(0)
    tarifa_alcanta = pd.to_numeric(df_mod['tarifa_alcanta'], errors='coerce').fillna(0)
    rango_ini = pd.to_numeric(df_mod['rango_ini'], errors='coerce').fillna(0)
    rango_fin_imputado = pd.to_numeric(df_mod['rango_fin'], errors='coerce').fillna(99999)
    cargo_fijo = pd.to_numeric(df_mod['prestador_cargo_fijo'], errors='coerce').fillna(0)
    consumo_prom = pd.to_numeric(df_mod['localidad_consumo_promedio'], errors='coerce').fillna(0)
    vol_asignado = pd.to_numeric(df_mod['eett_categoria_volumen_asignado'].astype(str).str.replace(r'[^\d.]', '', regex=True), errors='coerce').fillna(1e-8)
    
    df_mod['rango_amplitud'] = (rango_fin_imputado - rango_ini).clip(lower=0)
    df_mod['tarifa_total'] = tarifa_agua + tarifa_alcanta
    df_mod['tarifa_total_cuadrado'] = df_mod['tarifa_total'] ** 2
    df_mod['tarifa_diferencial'] = tarifa_agua - tarifa_alcanta
    df_mod['proporcion_alcanta'] = tarifa_alcanta / (tarifa_agua + 1e-8)
    df_mod['relacion_cargo_fijo'] = cargo_fijo / (df_mod['tarifa_total'] + 1e-8)
    df_mod['relacion_consumo_volumen'] = consumo_prom / vol_asignado
    return df_mod

def entrenar_imputador_config(df, config_num):
    valores_imputacion = {}
    for col in config_num.get("imputar_mediana", []):
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            mediana = df[col].median(skipna=True)
            valores_imputacion[col] = mediana if not pd.isna(mediana) else 0
            registrar_progreso(f"Entrenamiento [Imputación] - {col}: Mediana = {valores_imputacion[col]}")
            
    for col in config_num.get("imputar_promedio", []):
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            promedio = df[col].mean(skipna=True)
            valores_imputacion[col] = promedio if not pd.isna(promedio) else 0
            registrar_progreso(f"Entrenamiento [Imputación] - {col}: Promedio = {valores_imputacion[col]:.4f}")
            
    return valores_imputacion

def aplicar_imputador_config(df, config_num, valores_imputacion):
    df_proc = df.copy()
    
    for col in config_num.get("limpiar_texto", []):
        if col in df_proc.columns:
            df_proc[col] = df_proc[col].astype(str).str.replace(r'[^\d.]', '', regex=True)
            df_proc[col] = pd.to_numeric(df_proc[col], errors='coerce')
            
    for col in config_num.get("imputar_mediana", []) + config_num.get("imputar_promedio", []):
        if col in df_proc.columns and col in valores_imputacion:
            df_proc[col] = pd.to_numeric(df_proc[col], errors='coerce').fillna(valores_imputacion[col])
            
    for col in config_num.get("imputar_cero", []):
        if col in df_proc.columns:
            df_proc[col] = pd.to_numeric(df_proc[col], errors='coerce').fillna(0)
            
    for col in config_num.get("imputar_extremo_superior", []):
        if col in df_proc.columns:
            df_proc[col] = pd.to_numeric(df_proc[col], errors='coerce').fillna(99999)
            
    return df_proc

def entrenar_codificador_config(df, config_cat):
    mapa_codificacion = {}
    for col in config_cat.get("binario", []):
        if col in df.columns:
            serie = df[col].map(normalizar_texto)
            conteo = serie.value_counts(dropna=False)
            categoria_base = conteo.index[0] if len(conteo) > 0 else "desconocido"
            mapa_codificacion[col] = {"tipo": "binario", "categoria_base": categoria_base}
            registrar_progreso(f"Entrenamiento [Codificación] - {col}: Binarización (Base={categoria_base})")
            
    for col in config_cat.get("onehot", []):
        if col in df.columns:
            serie = df[col].map(normalizar_texto)
            categorias = list(serie.value_counts(dropna=False).index)
            mapa_codificacion[col] = {"tipo": "onehot", "categorias": categorias}
            registrar_progreso(f"Entrenamiento [Codificación] - {col}: OneHot ({len(categorias)} cols)")
            
    for col in config_cat.get("frecuencia", []):
        if col in df.columns:
            serie = df[col].map(normalizar_texto)
            conteo = serie.value_counts(dropna=False)
            total = len(serie) if len(serie) > 0 else 1
            frecuencias = {cat: freq / total for cat, freq in conteo.items()}
            mapa_codificacion[col] = {"tipo": "frecuencia", "frecuencias": frecuencias}
            registrar_progreso(f"Entrenamiento [Codificación] - {col}: Frecuencia ({len(frecuencias)} cats)")
            
    return mapa_codificacion

def aplicar_codificador_config(df, mapa_codificacion):
    df_cod = df.copy()
    cols_generadas = []
    for col, reglas in mapa_codificacion.items():
        if col not in df_cod.columns:
            continue
        serie = df_cod[col].map(normalizar_texto)
        if reglas["tipo"] == "binario":
            nueva_col = f"{col}__binario"
            df_cod[nueva_col] = (serie == reglas["categoria_base"]).astype(float)
            cols_generadas.append(nueva_col)
        elif reglas["tipo"] == "onehot":
            for cat in reglas["categorias"]:
                nueva_col = f"{col}__{nombre_seguro_columna(cat)}"
                df_cod[nueva_col] = (serie == cat).astype(float)
                cols_generadas.append(nueva_col)
        elif reglas["tipo"] == "frecuencia":
            nueva_col = f"{col}__frecuencia"
            df_cod[nueva_col] = serie.map(reglas["frecuencias"]).fillna(0).astype(float)
            cols_generadas.append(nueva_col)
        df_cod.drop(columns=[col], inplace=True)
    return df_cod, cols_generadas

def limpiar_columnas(df, columnas_a_eliminar):
    cols_existentes = [col for col in columnas_a_eliminar if col in df.columns]
    return df.drop(columns=cols_existentes)

def preparar_export_limpio(df):
    df_export = df.dropna(axis=1, how='all').copy()
    columnas_texto = df_export.select_dtypes(include=['object', 'string']).columns
    for col in columnas_texto:
        serie = df_export[col].astype(str).str.strip()
        vacios = serie.eq("") | serie.str.lower().isin(["nan", "none", "null"])
        if vacios.all():
            df_export.drop(columns=[col], inplace=True)
    return df_export

def inyectar_anomalias(df_limpio, columnas_num):
    num_anomalos = int(len(df_limpio) * 0.3)
    indices_aleatorios = np.random.choice(df_limpio.index, size=num_anomalos, replace=False)
    df_anomalos = df_limpio.loc[indices_aleatorios].copy()
    for col in columnas_num:
        if col in df_anomalos.columns:
            factor = np.random.choice([np.random.uniform(0.5, 1.5), np.random.uniform(2.0, 3.5)], size=num_anomalos)
            desplazamiento = np.random.uniform(-0.15, 0.15, size=num_anomalos)
            df_anomalos[col] = pd.to_numeric(df_anomalos[col], errors='coerce')
            df_anomalos[col] = (df_anomalos[col] * factor) + desplazamiento
    if 'periodo_anio_mes' in df_anomalos.columns:
        ajuste_periodo = np.random.choice([-200, -100, 100, 200, 300], size=num_anomalos)
        df_anomalos['periodo_anio_mes'] = pd.to_numeric(df_anomalos['periodo_anio_mes'], errors='coerce').fillna(0).astype(int) + ajuste_periodo
    df_anomalos['etiqueta_anomalia'] = 1
    df_congruentes = df_limpio.copy()
    df_congruentes['etiqueta_anomalia'] = 0
    return pd.concat([df_congruentes, df_anomalos]).reset_index(drop=True)

def sigmoide(z):
    z = np.clip(z, -250, 250)
    return 1.0 / (1.0 + np.exp(-z))

def entrenar_regresion_logistica(X, y, tasa_aprendizaje=0.01, iteraciones=1000, tolerancia=1e-5, lambda_l2=0.1):
    muestras, caracteristicas = X.shape
    pesos = np.zeros(caracteristicas)
    sesgo = 0.0
    historial_costo = []
    
    for i in range(iteraciones):
        modelo_lineal = np.dot(X, pesos) + sesgo
        predicciones = sigmoide(modelo_lineal)
        epsilon = 1e-9
        
        costo_base = -1/muestras * np.sum(y * np.log(predicciones + epsilon) + (1 - y) * np.log(1 - predicciones + epsilon))
        penalizacion_l2 = (lambda_l2 / (2 * muestras)) * np.sum(pesos ** 2)
        costo = costo_base + penalizacion_l2
        historial_costo.append(costo)

        if i > 0 and abs(historial_costo[-2] - costo) < tolerancia:
            registrar_progreso(f" Convergencia alcanzada tempranamente en la iteración {i+1}. Costo: {costo:.8f}")
            break

        dw = (1 / muestras) * np.dot(X.T, (predicciones - y)) + (lambda_l2 / muestras) * pesos
        db = (1 / muestras) * np.sum(predicciones - y)
        
        pesos -= tasa_aprendizaje * dw
        sesgo -= tasa_aprendizaje * db

        if (i+1) % 200 == 0:
            registrar_progreso(f" Iteración {i+1}/{iteraciones} - Costo: {costo:.8f}")

    return pesos, sesgo, historial_costo

def predecir(X, pesos, sesgo, umbral=0.5):
    modelo_lineal = np.dot(X, pesos) + sesgo
    probabilidades = sigmoide(modelo_lineal)
    clases = [1 if p >= umbral else 0 for p in probabilidades]
    return np.array(clases)

def calcular_metricas(y_real, y_pred):
    TP = np.sum((y_real == 1) & (y_pred == 1))
    TN = np.sum((y_real == 0) & (y_pred == 0))
    FP = np.sum((y_real == 0) & (y_pred == 1))
    FN = np.sum((y_real == 1) & (y_pred == 0))
    exactitud = (TP + TN) / (TP + TN + FP + FN) if (TP + TN + FP + FN) > 0 else 0
    precision = TP / (TP + FP) if (TP + FP) > 0 else 0
    exhaustividad = TP / (TP + FN) if (TP + FN) > 0 else 0
    f1_score = 2 * (precision * exhaustividad) / (precision + exhaustividad) if (precision + exhaustividad) > 0 else 0
    return TP, TN, FP, FN, exactitud, precision, exhaustividad, f1_score

if __name__ == "__main__":
    EJECUTANDO_EN_COLAB = "google.colab" in sys.modules
    BASE_DIR = "/content" if EJECUTANDO_EN_COLAB else "."
    DIR_DATOS = os.path.join(BASE_DIR, "data")
    DIR_RUN = os.path.join(BASE_DIR, "run")
    URL_DATASET = "https://github.com/juanusat/md-u2/raw/refs/heads/main/data/EETT_Dataset.csv"
    NOMBRE_DATASET = "EETT_Dataset.csv"

    os.makedirs(DIR_DATOS, exist_ok=True)
    os.makedirs(DIR_RUN, exist_ok=True)

    marca_tiempo = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    dir_run = os.path.join(DIR_RUN, marca_tiempo)
    os.makedirs(dir_run, exist_ok=True)
    archivo_progreso = os.path.join(dir_run, "progreso.txt")
    archivo_resumen = os.path.join(dir_run, "resumen.txt")

    ruta_dataset = obtener_ruta("data", NOMBRE_DATASET)
    asegurar_dataset_descargado(ruta_dataset)
    df_original = pd.read_csv(ruta_dataset, sep=';', low_memory=False)

    ruta_dataset_original_comas = os.path.join(dir_run, "dataset_original_comas.csv")
    df_original.to_csv(ruta_dataset_original_comas, sep=',', index=False, encoding='utf-8')
    registrar_progreso(f"Dataset original con separador coma guardado en {ruta_dataset_original_comas}")

    cols_num = CONFIG_PIPELINE["columnas_base"]["numericas"]
    cols_cat = CONFIG_PIPELINE["columnas_base"]["categoricas"]

    df_base = df_original[cols_num + cols_cat].copy()
    df_base = procesar_listas_numericas(df_base, CONFIG_PIPELINE["transformaciones_numericas"].get("promediar_listas", []))
    auditar_datos_invalidos(df_base, cols_num, cols_cat, CONFIG_PIPELINE)

    ruta_dataset_limpio = os.path.join(dir_run, "dataset_limpio.csv")
    df_base_export = preparar_export_limpio(df_base)
    df_base_export.to_csv(ruta_dataset_limpio, sep=',', index=False, encoding='utf-8')
    registrar_progreso(f"Dataset limpio guardado en {ruta_dataset_limpio}")

    df_final = inyectar_anomalias(df_base, CONFIG_PIPELINE["anomalias"]["columnas_inyectar"])
    ruta_dataset_anomalias = os.path.join(dir_run, "dataset_con_anomalias_etiquetado.csv")
    df_final.to_csv(ruta_dataset_anomalias, sep=',', index=False, encoding='utf-8')
    registrar_progreso(f"Dataset con anomalías etiquetadas guardado en {ruta_dataset_anomalias}")
    
    df_train, df_test = dividir_entrenamiento_prueba(df_final, proporcion_prueba=0.2)

    df_train_proc = procesar_nuevas_caracteristicas(df_train)
    df_test_proc = procesar_nuevas_caracteristicas(df_test)

    valores_imputacion = entrenar_imputador_config(df_train_proc, CONFIG_PIPELINE["transformaciones_numericas"])
    df_train_imp = aplicar_imputador_config(df_train_proc, CONFIG_PIPELINE["transformaciones_numericas"], valores_imputacion)
    df_test_imp = aplicar_imputador_config(df_test_proc, CONFIG_PIPELINE["transformaciones_numericas"], valores_imputacion)

    mapa_codificacion = entrenar_codificador_config(df_train_imp, CONFIG_PIPELINE["transformaciones_categoricas"])
    df_train_cod, cols_gen = aplicar_codificador_config(df_train_imp, mapa_codificacion)
    df_test_cod, _ = aplicar_codificador_config(df_test_imp, mapa_codificacion)

    df_train_limpio = limpiar_columnas(df_train_cod, CONFIG_PIPELINE["columnas_a_eliminar"])
    df_test_limpio = limpiar_columnas(df_test_cod, CONFIG_PIPELINE["columnas_a_eliminar"])

    columnas_modelo = [c for c in df_train_limpio.columns if c not in cols_cat and c != 'etiqueta_anomalia']
    X_train_raw = df_train_limpio[columnas_modelo].fillna(0).values
    y_train = df_train_limpio['etiqueta_anomalia'].values
    X_test_raw = df_test_limpio[columnas_modelo].fillna(0).values
    y_test = df_test_limpio['etiqueta_anomalia'].values

    medias_X, desv_X = estandarizar_datos_fit(X_train_raw)
    X_train = estandarizar_datos_transform(X_train_raw, medias_X, desv_X)
    X_test = estandarizar_datos_transform(X_test_raw, medias_X, desv_X)

    pesos_optimos, sesgo_optimo, costos = entrenar_regresion_logistica(X_train, y_train, tasa_aprendizaje=0.1, iteraciones=8000, tolerancia=1e-6, lambda_l2=0.5)
    
    y_prediccion = predecir(X_test, pesos_optimos, sesgo_optimo, umbral=0.25)
    TP, TN, FP, FN, acc, prec, rec, f1 = calcular_metricas(y_test, y_prediccion)

    resumen_metricas = f"""========================================
RESUMEN DE RESULTADOS DEL MODELO
========================================
Directorio de ejecución: {dir_run}
Fecha y hora: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

Configuración de la partición:
- Tamaño de Entrenamiento: {len(X_train)}
- Tamaño de Prueba: {len(X_test)}

Matriz de Confusión:
- Verdaderos Positivos (Anomalías detectadas): {TP}
- Verdaderos Negativos (Congruentes correctos): {TN}
- Falsos Positivos (Falsas alarmas): {FP}
- Falsos Negativos (Anomalías omitidas): {FN}

Métricas de Rendimiento:
- Exactitud (Accuracy):      {acc * 100:.2f}%
- Precisión (Precision):     {prec * 100:.2f}%
- Exhaustividad (Recall):    {rec * 100:.2f}%
- Puntuación F1 (F1-Score):  {f1 * 100:.2f}%
========================================"""

    with open(archivo_resumen, "w", encoding="utf-8") as f:
        f.write(resumen_metricas)

    plt.figure(figsize=(8,5))
    plt.plot(costos, color='blue', linewidth=2)
    plt.title('Disminución de la Función de Costo durante el Entrenamiento')
    plt.xlabel('Iteraciones')
    plt.ylabel('Costo (Log-Loss)')
    plt.grid(True)
    plt.savefig(os.path.join(dir_run, "convergencia_costo.png"))
    if EJECUTANDO_EN_COLAB:
        plt.show()
    plt.close()
    
    registrar_progreso("Ejecución finalizada con éxito.")