from random import randint, choice, expovariate, random
from datetime import datetime, timedelta
import Data
import numpy
import calendar
from math import exp

def dia_nuevo(dia):
    año1 = dia.year
    mes1 = dia.month
    dia1 = dia.day
    return datetime(año1, mes1, dia1)

def retornar_vendedor(nombre):
    vendedor = [i for i in vendedores if (i.nombre + ' ' + i.apellido) == nombre if i.entidad == 'Vendedor']

    if len(vendedor) != 0:
        return vendedor[0]
    else:
        quik = [i for i in vendedores if (i.nombre + ' ' + i.apellido) == 'Quik Devil']
        quik[0].tipo_comida = 'Todas'
        return quik[0]

def retornar_producto(nombre):
    prod = [i for i in Data.Productos.lista if i.producto == nombre]
    return prod[0]

def calidad_producto(producto, hora, calor):
    año = hora.year
    mes = hora.month
    dia = hora.day

    tiempo = hora - datetime(año, mes, dia, 8)
    tiempo = (tiempo.total_seconds()/60)
    tasa = int(producto.tasa_putre)
    putre = 1 - exp(-(tiempo/tasa)) + (1 - exp(-(tiempo/tasa)))*calor
    if putre > 1:
        putre = 1       #Pude haber usado una property pero así era más facil
    if putre <0.00001:
        EProgra.total_descompuestas += 1
    calidad = (int(producto.calorias) * ((1 - putre)**4)) / (int(producto.precio)**(4/5))
    return calidad

personas = Data.Persona.lista                                           #Todos
miembros_uc = [i for i in Data.Persona.lista if i.entidad == 'Alumno'   #Miembros UC
               or i.entidad == 'Funcionario']        
carabineros = [i  for i in personas if i.entidad == 'Carabinero']       #Fiscalizan
alumnos = [i for i in personas if i.entidad == 'Alumno']                #compran Comida
funcionarios = [i  for i in personas if i.entidad == 'Funcionario']     #Conpran Comida
vendedores = [i  for i in personas if i.entidad == 'Vendedor']          #Conpran Comida

prod_mexicanos = [i for i in Data.Productos.lista if i.vendido_en == 'Puesto de comida mexicana']
prod_chinos = [i for i in Data.Productos.lista if i.vendido_en == 'Puesto de comida china']
prod_snacks = [i for i in Data.Productos.lista if i.vendido_en == 'Puesto de snacks']


class ENoProgra:
    lista_eventos = []
    engaños = 0

    def __init__(self, simu):
        self.generar_temperatura_extrema(simu)
        #self.generar_lluvia_hamburguesas(simu)
        #self.generar_concha_acustica(simu)
        #self.generar_llamada_policias(simu)
        #self.generar_ultimo_dia_mes(simu)

    def generar_ultimo_dia_mes(self, simu):
        dia = simu.dia_actual
        dia = dia_nuevo(dia)
        dia = dia + timedelta(days = 1)
        mes = dia.month
        año = dia.year
        simu.ultimo_dia_mes = datetime(año, mes, calendar.monthrange(año, mes)[1])
        ENoProgra.lista_eventos.append((simu.ultimo_dia_mes, 'ultimo_dia'))


    def generar_temperatura_extrema(self, simu):
        extra = timedelta(days = randint(2,20))
        extra2 = timedelta(days = randint(2,20))
        elec = random()
        simu.dia_actual = dia_nuevo(simu.dia_actual)
        if elec <0.5:
            simu.frio = simu.dia_actual + extra
            simu.calor = simu.frio + extra2
        else:
            simu.calor = simu.dia_actual + extra
            simu.frio = simu.calor + extra2

        ENoProgra.lista_eventos.append((simu.frio, 'frio'))
        ENoProgra.lista_eventos.append((simu.calor, 'frio'))


    def generar_lluvia_hamburguesas(self, simu):
        udia = max(simu.frio, simu.calor)
        dia = dia_nuevo(simu.dia_actual)
        #diferencia en segundos
        dif = (dia - udia).total_seconds()
        #pero la diferencia en dias
        dif = dif/86400
        #genera la distancia a la proxima lluvia de hambuguesas
        tpo = expovariate(1/(21 - dif))
        #redondea para que sea todo un día de lluvia de hamburguesas
        tpo = round(tpo)
        #Si da el día 3.5 hay lluvia de hamburguesas en el día 4
        tpo = timedelta(days = tpo)
        simu.lluvia_hamburguesas = dia + tpo
        ENoProgra.lista_eventos.append((simu.lluvia_hamburguesas, 'lluvia_hamburguesas'))
        ENoProgra.lista_eventos.append((simu.lluvia_hamburguesas + timedelta(days = 1), 'lluvia_hamburguesas2'))


    def generar_concha_acustica(self, simu):
        pconcha = Data.Parametros.dict['concha_estéreo']
        udia = simu.concha
        dia = dia_nuevo(simu.dia_actual)
        bool = False
        while bool == False:
            dif_en_semanas = ((dia - udia).total_seconds())/604800
            if dia.isoweekday() == 5:
                prob = random()
                if dif_en_semanas >= 4 or prob < float(pconcha):
                    simu.concha = dia
                    bool = True
                dia += timedelta(days = 1)
            else:
                dia += timedelta(days = 1)
        ENoProgra.lista_eventos.append((simu.concha, 'concha'))


    def generar_llamada_policias(self, simu):
        dia = dia_nuevo(simu.dia_actual)
        tasa = float(Data.Parametros.dict['llamado_policial'])
        tpo = timedelta(days = round(expovariate(tasa)))
        simu.policias = dia + tpo
        hora_aparicion_policias = simu.policias + timedelta(hours = randint(11, 15))
        ENoProgra.lista_eventos.append((simu.policias, 'policias', hora_aparicion_policias))

    def revision_policia(self, simu, eventos):
        carabinero = choice(carabineros)
        strings = [i[1] for i in eventos]
        calor = 0
        if 'calor' in strings:
            calor = 1

        for i in simu.puestos:
            suerte = random()
            if suerte < carabinero.prob_engaño:
                ENoProgra.engaños += 1
            if i.permiso and suerte < carabinero.prob_engaño:
                #atrasamos el tiempo de todas las peronas en cola
                #no me queda tiempo para hacer que al que están atendiendo vuelva a la cola, por lo tanto asumimos
                #que el vendedor siemplemente le da la comida rápido y el estudiante corre por su vida mientras que el vendedor
                #reza para que no lo reten por hacer la última venta
                for k in i.cola:
                    k.hora_entrega += timedelta(minutes = 40 / len(simu.puestos))

                #calculamos la putrefacción de todos sus productos
                #Si tienen el permiso siempre se les revisa sus productos
                for j in i.dict_productos:
                    '''#Asusimos que la calidad tiene que ser menor a 0.01 para que sea confiscado
                    Elegimos un número tan bajo porque segun la formula las calidades son muy bajas
                    Como son calidades muy bajas, los alumnos se enferman mucho y rapidamente nos quedamos sin vendedores,
                    por lo tanto por resultados prácticos haremos que se confisque el stock con calidad 0.01'''
                    prod = retornar_producto(j)
                    cal = calidad_producto(prod, simu.dia_actual, calor)
                    if cal < 0.01:
                        i.stock = 0
                        i.contador_no_stock += 1
                        Data.Persona.contador_no_stock_diario += 1
                        estado = True
                        break


                perdida = 0 #Perdida Inicial
                if estado  == True:
                    #Se procede a la confiscación
                    for j in i.dict_productos:
                        '''Se confiscan todos los productos'''
                        prod = retornar_producto(j)
                        perdida += int(prod.precio) * int(i.dict_productos[j])
                        '''Se confisca el precio del producto por la cantidad que le quedaban de cada uno'''
                    Data.Persona.lista_precio_confisca.append(perdida)

                    if carabinero.personalidad == 'Dr. Jekyll':
                        Data.Persona.confisca_jekyll += 1
                    else:
                        Data.Persona.confisca_hide += 1


            if not i.permiso:
                #AL correr no pierde stock, se lo lleva para ser reseteado al día siguiente
                i.asustado = True
                i.instalado = False
                ps = simu.puestos.index(i)
                simu.puestos.pop(ps)        #Sacamos a los vendedores que ya no tienen stock y por lo tanto se van a sus casa


class EProgra:
    total_no_almorzaron = 0
    total_descompuestas = 0
    cambio_fila = 0
    def __init__(self, simu):
        #Reseteamos los días
        self.tiempo_llegar_campus(simu)
        self.tiempo_almorzar(simu)
        self.tiempo_snack(simu)
        self.tiempo_instalar_puestos(simu)
        self.definir_paciencia()
        #for i in Data.Productos.lista:
        #for i in


    def definir_paciencia(self):
        for i in miembros_uc:
            paciencia = Data.Parametros.dict['limite_paciencia'].split(';')
            i.paciencia = randint(int(paciencia[0]), int(paciencia[1]))


    def tiempo_llegar_campus(self, simu):
        #moda es en horasz
        moda = float(Data.Parametros.dict['moda_llegada_campus'])/60
        for i in miembros_uc:
            #240 minutos son 4 horas
            hora = numpy.random.triangular(0, moda, 4)
            i.hora_llegada_diaria = simu.dia_actual + timedelta(hours = 11 + hora)
            #Crea en todos los miembros uc una hora de llegada al campus del día
            snack = random()
            if snack <= 0.5:
                i.snack = True

    def llegar_campus(self, persona, simu):            #Snack
        hora = persona.hora_llegada_diaria
        print('Llego la persona ' + str(persona.nombre) +
              ' llegó al campus exactamente el '  + str(hora))
        persona.in_campus = True
        #Agregarlo a la fila del snack de uno de sus vendedores preferidos


    def tiempo_almorzar(self, simu):
        dia = dia_nuevo(simu.dia_actual)
        #Hay un error de +- 1 persona en esta parte de la simulación
        miembros_uc = [i for i in Data.Persona.lista if i.entidad == 'Alumno' or i.entidad == 'Funcionario']
        total = len(miembros_uc)
        cant_per_x = int(float(Data.Parametros.dict['distribución_almuerzo'].split(';')[0])*0.01*total)
        cant_per_y = int(float(Data.Parametros.dict['distribución_almuerzo'].split(';')[1])*0.01*total)
        cant_per_z = total - cant_per_x - cant_per_y
        c1 = 0 ; c2 = 0 ; c3 = 0
        for i in miembros_uc:
            if c3 < cant_per_z and i.hora_llegada_diaria.hour <= 12:
                #Agregar tiempo decidir ir a comer + la caminara
                deci_viaje = self.tiempo_ir_comer(i, timedelta(hours = 12))   #Tiempo en el que decide ir a comer y en el cual camina
                i.hora_almuerzo =  i.hora_llegada_diaria + deci_viaje
                c3 += 1
            elif c1 < cant_per_x and i.hora_llegada_diaria.hour <= 13:
                #Agregar tiempo decidir ir a comer + la caminara
                deci_viaje = self.tiempo_ir_comer(i, timedelta(hours = 13))   #Tiempo en el que decide ir a comer y en el cual camina
                i.hora_almuerzo = i.hora_llegada_diaria + deci_viaje
                c1 += 1
            elif c2 < cant_per_y and i.hora_llegada_diaria.hour <= 14:
                #Agregar tiempo decidir ir a comer + la caminara
                deci_viaje = self.tiempo_ir_comer(i, timedelta(hours = 13))   #Tiempo en el que decide ir a comer y en el cual camina
                i.hora_almuerzo = i.hora_llegada_diaria + deci_viaje
                c2 += 1

    def almorzar(self, persona, simu, eventos):
        concha = 0
        #No pude alterar el tiempo de atención de todas las personas una vez que ingresaba un funcionario
        if len(eventos) != 0:
            strings = [i[1] for i in eventos]
            if 'lluvia_hamburguesas' in strings:
                print('No almuerza nadie')
                '''Para los vendedores es como si nadie estuviera en el campus'''
                persona.in_campus == False
                EProgra.total_no_almorzaron += len(miembros_uc)

            if 'concha' in strings:
                concha = 1

        if persona.in_campus:
            '''Esta función se activa cuando una persona está en el local de almuerzo y se pone a la fila
            al ingresar a la fila se agrega el tiempo en el cual la persona va a almorzar a la lista de tiempos discretos de la simulación y 
            se luego el proceso de terminar de almorzar lo hace la función 'atendieron'  '''
            a = False
            pos = 0
            #Elegimos los vendedores preferido que venden solamente almuerzos
            vende_almuerzos = [i for i in persona.vendedores_prefe
                               if retornar_vendedor(i).tipo_comida != 'Snack'
                               and retornar_vendedor(i).stock > 0
                               and retornar_vendedor(i).instalado == True]


            while a == False and pos < len(vende_almuerzos):
                if persona.entidad == 'Funcionario':
                    eleccion = vende_almuerzos[pos]
                    vendedor = retornar_vendedor(eleccion)  #Me retorna el objeto de vendedor con ese nombre
                    if vendedor.instalado == True and vendedor != persona.ultimo_almuerzo and vendedor.stock > len(vendedor.cola):
                        a = True
                        print('La persona {} llegó a la fila de {} a exactamente las {}'.format(persona.nombre + ' ' + persona.apellido, eleccion, persona.hora_almuerzo))
                        vendedor.cola.appendleft(persona)
                        vendedor.venta += 1
                        alcanza_para = [i for i in vendedor.dict_productos
                                        if int(persona.presu_diario) > int(retornar_producto(i).precio)
                                                                    + 0.25*int(retornar_producto(i).precio) * concha]
                        #Si hay concha acústica te alcanza oara menos productos
                        comida = choice(alcanza_para)
                        '''Suma a la lista de tiempos de la simulación el tiempo en el cual lo van a atender'''
                        '''Aqui el funcionario que llega último se pone primero, idependiente de que si hay otro funcionario adelante de él'''
                        tiempo_atencion = (persona.hora_almuerzo + timedelta(minutes = vendedor.velocidad))
                        if vendedor.nombre == 'Quik':
                            tiempo_atencion = persona.hora_almuerzo
                        persona.hora_entrega = tiempo_atencion
                        persona.comida_diaria = comida
                        persona.le_compra = vendedor
                        persona.ultimo_almuerzo = vendedor

                elif persona.entidad == 'Alumno':
                    eleccion = vende_almuerzos[pos]
                    vendedor = retornar_vendedor(eleccion)
                    paciencia = persona.paciencia
                    alcanza_para = [i for i in vendedor.dict_productos
                                    if int(persona.mesada_diaria) > int(retornar_producto(i).precio) +
                                                                    0.25*int(retornar_producto(i).precio) * concha]
                    #Si hay concha alcanza para menos productos
                    if len(alcanza_para) == 0:
                        print('No tienes suficiente mesada diaria para comprar en ese local, eligiendo el próximo')
                    if vendedor.instalado == True and len(alcanza_para) != 0 and vendedor.stock > len(vendedor.cola):
                        vendedor.venta += 1
                        vendedor.cola.append(persona)
                        print('La persona {} llegó a la fila de {} a exactamente las {}'.format(
                            persona.nombre + ' ' + persona.apellido, eleccion, persona.hora_almuerzo))
                        comida = choice(alcanza_para)
                        tiempo_atencion = (persona.hora_almuerzo + timedelta(minutes = (vendedor.velocidad * len(vendedor.cola)) ))

                        if vendedor.nombre == 'Quik':
                            tiempo_atencion = persona.hora_almuerzo

                        if tiempo_atencion - persona.hora_almuerzo < timedelta(minutes = paciencia):
                            print(tiempo_atencion, 'a la hora que lo van a atender')
                            persona.hora_entrega = tiempo_atencion
                            persona.comida_diaria = comida
                            persona.le_compra = vendedor
                            print('planea que lo atiendan a las {}'.format(tiempo_atencion))
                            a = True
                        else:
                            persona.paciencia -= 5
                            if paciencia <= 0 or pos >= 3:
                                print('Chao perro mató me voy al quik devil')
                                vendedor = retornar_vendedor('Quik Devil')
                                tiempo_atencion = persona.hora_almuerzo
                                persona.hora_entrega = tiempo_atencion
                                persona.comida_diaria = comida
                                persona.le_compra = vendedor
                                print('planea que lo atiendan a las {}'.format(tiempo_atencion))
                                a = True
                                EProgra.cambio_fila += 1
                    else:
                        print('La persona se quedó sin almorzar')
                        print(persona.vendedores_prefe)
                        #Para fines prácticos se pone que almorzó, sino el problema arroja error
                        a = True
                        EProgra.total_no_almorzaron += 1
                pos += 1


        persona.almuerzo = True

    def atendieron(self, simu, persona, eventos):
        #Saca al cliente de la cola
        #Baja el Stock
        #Clientes se pueden enfermar
        #Clientes gastan plata
        entidad = persona.entidad
        vendedor = persona.le_compra
        vendedor.entrega += 1
        enferma = random()
        frio = 0 ; calor = 0 ; lluvia_h = 0 ; lluvia_h2 = 0 ; policias = 0; concha = 1
        strings = [i[1] for i in eventos]
        if 'frio' in strings:
            frio = 1
        if 'calor' in strings:
            calor = 1
        if 'lluvia_hamburguesas' in strings:
            lluvia_h = 1
        if 'lluvia_hamburguesas2' in strings:
            lluvia_h2 = 1

            '''No se de que me sirve esto todavía'''
        if 'concha' in strings:
            concha = 1

        if vendedor.stock == 0:
            vendedor.instalado = False
            ps = simu.puestos.index(vendedor)
            simu.puestos.pop(ps)        #Sacamos a los vendedores que ya no tienen stock y por lo tanto se van a sus casa
            vendedor.contador_no_stock += 1
            '''Hay que resetearlo todos los meses!!!'''


        if entidad == 'Alumno' and vendedor.stock != 0:
            print(vendedor.nombre + ': le entregué el almuerzo a ' + persona.nombre + ' ' + persona.apellido)
            persona.almuerzo_entregado = True
            comida = persona.comida_diaria          #Es un string
            comida = retornar_producto(comida)
            calidad = calidad_producto(comida, persona.hora_entrega, calor) \
                      - calidad_producto(comida, persona.hora_entrega, calor)/2 * frio     #si frio es 1 baja a la mitad
            persona.mesada_diaria -= int(comida.precio) + 0.25*int(comida.precio) * concha #Si hay concha los precios suben un 25%
            #Se ajusta el presupuesto diario de la persona

            if calidad < 0.2 and enferma < (0.35 + 0.35*lluvia_h2) and vendedor.nombre != 'Quik':
                #Gente se enferma con el doble de probabilidad si el día anterior fue lluvia de hamburguesas
                #Persona se enferma
                vendedor1 = vendedor.nombre + ' ' + vendedor.apellido
                pos = persona.vendedores_prefe.index(vendedor1)
                vendedor.intoxicados_mi_culpa += 1
                persona.vendedores_prefe.pop(pos) #Sacamos al vendedor de la lista de vendedores preferidos

            if vendedor.nombre != 'Quik':
                vendedor.cola.popleft()

        elif entidad == 'Funcionario' and vendedor.stock != 0:                        #Le vendemos el producto de mejor calidad
            print(vendedor.nombre + ': le entregué el almuerzo a ' + persona.nombre + ' ' + persona.apellido)
            persona.almuerzo_entregado = True
            max = ('string', 0)
            for i in vendedor.dict_productos:
                prod = retornar_producto(i)
                cal = calidad_producto(prod, persona.hora_entrega, calor) \
                      - calidad_producto(prod, persona.hora_entrega, calor)/2 * frio     #Si frio es 1 baja a la mitad
                if cal > max[1]:
                    max = (prod, cal)
            comida = max[0]
            calidad = max[1]
            persona.presu_diario -= int(comida.precio) + 0.25*int(comida.precio) * concha #Si hay concha suben los precios un 25%
            #Se ajusta el presupuesto diario de la persona


            if calidad < 0.2 and enferma < (0.35 + 0.35*lluvia_h2) and vendedor.nombre != 'Quik':
                #Gente se enferma con el doble de probabilidad si el día anterior fue lluvia de hamburguesas
                #Persona se enferma
                vendedor1 = vendedor.nombre + ' ' + vendedor.apellido
                vendedor.intoxicados_mi_culpa += 1
                pos = persona.vendedores_prefe.index(vendedor1)
                persona.vendedores_prefe.pop(pos) #Sacamos al vendedor de la lista de vendedores preferidos

            if vendedor.nombre != 'Quik':
                vendedor.cola.popleft()

        vendedor.dict_productos = {x: vendedor.dict_productos[x] - 1 for x in vendedor.dict_productos}
        vendedor.stock -= 1


    def tiempo_ir_comer(self, persona, hora):
        #tiempo traslado
        hora_llegada = persona.hora_llegada_diaria
        tasa = float(Data.Parametros.dict['traslado_campus'])
        a = True
        while a:
            caminata = expovariate(tasa)
            if caminata < tasa*3:
                a = False
        #tiempo caminata
        a = True
        while a:
            num = numpy.random.normal(10, 10)
            if num < 120 and num > -60 and (num + caminata > 0):
                a = False

        return timedelta(minutes = num) + timedelta(hours = caminata)

    #solo alumnos
    def tiempo_instalar_puestos(self, simu):
        for i in vendedores:
            num = numpy.random.normal(660, 30)
            dia = dia_nuevo(simu.dia_actual)
            i.hora_puesto = dia + timedelta(minutes=num)
    #solo Vendedores
    def instalar_puesto(self, simu, vendedor):
        if not vendedor.asustado or vendedor.dias_asustado == vendedor.dias_susto:
            vendedor.asustado = False
            simu.puestos.append(vendedor)
            vendedor.instalado = True
            print('el vendedor {} instala su puesto a las {}'.format(vendedor.nombre, simu.dia_actual))

            lista1 = Data.Parametros.dict['stock_vendedores'].split(';')        #Definimos el stock del día siguiente
            vendedor.stock = randint(int(lista1[0]), int(lista1[1]))
            vendedor.stock_inicial = vendedor.stock

            '''Le damos su stock de productos como un diccionario, tomaremos el stock como un total
            Si el stock dado en el modulo Data es 120, cada producto tiene 120 de disponibilidad
            Si compran uno, bajan todos los numeros por el supuesto del enunciado '''
            if vendedor.tipo_comida == 'China':
                for i in prod_chinos:
                    prod = {i.producto: vendedor.stock}
                    vendedor.dict_productos.update(prod)
            elif vendedor.tipo_comida == 'Snack':
                for i in prod_snacks:
                    prod = {i.producto: vendedor.stock}
                    vendedor.dict_productos.update(prod)
            elif vendedor.tipo_comida == 'Mexicana':
                for i in prod_mexicanos:
                    prod = {i.producto: vendedor.stock}
                    vendedor.dict_productos.update(prod)

        else:
            vendedor.dias_asustado += 1

    def tiempo_snack(self, simu):
        for i in miembros_uc:
            if i.snack:
                hora = randint(i.hora_llegada_diaria.hour, 15)   #Por la aclaración del issue #543, los snacks distribuyen uniforme
                if i.hora_almuerzo != hora:
                    #No permite que se compre snack al mismo tiempo que se compra almuerzo
                    i.hora_snack = dia_nuevo(simu.dia_actual) + timedelta(hours = hora)


    def snack(self, simu):
        pass


    def recalcular_mesada(self):
        for i in alumnos:
            if i.entidad == 'Alumno':
                i.mesada = int(Data.Parametros.dict['base_mesada'])*(1 + (random())**random())*20
                i.mesada_diaria = round(i.mesada/20)
                i.mesada_diaria_mes = i.mesada_diaria

