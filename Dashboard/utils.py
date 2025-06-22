import calendar
from datetime import date, timedelta
from calendar import monthrange

MESES = {
    1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril',
    5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto',
    9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
}

def obtener_nombre_mes(mes_numero):
    return MESES.get(mes_numero, "Mes inválido")

def obtener_nombre_semana(numero_semana, inicio, fin):
    mes_nombre = MESES.get(inicio.month, "Mes")
    return f"Sem {numero_semana} ({inicio.day}-{fin.day} {mes_nombre})"


def resta_meses(fecha, meses):
    año = fecha.year
    mes = fecha.month - meses
    dia = fecha.day

    while mes <= 0:
        mes += 12
        año -= 1

    ultimo_dia_mes = monthrange(año, mes)[1]
    if dia > ultimo_dia_mes:
        dia = ultimo_dia_mes

    return date(año, mes, dia)