from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from Ventas.models import Venta
from Ventas.models import DetalleVenta
from django.db.models import Sum
from datetime import datetime
from django.db.models.functions import ExtractMonth, ExtractYear


from .ml_model import predecir_ventas  # Asegúrate que esté implementado

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def lista_prediccion_ventas(request):
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

        # Predecir
        prediccion = predecir_ventas(año, mes, cantidad_anterior)

        return Response({
            'año_prediccion': año,
            'mes_prediccion': mes,
            'cantidad_anterior': cantidad_anterior,
            'prediccion': round(prediccion)
        }, status=200)

    except (TypeError, ValueError) as e:
        return Response({'error': f'Datos inválidos: {str(e)}'}, status=400)
    except Exception as e:
        return Response({'error': str(e)}, status=500)