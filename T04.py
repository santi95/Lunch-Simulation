from collections import deque, namedtuple
from datetime import datetime, timedelta
from Eventos import ENoProgra, EProgra, \
    miembros_uc, carabineros, alumnos, \
    funcionarios, vendedores, dia_nuevo, \
    retornar_producto
import Data
from random import randint
from functools import reduce


class Simulation:
    total_policias = 0
    total_conchas = 0
    total_extremas = 0
    total_ll_hambur = 0

    # Asumimos que los 4 meses son a partir de marzo de este año
    def __init__(self):
        self.ti = datetime.strptime('01/03/2017', '%d/%m/%Y')
        self._tiempo = self.ti
        # Ultimos eventos no programados en días
        self.frio = datetime.strptime('01/03/2017', '%d/%m/%Y')
        self.calor = datetime.strptime('01/03/2017', '%d/%m/%Y')
        self.lluvia_hamburguesas = datetime.strptime('01/03/2017', '%d/%m/%Y')
        self.concha = datetime.strptime('01/03/2017', '%d/%m/%Y')
        self.policias = datetime.strptime('01/03/2017', '%d/%m/%Y')
        self.ultimo_dia_mes = datetime.strptime('01/03/2017', '%d/%m/%Y')
        # Entidades
        self.puestos = []
        self.bancarrota = []

    @property
    def dia_actual(self):
        return self._tiempo

    @dia_actual.setter
    def dia_actual(self, value):
        self._tiempo = value

    def run(self):
        n = ENoProgra(self)
        s = EProgra(self)

        n.generar_lluvia_hamburguesas(self)
        n.generar_concha_acustica(self)
        n.generar_ultimo_dia_mes(self)
        n.generar_llamada_policias(self)

        no_progra = [(self.frio, 'frio'),
                     (self.calor, 'calor'),
                     (self.lluvia_hamburguesas, 'lluvia_hamburguesas'),
                     (self.ultimo_dia_mes, 'ultimo_dia_mes'),
                     (self.concha, 'concha'),
                     (self.policias, 'policias')]
        lista_tiempos = []

        hora_llegada = [(i.hora_llegada_diaria, 'llegada', i) for i in
                        miembros_uc]
        hora_almuerzo = [(i.hora_almuerzo, 'almuerzo', i) for i in miembros_uc]
        hora_puestos = [(i.hora_puesto, 'poner puesto', i) for i in vendedores]
        hora_entrega = [(i.hora_entrega, 'atendieron', i) for i in miembros_uc]

        lista_tiempos.extend(no_progra)
        lista_tiempos.extend(hora_llegada)
        lista_tiempos.extend(hora_almuerzo)
        lista_tiempos.extend(hora_puestos)
        lista_tiempos.extend(hora_entrega)

        lista_tiempos.sort(key=lambda tup: tup[0])
        hora_policias = (
        datetime.strptime('01/03/2019', '%d/%m/%Y'), 'hora_llegada')

        # lista_tiempos = min(lista_tiempos, key = lambda t: t[0])
        minimo = lista_tiempos[0]
        # lista_tiempos.pop(0)

        while minimo[0] < datetime.strptime('01/07/2017', '%d/%m/%Y'):
            self.dia_actual = minimo[0]
            print(self.dia_actual, 'día actual')
            if minimo[1] == 'frio':
                print('Frio')
                Simulation.total_extremas += 1
            if minimo[1] == 'calor':
                print('Calor')
                Simulation.total_extremas += 1
            if minimo[1] == 'ultimo_dia_mes':
                print('dia final mes')
                s.recalcular_mesada()
                lista_tiempos.pop(0)
                n.generar_ultimo_dia_mes(
                    self)  # Generamos el próximo ultimo día del mes
                for i in vendedores:
                    nv = i.contador_no_venta
                    ns = i.contador_no_stock
                    for j in i.dict_productos:
                        if i.nombre != 'Quik':
                            prod = retornar_producto(j)
                            prod.precio = int(prod.precio) + 0.06 * ns
                            prod.precio = int(prod.precio) - 0.05 * nv

                    if nv >= 20 and i.nombre != 'Quik':
                        i.entidad = 'Bancarrota'
                        pos = vendedores.index(i)
                        vendedores.pop(pos)
                        self.bancarrota.append(i)

            if minimo[1] == 'concha':
                print('concha')
                n.generar_concha_acustica(self)
                pos = lista_tiempos.index(minimo)
                lista_tiempos.pop(pos)
                self.dia_actual += timedelta(microseconds=1)
                Simulation.total_conchas += 1
            if minimo[1] == 'lluvia_hamburguesas':
                n.generar_lluvia_hamburguesas(self)
                print('lluvia hamburguesas')
                Simulation.total_ll_hambur += 1

            if minimo[1] == 'policias':
                print('Se llamó a los policias')
                n.generar_llamada_policias(self)
                hora_policias = (
                minimo[0] + timedelta(hours=13, minutes=(randint(0, 40))),
                'hora_llegada')
                Simulation.total_policias += 1

            if minimo[1] == 'hora_llegada':
                fecha_cosas = datetime(minimo[0].year, minimo[0].month,
                                       minimo[0].day)
                tweak = [i for i in list(set(ENoProgra.lista_eventos)) if i[
                    0] == fecha_cosas]  # el set nos toma los elementos distintos de la lista
                print('llegaron los pacos a la feria')
                lista_tiempos.pop(0)
                n.revision_policia(self, tweak)
                hora_policias = (
                datetime.strptime('01/03/2019', '%d/%m/%Y'), 'hora_llegada')


            elif minimo[1] == 'llegada':
                s.llegar_campus(minimo[2], self)
            elif minimo[1] == 'almuerzo':
                fecha_cosas = datetime(minimo[0].year, minimo[0].month,
                                       minimo[0].day)
                tweak = [i for i in list(set(ENoProgra.lista_eventos)) if i[
                    0] == fecha_cosas]  # el set nos toma los elementos distintos de la lista
                # Nos dice que eventos no programados están pasando el mismo día
                s.almorzar(minimo[2], self, tweak)
            elif minimo[1] == 'poner puesto':
                s.instalar_puesto(self, minimo[2])
            elif minimo[1] == 'atendieron':
                fecha_cosas = datetime(minimo[0].year, minimo[0].month,
                                       minimo[0].day)
                tweak = [i for i in list(set(ENoProgra.lista_eventos)) if
                         i[0] == fecha_cosas]
                # Nos dice que eventos están pasando el mismo día
                s.atendieron(self, minimo[2], tweak)
            else:
                print(minimo[1], 'Que pasó')

            n = ENoProgra(self)
            lista_tiempos = []
            no_progra = [(self.frio, 'frio'),
                         (self.calor, 'calor'),
                         (self.lluvia_hamburguesas, 'lluvia_hamburguesas'),
                         (self.concha, 'concha'),
                         (self.ultimo_dia_mes, 'ultimo_dia_mes'),
                         (self.policias, 'policias')]
            lista_tiempos.extend(no_progra)
            lista_tiempos.append(hora_policias)

            hora_llegada = [(i.hora_llegada_diaria, 'llegada', i) for i in
                            miembros_uc if not i.in_campus]
            hora_almuerzo = [(i.hora_almuerzo, 'almuerzo', i) for i in
                             miembros_uc if not i.almuerzo]
            hora_puestos = [(i.hora_puesto, 'poner puesto', i) for i in
                            vendedores if not i.instalado]
            hora_entrega = [(i.hora_entrega, 'atendieron', i) for i in
                            miembros_uc if not i.almuerzo_entregado]

            # Si las 2 listas están vacías, poner en 0 todo y correrlo
            # Falta agregar a esta lista los tiempos del día de armar y poner los puestos
            dia_siguiente = self.dia_actual + timedelta(days=1)
            if len(hora_almuerzo) == 0 and len(
                    hora_llegada) == 0:  # If se acabó el día
                if dia_siguiente.isoweekday() != 6 and dia_siguiente.isoweekday() != 7:
                    n.generar_ultimo_dia_mes(self)
                    for i in miembros_uc:

                        i.in_campus = False
                        i.almuerzo = False
                        i.almuerzo_entregado = False
                        i.hora_entrega = datetime.strptime('01/05/2019',
                                                           '%d/%m/%Y')  # Un día más allá para que no moleste

                        if i.entidad == 'Alumno':
                            i.mesada_diaria = i.mesada_diaria_mes
                        if i.entidad == 'Funcionario':
                            i.presu_diario = i.presu_diario_mes

                    for i in vendedores:
                        if i.stock == i.stock_inicial:
                            i.contador_no_venta += 1  # No vendió nada
                            # lista1 = Data.Parametros.dict['stock_vendedores'].split(';')        #Definimos el stock del día siguiente
                            # i.stock = randint(int(lista1[0]), int(lista1[1]))
                            # i.stock_inicial = i.stock

                    Data.Persona.lista_contador_no_stock.append(
                        Data.Persona.contador_no_stock_diario)
                    Data.Persona.contador_no_stok_diario = 0

                    self.dia_actual = dia_nuevo(self.dia_actual) + timedelta(
                        days=1)
                    s = EProgra(self)

                    hora_policias = (
                    datetime.strptime('01/05/2019', '%d/%m/%Y'),
                    'hora_llegada')

                    hora_llegada = [(i.hora_llegada_diaria, 'llegada', i) for i
                                    in miembros_uc if not i.in_campus]
                    hora_almuerzo = [(i.hora_almuerzo, 'almuerzo', i) for i in
                                     miembros_uc if not i.almuerzo]
                    hora_puestos = [(i.hora_puesto, 'poner puesto', i) for i in
                                    vendedores]
                    hora_entrega = [(i.hora_entrega, 'atendieron', i) for i in
                                    miembros_uc if not i.almuerzo_entregado]

                else:
                    self.dia_actual += timedelta(days=1)
                    lista_tiempos.append((self.dia_actual, 'Fin de Semana'))

            lista_tiempos.extend(hora_llegada)
            lista_tiempos.extend(hora_almuerzo)
            lista_tiempos.extend(hora_puestos)
            lista_tiempos.extend(hora_entrega)

            lista_tiempos.sort(key=lambda tup: tup[0])
            minimo = lista_tiempos[0]

    def estadisticas(self):
        print('-------Estadísticas-------')
        # 1 Estadística
        promedio_confiscado = reduce(lambda x, y: x + y,
                                     Data.Persona.lista_precio_confisca) / len(
            Data.Persona.lista_precio_confisca)
        print(promedio_confiscado)
        # 2
        '''Falta'''
        # 3
        print(Data.Persona.confisca_jekyll)
        print(Data.Persona.confisca_hide)
        # 4
        print(Simulation.total_policias)
        # 5
        print(Simulation.total_conchas)
        # 6
        print(Simulation.total_extremas)
        # 7
        print(Simulation.total_ll_hambur)
        # 8
        '''Promedio de horarios'''
        # 9
        print(EProgra.total_no_almorzaron)
        # 10
        '''Escenarios que todavía no hago'''
        # 11
        print('Vendedor: \t \t número intoxicados')
        for i in vendedores:
            print(i.nombre + ' ' + i.apellido + ':\t\t\t' + str(
                i.intoxicados_mi_culpa))
        # 12
        print(EProgra.total_descompuestas)
        # 13
        'Falta'
        # 14
        no_stock = reduce(lambda x, y: x + y,
                          Data.Persona.lista_contador_no_stock) / len(
            Data.Persona.lista_contador_no_stock)
        print(no_stock)
        # 15
        print(ENoProgra.engaños)


w = Simulation()
w.run()

w.estadisticas()
