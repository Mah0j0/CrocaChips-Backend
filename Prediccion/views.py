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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def lista_prediccion_general(request):
    try:
        # Obtener año y mes del body
        año = request.data.get('año')
        mes = request.data.get('mes')

        if not año or not mes:
            return Response({'error': 'Se requieren los campos "año" y "mes".'}, status=400)

        año = int(año)
        mes = int(mes)

        if mes < 1 or mes > 12:
            return Response({'error': 'El mes debe estar entre 1 y 12.'}, status=400)

        # Calcular el mes anterior
        if mes == 1:
            año_anterior = año - 1
            mes_anterior = 12
        else:
            año_anterior = año
            mes_anterior = mes - 1

        # Obtener cantidad vendida en el mes anterior
        cantidad_anterior = DetalleVenta.objects.filter(
            id_venta__fecha__year=año_anterior,
            id_venta__fecha__month=mes_anterior
        ).aggregate(cantidad_total=Sum('cantidad'))['cantidad_total'] or 0

        # Consumir API externa
        payload = {
            "año": año,
            "mes": mes,
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

    except (TypeError, ValueError) as e:
        return Response({'error': f'Datos inválidos: {str(e)}'}, status=400)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def lista_prediccion_producto(request):
    try:
        # Obtener año, mes y producto_id del body
        id_producto = request.data.get('id_producto')
        año = request.data.get('año')
        mes = request.data.get('mes')
        

        if not all([id_producto, año, mes]):
            return Response({'error': 'Se requieren los campos "id_producto", "año" y "mes".'}, status=400)

        id_producto = int(id_producto)
        año = int(año)
        mes = int(mes)

        if mes < 1 or mes > 12:
            return Response({'error': 'El mes debe estar entre 1 y 12.'}, status=400)

        # Llamar al modelo de predicción sin cantidad_anterior
        payload = {
            "id_producto": id_producto,
            "año": año,
            "mes": mes,
        }

        respuesta = requests.post(f"{PREDICCION_API_URL}/prediccion-productos/", json=payload)

        if respuesta.status_code != 200:
            return Response({'error': 'Error al consumir el modelo de predicción'}, status=502)

        resultado = respuesta.json()

        producto = Producto.objects.get(id_producto=id_producto)

        return Response({
            "año_prediccion": resultado["año"],
            "mes_prediccion": obtener_nombre_mes(resultado["mes"]),
            "id_producto": resultado["id_producto"],
            "nombre_producto": producto.nombre,
            "prediccion": resultado["prediccion"]
        }, status=200)

    except (TypeError, ValueError) as e:
        return Response({'error': f'Datos inválidos: {str(e)}'}, status=400)
    except Exception as e:
        return Response({'error': str(e)}, status=500)