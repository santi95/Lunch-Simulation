from random import random, randint
from collections import deque
from datetime import datetime, timedelta

class Persona:
    lista = []
    lista_precio_confisca = []
    confisca_jekyll = 0
    confisca_hide = 0
    total_confisca = confisca_hide + confisca_jekyll
    contador_no_stock_diario = 0
    lista_contador_no_stock = []

    def __init__(self, nombre, apellido, edad, vendedores_prefe, entidad, tipo_comida, personalidad):
        self.nombre = nombre
        self.apellido = apellido
        self.edad = edad
        self.vendedores_prefe = vendedores_prefe
        self.entidad = entidad
        self.in_campus = False
        #Miembros UC
        self.hora_llegada_diaria = ""
        self.hora_almuerzo = ''
        self.almuerzo = False       #Si ya almorzó
        self.snack = False
        self.hora_snack = ''
        self.paciencia = 0
        self.almuerzo_entregado = False                                 #Si terminó o no la cola
        self.hora_entrega = datetime.strptime('01/05/2019', '%d/%m/%Y') #A la hora a la cual le entregan su comida
        self.comida_diaria = str                                        #Lo que le compra al día
        self.le_compra = object                                         #al objeto vendedor al cual le compra la comida del día
        #Si estudiante
        self.mesada = int
        self.mesada_diaria = int    #lo que puede gastar total en un dia
        self.mesada_diaria_mes = self.mesada_diaria
        #Si Funcionario
        self.presu_diario = 0       #Presupuesto diario de comida
        self.presu_diario_mes = self.presu_diario
        self.ultimo_almuerzo = ''
        #Si vendedor
        self.tipo_comida = tipo_comida
        self.puesto = ''                    #Puede ser Snack o tipo de almuerzos
        self.velocidad = 0                  #Velocidad con la que procesa cada persona
        self.cola = deque()                 #Cola de clientes esperando a comprar sus productos
        self.asustado = False               #Estado del vendedor luego de que aparece un carabinero se pone True
        self.dias_susto = 0                 #Se saca de parametros y se pone aquí más adelante
        self.dias_asustado = 0              #Cuenta los días que lleva asustado, para luego sacarlo de ese estado
        self.instalado = False              #Si está o no listo para vender
        self.stock = 0                      #Cuantos productos más puede vender
        self.stock_inicial = 0              #cuenta cuantos días está asustado luego lo deja voler
        self.contador_no_stock = 0          #suma 1 cada vez en el mes que el vendedor se queda sin stock de todos sus productos
        self.contador_no_venta = 0          #suma 1 cada vez que un vendedor no vende nada en un día
        self.permiso = False                #la probabilidad que el vendedor tenga un permiso de venta del lugar
        self.hora_puesto = ''               #A la hora que el vendedor empieza a vender
        self.dict_productos = {}            #Diccionario con los productos y sus cantidades
        self.venta = 0
        self.entrega = 0
        self.intoxicados_mi_culpa = 0
        #Si carabinero
        self.personalidad = personalidad    #Si Jeckyl o Hide
        self.tasa_productos = 0             #
        self.prob_engaño = 0


    def __repr__(self):
        return self.nombre + ' ' + self.apellido


class Parametros:
    dict = {}
    def __init__(self, nombre, dato):
        self.nombre = nombre
        self.dato = dato
        cosa = {self.nombre : self.dato}
        Parametros.dict.update(cosa)

class Productos:
    lista = []
    def __init__(self, producto, tipo, precio, calorias, tasa_putre, vendido_en):
        self.producto = producto
        self.tipo = tipo
        self._precio = precio
        self.precio_incial = precio
        self.calorias = calorias
        self.tasa_putre = tasa_putre
        self.vendido_en = vendido_en

    def __repr__(self):
        return self.producto + ' ' + self.tipo + ' ' + self.precio + ' ' + self.calorias + ' ' + self.tasa_putre + ' ' + self.vendido_en
    @property
    def precio(self):
        return self._precio
    @precio.setter
    def precio(self, value):
        if int(self._precio) < 0.01*int(self.precio_incial):
            self._precio == 0.01*int(self.precio_incial)


with open('productos.csv', encoding = 'utf-8') as file:
    datos = (linea for linea in file)
    nombres = next(datos)
    nombres = nombres.strip()
    nombres = nombres.split("; ")
    #Por si nos entregan las bases de datos en un orden distinto
    pos0 = nombres.index("Producto")
    pos1 = nombres.index("Tipo")
    pos2 = nombres.index("Precio")
    pos3 = nombres.index("Calorias")
    pos4 = nombres.index("Tasa Putrefacción")
    pos5 = nombres.index("Vendido en")
    nombres = next(datos)
    while nombres != None:
        nombres = nombres.strip().split('; ')
        prod = Productos(nombres[pos0],
                         nombres[pos1],
                         nombres[pos2],
                         nombres[pos3],
                         nombres[pos4],
                         nombres[pos5])
        Productos.lista.append(prod)
        nombres = next(datos, None)

archivo = 'parametros_iniciales.csv'
with open(archivo, encoding = 'utf-8') as file:
    datos = (linea for linea in file)
    parametros = next(datos).strip().split(', ')
    numeros = next(datos).strip().split(',')
    for i in range(len(parametros)):
        par = Parametros(parametros[i], numeros[i])




with open('personas.csv', encoding = 'utf-8') as file:
    datos = (linea for linea in file)
    fila = next(datos)
    fila = fila.strip()
    fila = fila.split("; ")
    #Por si nos entregan las bases de datos en un orden distinto
    pos_nombre = fila.index("Nombre")
    pos_apellido = fila.index("Apellido")
    pos_edad = fila.index("Edad")
    pos_vendedores_prefe = fila.index("Vendedores de Preferencia")
    pos_entidad = fila.index("Entidad")
    pos_tipo_comida = fila.index("Tipo Comida")
    pos_personalidad = fila.index("Personalidad")
    fila = next(datos, None)


    while fila != None:
        fila = fila.split("; ")
        person = Persona(fila[pos_nombre],
                         fila[pos_apellido],
                         fila[pos_edad],
                         fila[pos_vendedores_prefe].split(' - '),
                         fila[pos_entidad],
                         fila[pos_tipo_comida][:-1],
                         fila[pos_personalidad])
        person.vendedores_prefe.append('Quik Devil')
        #Lee los datos directos y luego los completa usando los parametros iniciales

        if person.entidad == 'Alumno':
            person.mesada = int(Parametros.dict['base_mesada'])*(1 + (random())**random())*20
            person.mesada_diaria = round(person.mesada/20)
            person.mesada_diaria_mes = person.mesada_diaria

        if person.entidad == 'Funcionario':
            person.presu_diario = int(Parametros.dict['dinero_funcionarios'])
            person.presu_diario_mes = person.presu_diario

        if person.entidad == 'Vendedor':
            person.cola = deque()
            lista = Parametros.dict['rapidez_vendedores'].split(';')
            person.velocidad = randint(int(lista[0]), int(lista[1]))
            lista1 = Parametros.dict['stock_vendedores'].split(';')
            person.stock_inicial = randint(int(lista1[0]), int(lista1[1]))
            susto = Parametros.dict['días_susto']
            person.dias_susto = int(susto)
            prob_permiso = Parametros.dict['probabilidad_permiso']
            probabilidad = random()
            if probabilidad > float(prob_permiso):
                person.permiso = True

        if person.entidad == 'Carabinero':
            perso_jekyll = Parametros.dict['personalidad_jekyll'].split(';')
            perso_hide = Parametros.dict['personalidad_hide'].split(';')
            if person.personalidad == 'Dr. Jekyll':
                person.tasa_productos = float(perso_jekyll[0])
                person.prob_engaño = float(perso_jekyll[1])
            else:
                person.tasa_productos = float(perso_hide[0])
                person.prob_engaño = float(perso_hide[1])

        Persona.lista.append(person)
        fila = next(datos, None)

    #luego creamos al quick deli como vendedor
    quick = Persona('Quik', 'Devil', '', '', 'Vendedor', 'Todas', '')
    #Seteamos el stock del quik devil como 10000 para que no se acabe nunca
    quick.stock = 100000000
    quick.stock_inicial = 100000000
    quick.tipo_comida = 'Todas'
    for i in Productos.lista:
        quick.dict_productos.update({i.producto: int(i.precio)})

    quick.instalado = True
    Persona.lista.append(quick)

# print(Parametros.dict)
# print(len(Persona.lista))
# for i in Persona.lista:
#     print(i.entidad)


