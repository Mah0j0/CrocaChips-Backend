import requests
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from Ventas.models import Venta
from Ventas.models import DetalleVenta
from Productos.models import Producto
from django.db.models import Sum
from datetime import datetime
from django.db.models.functions import ExtractMonth, ExtractYear
from .utils import obtener_nombre_mes

PREDICCION_API_URL = "https://web-production-cc23.up.railway.app/"



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def lista_prediccion_general(request):
    try:
        # Obtener fecha actual
        hoy = datetime.today()
        año_actual = hoy.year
        mes_actual = hoy.month

        # Calcular próximo mes y su año correspondiente
        if mes_actual == 12:
            año_pred = año_actual + 1
            mes_pred = 1
        else:
            año_pred = año_actual
            mes_pred = mes_actual + 1

        # Calcular mes anterior al mes de predicción
        if mes_pred == 1:
            año_anterior = año_pred - 1
            mes_anterior = 12
        else:
            año_anterior = año_pred
            mes_anterior = mes_pred - 1

        # Obtener cantidad vendida en el mes anterior
        cantidad_anterior = DetalleVenta.objects.filter(
            id_venta__fecha__year=año_anterior,
            id_venta__fecha__month=mes_anterior
        ).aggregate(cantidad_total=Sum('cantidad'))['cantidad_total'] or 0

        # Consumir API externa
        payload = {
            "año": año_pred,
            "mes": mes_pred,
            "cantidad_anterior": cantidad_anterior
        }

        respuesta = requests.post(f"{PREDICCION_API_URL}/prediccion-general/", json=payload)

        if respuesta.status_code != 200:
            return Response({'error': 'Error al consumir el modelo de predicción'}, status=502)

        resultado = respuesta.json()

        return Response({
            "año_prediccion": resultado["año"],
            "mes_prediccion": obtener_nombre_mes(resultado["mes"]),
            "cantidad_anterior": resultado["cantidad_anterior"],
            "prediccion": resultado["prediccion"]
        }, status=200)

    except Exception as e:
        return Response({'error': str(e)}, status=500)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def lista_prediccion_producto(request):
    try:
        # Calcular próximo mes y año
        hoy = datetime.today()
        año_actual = hoy.year
        mes_actual = hoy.month

        if mes_actual == 12:
            año_pred = año_actual + 1
            mes_pred = 1
        else:
            año_pred = año_actual
            mes_pred = mes_actual + 1

        predicciones = []

        # Obtener todos los productos
        productos = Producto.objects.all()

        for producto in productos:
            payload = {
                "id_producto": producto.id_producto,
                "año": año_pred,
                "mes": mes_pred,
            }

            respuesta = requests.post(f"{PREDICCION_API_URL}/prediccion-productos/", json=payload)

            if respuesta.status_code == 200:
                resultado = respuesta.json()
                predicciones.append({
                    "año_prediccion": resultado["año"],
                    "mes_prediccion": obtener_nombre_mes(resultado["mes"]),
                    "id_producto": resultado["id_producto"],
                    "nombre_producto": producto.nombre,
                    "prediccion": resultado["prediccion"]
                })
            else:
                predicciones.append({
                    "id_producto": producto.id_producto,
                    "nombre_producto": producto.nombre,
                    "error": "Error al predecir"
                })

        return Response(predicciones, status=200)

    except Exception as e:
        return Response({'error': str(e)}, status=500)