
MESES = {
    1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril',
    5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto',
    9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
}

DIAS = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']

def mapear_meses(ventas_meses_raw):
    for item in ventas_meses_raw:
        item['mes'] = MESES[item['mes']]
    return ventas_meses_raw




def mapear_semana(ventas_semana_raw):
    for item in ventas_semana_raw:
        item['fecha'] = DIAS[item['fecha'].weekday()]
    return ventas_semana_raw