import T04

class Parametros:
    dict = {}
    lista_lineas = []
    def __init__(self, nombre, dato):
        self.nombre = nombre
        self.dato = dato
        cosa = {self.nombre : self.dato}
        Parametros.dict.update(cosa)


archivo = 'escenarios.csv'
with open(archivo, encoding = 'utf-8') as file:
    datos = (linea for linea in file)
    parametros = next(datos).strip().split(', ')
    linea = next(datos, None)
    while linea != None:
        linea = linea.strip().split(',')
        for i in range(len(parametros)):
            par = Parametros(parametros[i], linea[i])
        cosa = Parametros.dict.copy()
        Parametros.lista_lineas.append(cosa)
        dict = {}
        linea = next(datos, None)


#Le agregabamos los parametros de cada uno de estos escenarios y comparamos
for i in range(len(Parametros.lista_lineas)):
    T04.Simulation.run()

