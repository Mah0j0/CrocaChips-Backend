import calendar

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

