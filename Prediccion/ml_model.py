# prediccion/ml_model.py

import joblib
import numpy as np
import os

# Ruta al archivo .pkl
RUTA_MODELO = os.path.join(os.path.dirname(__file__), 'modelo', 'modelo_xgboost.pkl')

# Cargar el modelo una vez
modelo = joblib.load(RUTA_MODELO)

def predecir_ventas(anio, mes, cantidad_mes_anterior):
    X = np.array([[anio, mes, cantidad_mes_anterior]])
    prediccion = modelo.predict(X)
    return float(prediccion[0])
