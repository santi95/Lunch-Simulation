# Explicación Tarea

## Santiago Muñoz Venezian; santi95

25 de Octubre, 2017

Para que sea más facil de corregir, lo que no me funcionó fue:

    1. Al agregarse funcionarios a la cola simplemete se ponen primeros, ignoran que hayan más funcionarios.
    2. pep8 está horrible, perdón por eso, ando cortísimo de tiempo.
    3. En vez de que cuando el stock se agote los estudiantes se vayan,
    no les permite entrar a la cola a menos de que haya suficiente stock para todos.
    4. Desplgegamiento de las Estadísticas hecho muy muy mal, la información está, pero tema tiempo me mató
    5. Escenarios, tenía que cambiar los prints y cambiar de adonde estaba el programa leyendo los parametros y quedaban corriendo
    6. No alcancé a hacer lo de los snacks


Todo el resto funciona super bien en general

Mi tarea tiene 5 modulos.

    1. Data
    2. Eventos
    3. T04
    4. Variables
    5. Escenarios

Se procesan en este orden: Data < Eventos < T04 < Escenarios (Escenarios corre mal)

#### 1. Data

Tiene una clase Persona que lee y guarda los atributos de todas las personas independientres de su entidad,
más adelante en el programa se hace una separación de ellos con listas.

Es solamente una clase, con muchos atributos, pero solo usan algunos de ellos. Sin embargo todos esos atributos son
usados por el programa y no podrían ser menos segíun mi simulación. Muchos de ellos ayudan a generar las estadísticas finales.

Como atributos de clases podemos ver:

lista: contiene todas las personas sin excepción, incluyendo a QuikDevil
confisca_jekyll: suma cada vez que un carabinero de personalidad Jekyll confisca productos
confisca_hide: lo mismo que antes, pero para Hide
contador_no_stock_diario: nombre eterno, pero explica que suma 1 cada vez que un vendedor se queda sin stock
lista_contador_no_stock: Para poder calcular los promedios diarios de las veces que los vendedores se quedan sin stock

Tiene una clase Parametros que crea un diccionario con todas las características iniciales
con sus respectivos datos de la simulación, solo tenía que cambiar esto para crear los parametros :(

Tiene una clase Productos, que les pone atributos y tiene un property para que el precio no baje más allá de 0
Tiene también un atributo de clase que es una lista que guarda todos los objetos


Luego vienen los lectores de datos, primero tenemos el lector de productos, que
toma las posiciones de cada uno y crea los objetos necesarios.

parametros_iniciales es el que tenía que cambiar para generar los escenarios, ese nombre,
que está en la variable archivo.

Finalmente el más largo, el lector y creador de personas.
Les dá atributos dependiendo de que entidad tienen y al final crea la 'persona' quikDevil
por terminos prácticos de la simulación.

#### 2. Eventos

1, Importa todo lo necesario

2, crea 4 funciones que se van a usar a lo largo de toda la modelación


    a. dia_nuevo, para crear los eventos nos programados con facilidad

    b. retornar_vendedor, retorna el objeto del vendedor buscando su nombre

    c. retornar_producto, hace lo mismo con los productos, a partir del nombre
    te entrega el objeto

    d. calidad_producto, retorna la calidad del producto considerando si hace calor o no
    durante el día

3, Separa los objetos en distintas listas, estan los miembros_uc, carabineros
alumnos, funcionarios, vendedores, y distintos tipos de productos

Hay 2 clases de eventos:

    1. ENoProgra, Eventos no Programados: generan las distintas fechas de los eventos

    Cada vez que una de estas funciones es llamada, crea otro evento igual

        a. generar_ultimo_dia_mes: Era necesaria pq en este día pasaban muchas cosas explciadas
        luego en el T04

        b. genera las temperaturas extremas, las 2 uniformemente.

        c. Genera la lluvia de hamburguesas, redondea la fecha, crea en la simulación
        un atributo lluvia hamburguesa con su fecha y lo agrega al tiempo.

        d. generar_concha_acustica: nos dice el día en el cual va a haber una concha acustica

        e. generar_llamado_policia: nos dice cuando llegarán los policias, información
        por la cual los vendedores pagarían mucha plata.

        f. revision_policia: no retorna al atendido a la fila, sino que lo atiende rápido, todo
        el resto se atrasa el tiempo, con la posibilidad de cambiarse de fila.
        además confisca productos y hace todo lo pedido.


    2. EProgra, Eventos programados: generan eventos casi todos los días

        a. definir_paciencia: define la paciencia de cola de un alumno

        b. entrega todos los tiempos de todos los alumnos en llegar al campus

        c. llegar_campus: lo que pasa cuando el alumno llega al campus,
        el objeto.in_campus se hace verdadero y se escribe en la consola

        d. tiempo_almorar: define quien almuerza a que hora diariamente

        e. almorzar, hace todo lo que pasa desde el momento en que
        es la hora de almorzar de la persona hasta que lo atiende el vendedor.
        elige fila, ve la condicion de la lluvia de hamburguesas y de la concha
        acustica. Decide por un vendedor y se cumplen los parametros dependiendo
        del tipo de entidad de la persona

        f. atendieron, verifica stock del vendedor, sino alumno se cambia de fila,
        ve si se enferma la gente o no, dependiendo de que si es día siguiente
        de la lluvia de hamburguesas y hace lo mismo para los funcionarios

        g. tiempo_ir_comer, me dice cuanto tiempo el miembro_uc se demora en
        decidir ir a comer + caminar hasta el puesto, esta función es llamada desde
        tiempo_almorzar

        h. tiempo_instalar_puesto: crea para todos los vendedores la hora de armado
        de su puesto en la mañana

        i. lo que pasa cuando se instala el puesto, se setea stock diario,
        y puede empezar a vender, aquí se aplica la condición de vendedor asustado

        j y k los snacks no los alcancé a hacer

        l. recalcula la mesada todos los fines de mes


#### T04

La simulación en si.

En los parametros de la clase
 tiene contadores de eventos no programados, para las Estadísticas.

 En el __init__ se definen los tiempos de eventos no programados a usar en la simulación
 Además hay 2 listas, una de bancarrota y otra de los puestos instalados

 Función Central, run().

 Tiene varios pasos

    1. crea 2 objetos de las clases eventos, para poder manejarlos con facilidad

    2. genera los tiempos No Programados de la simulación

    3. los agrega a la lista_tiempos del día en forma de tupla, el segundo argumento
    dice que hay en el tiempo del primer elemento de la tupla

    4. Se crea el mismo tipo de tupla para las horas de llegada, horas de almuerzo,
    hora de instalado de los puestos y las horas de entrega que sin generadas por las horas
    de almuerzo

    5. hacemos un sort de la lista y sacamos el primer elemento para ver cual es el evento más próximo

    6. parte la simulación con un while, las fechas usadas son datetimes y el periodo de
    simulación es entre Marzo 1 y Julio 1, 4 meses.

    7. Las tuplas nos dicen que tiempo significa que evento y se lleva a cabo con su función respectiva

    8. en el día_ultimo_mes, se recalcula la mesada, se cuenta la cantidad de veces que un vendedor estuvo sin stock
    o en cuantos días no vendió nada. Se recalculan los precios con respecto a eso.

    9. Se crean las conchas acústicas, policias, lluvia_hamburguesas y la hora llegada
    de los policias a la feria.

    10. Se notifica cada vez que un alumno llega a la universidad

    11. almuerzo, la lista tweak, retorna los
    Eventos No Programados que se están dando
    en el transcurso de ese día

    12. else final, me indicaba cuando tenía algun error en la programación. en los eventos
    programados.

    13. Se vuelven a crear los elementos no programados y se revisa cuantos alumnos
    faltan por llegar, almorzar, puestos por instalar o entrega de comida. Cada vez que se
    corre un ciclo del while es, porque se leyó un evento de la lista de eventos.

    14. Si no falta nadie por almorzar, no poner su puesto, ni por entregar su comida
    ni por llegar, se notifica un cambio de día.

    15. revisión si es fin de semana al día siguiente o no. En el segundo if

    16. Como cambio el día se vuelve a generar el último_dia_mes, se resetean las mesadas
    y los presupuestos diarios de los alumnos y funcionarios.

    17. Se cuenta si el vendedor vendió algo durante los últimos 20 días habiles, sino
    quiebra.

    18. la simulación avanza un día, la verdad esto es innecesario, me acabo de dar cuenta

    19. se resetean los valores de llegada/almuerzo/seteo_puestos de todas las perosnas

    20. se avanza un día para que la simuñación se mueva a un evento llamado,
    fin de semana.

    21. Perdón por las estadísticas, me dan verguenza, pero los datos están!!


#### 4. Escenarios

    Iba a hacer un metodo de overwriting para la función parametros cuando quisiera
    leer todos los escenarios, empecé por leer los datos de los escenarios
    y luego no alcancé.

#### 5. Variables

    No tiene nada util, lo cree al inciio de la tarea y nunca lo edité ni borré, sorry denuevo


Entretenida la tarea, eso si, perdía el sentido ya que las tasas de calidad
por la formula entregada eran bajisimas, por lo tanto todos se enfermaban casi
siempre y todos los miembros uc terminaban comprando en QuikDevil


Gracias por corregirme la tarea! Ojalá este readme haya ayudado. Funciona casi todo,
fue un tema de tiempo que no pude hacerlo todo.

Saludos y gracias denuevo.
