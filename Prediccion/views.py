from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from Ventas.models import Venta
from Ventas.models import DetalleVenta
from django.db.models import Sum
from django.db.models.functions import ExtractMonth, ExtractYear

# Obtener el año, mes, cantidad vendida por producto  

@api_view(['GET'])
def lista_preddiccion_ventas(request):
    return Response('Bienvenido a la prediccion de ventas')
