#!/usr/bin/python3

'''
Proyecto Python - IE-0117
Alvaro Alfaro Miranda B70224
Heiner Mauricio Obando Vega B55130
Miguel Roberto Jimenez Tung B94104

Este programa consiste un juego cuya base es un "Endless Runner", en este caso
el personaje deberá evitar los obstáculos que aparecerán en el camino de
manera aleatoria y el juego no terminará hasta que el personaje no choque con
algún obstáculo, habrá un conteo del puntaje que logré el jugador, pero solo
se guardará para ver luego el puntaje más alto que se logre alcanzar. El
personaje se moverá con las flechas del teclado.
El programa tiene un menú el cual permite acceder a jugar, al tutorial o a
observar el puntaje más alto.
'''

# Librerias a utilizar en el código
import pygame
import random
import gi
import sys

# Se importan la biblioteca Gtk
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk  # noqa

constructor = Gtk.Builder()  # Se crean el objeto constructor
glade_file = 'Proyecto.glade'  # Se carga el archivo de glade
constructor.add_from_file(glade_file)  # Añade todos los widgets del archivo

# Obtenemos widgets por ID
ventana = constructor.get_object('main_window')
boton_jugar = constructor.get_object('button_1')
boton_tutorial = constructor.get_object('button_2')
boton_puntaje = constructor.get_object('button_3')
boton_salir = constructor.get_object('button_4')

# Crea una asociación entre la señal "destroy" y la función Gtk.main_quit
ventana.connect('destroy', Gtk.main_quit)


def main(button):
    """
    Esta función se encarga de controlar el juego, movimiento del jugador,
    condiciones, puntajes, imagenes  y sonidos.
    """

    pygame.init()  # Inicializa todos los módulos importados de pygame

    # Constantes del juego
    BLANCO = (255, 255, 255)
    AMARILLO = (255, 255, 0)
    ANCHO = 450  # Ancho para la ventana del juego
    ALTO = 300  # Alto para la ventana del juego
    GRAVEDAD = 1  # Gravedad que influye en el personaje
    FPS = 60
    VEL_OBSTACULOS = 2  # Velocidad a la que se mueven los obstáculos

    # Variables del juego
    puntaje = 0
    posicion_x = 50  # Posición del jugador en el eje x
    posicion_y = 200  # Posición del jugador en el eje y
    cambio_y = 0  # Cambio en la posición del jugador en el eje x
    cambio_x = 0  # Cambio en la posición del jugador en el eje y
    obstaculos = [300, 450, 600]  # Posición inicial de los obstaculos
    activo = False  # El juego está activo
    jugando = True  # Se ejecuta el código del juego
    mov_izquierda = False  # Indica si el personaje se mueve hacía la izquierda
    mov_derecha = False  # Indica si el personaje se mueve hacía la derecha
    saltando = False  # Indica si el personaje está saltando
    pasos_cont = 0  # Conteo de pasos para el cambio de movimientos del jugador

    # Se cargan imagenes desde archivos
    fondo = pygame.image.load("fondoPokemon.png")
    derecha = [pygame.image.load('Paso_1.png'),
               pygame.image.load('Paso_2.png')]
    izquierda = [pygame.image.load('Paso_i_1.png'),
                 pygame.image.load('Paso_i_2.png')]
    arbol = pygame.image.load('arbolpokemon.png')
    psyduck = pygame.image.load('psyduck.png')
    snorlax = pygame.image.load('Snorlax.png')
    personaje = pygame.image.load('Quieto.png')
    salto = pygame.image.load('Salto.png')

    # Se crean los objetos de sonido a partir de archivos
    sonido_fondo = pygame.mixer.Sound('pokemonVB.wav')
    sonido_salto = pygame.mixer.Sound('salto.wav')
    sonido_snorlax = pygame.mixer.Sound('Snorlax_Sonido.wav')
    sonido_psyduck = pygame.mixer.Sound('Psyduck_Sonido.wav')
    sonido_arbol = pygame.mixer.Sound('Arbol_Sonido.wav')

    # Configuración del modo de visualización
    pantalla = pygame.display.set_mode([ANCHO, ALTO])
    pygame.display.set_caption('Pokémon Runner')  # Nombre de la ventana
    fuente = pygame.font.Font('freesansbold.ttf', 16)  # Fuente de letra
    temp = pygame.time.Clock()  # Objeto para controlar el tiempo

    def puntuacion_mayor():
        """
        Permite leer el valor del puntaje más alto obtenido del
        archivo donde fue guardado
        """
        with open("highestscorePRUEBA.txt", "r") as f:
            return f.read()

    # Si el archivo no existe o dentro del archivo no existe un valor
    # para la puntuación máxima o posee un valor erroneo
    # se atrapa el error y se declara el valor como cero
    try:
        puntaje_mayor = int(puntuacion_mayor())
    except Exception:
        puntaje_mayor = 0

    while jugando:
        temp.tick(FPS)  # Controla los fotogramas por segundo
        pantalla.blit(fondo, (0, 0))  # Coloca una superficie desde una fuente

        # Se crean los objetos de texto
        tex_puntaje = fuente.render(f'Puntaje: {puntaje}', True,
                                    BLANCO)
        tex_mayor_puntaje = fuente.render(f'Puntaje más alto: {puntaje_mayor}',
                                          True, BLANCO)
        boton_salida = fuente.render('T: Para volver al menú', True,
                                     BLANCO)

        # Se colocan en pantalla los objetos de texto creados
        pantalla.blit(tex_puntaje, (290, 10))
        pantalla.blit(tex_mayor_puntaje, (290, 40))
        pantalla.blit(boton_salida, (10, 270))

        # Archivos de texto mostrados cuando no se a iniciado el juego
        if not activo:
            boton_inicio = fuente.render('Espacio para iniciar',
                                         True, AMARILLO)
            boton_salto = fuente.render('Arriba para saltar',
                                        True, AMARILLO)
            boton_movimiento = fuente.render('Izquierda y Derecha '
                                             'para moverse', True, AMARILLO)

            # Se colocan en pantalla los objetos de texto creados
            pantalla.blit(boton_inicio, (150, 125))
            pantalla.blit(boton_salto, (25, 65))
            pantalla.blit(boton_movimiento, (25, 85))

        # Se crean los obstaculos y se indica su posición inicial
        obstaculo_0 = pantalla.blit(arbol, (obstaculos[0], 205))
        obstaculo_1 = pantalla.blit(psyduck, (obstaculos[1], 205))
        obstaculo_2 = pantalla.blit(snorlax, (obstaculos[2], 205))

        # Condiciones para observar un cambio de movimientos en el jugador
        if pasos_cont + 1 >= 4:
            pasos_cont = 0

        # Se cambia el movimiento del jugador de acuerdo
        # a los condiciones cumplidas
        if mov_izquierda:
            jugador = pantalla.blit(izquierda[pasos_cont//2], (posicion_x,
                                                               posicion_y))
            pasos_cont += 1
        elif mov_derecha:
            jugador = pantalla.blit(derecha[pasos_cont//2], (posicion_x,
                                                             posicion_y))
            pasos_cont += 1
        elif saltando:
            jugador = pantalla.blit(salto, (posicion_x, posicion_y))
            pasos_cont += 1
        else:
            jugador = pantalla.blit(personaje, (posicion_x, posicion_y))
            pasos_cont = 0

        # Se crea el manejo del personaje a partir de entradas en el teclado
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Permite cerrar el juego
                jugando = False

            # Usos y condiciones de teclado cuando el juego no está activo
            if event.type == pygame.KEYDOWN and not activo:  # Tecla presionada
                if event.key == pygame.K_SPACE:  # Iniciar juego
                    activo = True
                    mov_izquierda = False
                    mov_derecha = False
                    saltando = False
                    # Se paran posibles sonidos de los obtaculos al perder
                    # y reiniciar
                    pygame.mixer.Sound.stop(sonido_arbol)
                    pygame.mixer.Sound.stop(sonido_psyduck)
                    pygame.mixer.Sound.stop(sonido_snorlax)
                    # Se inicia sonido principal, -1 indica un búcle del sonido
                    pygame.mixer.Sound.play(sonido_fondo, -1)
                    obstaculos = [300, 450, 600]
                    posicion_x = 50
                    puntaje = 0
                if event.key == pygame.K_t:  # Cerrar ventana
                    jugando = False

            # Usos y condiciones de teclado cuando el juego está activo
            if event.type == pygame.KEYDOWN and activo:   # Tecla presionada
                if event.key == pygame.K_UP and cambio_y == 0:  # Tecla salto
                    mov_izquierda = False
                    saltando = True
                    mov_derecha = False
                    # Se activa sonido de salto
                    pygame.mixer.Sound.play(sonido_salto)
                    cambio_y = 19
                if event.key == pygame.K_RIGHT:  # Tecla movimiento derecha
                    mov_izquierda = False
                    saltando = False
                    mov_derecha = True
                    cambio_x = 2
                if event.key == pygame.K_LEFT:  # Tecla movimiento izquierda
                    mov_izquierda = True
                    saltando = False
                    mov_derecha = False
                    cambio_x = -2
                if event.key == pygame.K_t:  # Cerrar ventana
                    jugando = False

            # Usos y condiciones de teclas cuando no están precionadas
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:  # Tecla movimiento derecha
                    mov_izquierda = False
                    mov_derecha = False
                    cambio_x = 0
                if event.key == pygame.K_LEFT:  # Tecla movimiento izquierda
                    mov_izquierda = False
                    mov_derecha = False
                    cambio_x = 0

        # Condiciones para el correcto movimiento del personaje
        # dentro de la ventana
        if 0 <= posicion_x <= 420:  # Permite movimiento en el eje x
            posicion_x += cambio_x
        if posicion_x < 0:  # Impide superar limite izquierdo en el eje x
            posicion_x = 0
        if posicion_x > 420:  # Impide superar limite derecho en el eje x
            posicion_x = 420

        # Permite que el personaje caiga al saltar
        if cambio_y > 0 or posicion_y < 200:
            posicion_y -= cambio_y
            cambio_y -= GRAVEDAD
        # Impide que el personaje caiga más abajo del suelo
        if posicion_y > 200 and activo:
            posicion_y = 200
        # Se verifica de nuevo que el personaje no caiga más abajo del suelo
        if posicion_y == 200 and cambio_y < 0:
            saltando = False
            cambio_y = 0

        # Permite el movimiento de los personajes, sus ubicaciones aleatorias
        # y realiza el conteo del puntaje
        for i in range(len(obstaculos)):
            if activo:
                obstaculos[i] -= VEL_OBSTACULOS
                # Posición del obstaculo donde se obtiene un punto
                if obstaculos[i] < -20:
                    obstaculos[i] = random.randint(470, 700)
                    puntaje += 1

                # Condiciones si suceden colisiones con los obstaculos
                # Se activa sonido correspondiente al obstáculo
                # Se detiene sonido principal
                # Personaje sale de pantalla para evitar errores
                # Se detiene el juego
                if jugador.colliderect(obstaculo_0):
                    pygame.mixer.Sound.play(sonido_arbol)
                    pygame.mixer.Sound.stop(sonido_fondo)
                    posicion_y = 600
                    activo = False
                if jugador.colliderect(obstaculo_1):
                    pygame.mixer.Sound.play(sonido_psyduck)
                    pygame.mixer.Sound.stop(sonido_fondo)
                    posicion_y = 600
                    activo = False
                if jugador.colliderect(obstaculo_2):
                    pygame.mixer.Sound.play(sonido_snorlax)
                    pygame.mixer.Sound.stop(sonido_fondo)
                    posicion_y = 600
                    activo = False

        # Se revisa el puntaje obtenido, si supera el puntaje mayor
        # anterior lo sobreescribe
        if(puntaje_mayor < puntaje):
            puntaje_mayor = puntaje
        with open("highestscorePRUEBA.txt", "w") as f:
            f.write(str(puntaje_mayor))

        pygame.display.flip()  # Actualiza la pantalla completa de pygames

    pygame.quit()


def tutorial(button):
    """
    Esta función muestra el movimiento del jugador junto con las instrucciones.
    Cabe destacar que este código contiene secciones previamente
    comentadas, por lo que en este caso no se explicarán a fondo.
    Esta función no incluye todo el código de los obstáculos.
    """
    pygame.init()

    # Constantes del juego
    BLANCO = (255, 255, 255)
    AMARILLO = (255, 255, 0)
    ANCHO = 450
    ALTO = 300
    GRAVEDAD = 1
    FPS = 60

    # Variables del juego
    posicion_x = 50
    posicion_y = 200
    cambio_y = 0
    cambio_x = 0
    activo = False
    jugando = True
    mov_izquierda = False
    mov_derecha = False
    saltando = False
    pasos_cont = 0

    # Se cargan imagenes desde archivos
    fondo = pygame.image.load("fondoPokemon.png")
    derecha = [pygame.image.load('Paso_1.png'),
               pygame.image.load('Paso_2.png')]
    izquierda = [pygame.image.load('Paso_i_1.png'),
                 pygame.image.load('Paso_i_2.png')]
    personaje = pygame.image.load('Quieto.png')
    salto = pygame.image.load('Salto.png')

    # Se crean los objetos de sonido a partir de archivos
    sonido_fondo = pygame.mixer.Sound("pokemonVB.wav")
    sonido_salto = pygame.mixer.Sound("salto.wav")

    # Configuración del modo de visualización
    pantalla = pygame.display.set_mode([ANCHO, ALTO])
    pygame.display.set_caption('Pokémon Runner')
    fuente = pygame.font.Font('freesansbold.ttf', 16)
    temp = pygame.time.Clock()

    while jugando:
        temp.tick(FPS)
        pantalla.blit(fondo, (0, 0))

        # Se crean los objetos de texto
        boton_salto = fuente.render('Arriba para saltar',
                                    True, AMARILLO)
        boton_movimiento = fuente.render('Izquierda y Derecha '
                                         'para moverse', True, AMARILLO)
        boton_salida = fuente.render('T: Para volver al menú', True,
                                     BLANCO)

        # Se colocan en pantalla los objetos de texto creados
        pantalla.blit(boton_salto, (25, 65))
        pantalla.blit(boton_movimiento, (25, 85))
        pantalla.blit(boton_salida, (10, 270))

        # Archivos de texto mostrados cuando no se a iniciado el juego
        if not activo:
            boton_inicio = fuente.render('Espacio para iniciar',
                                         True, AMARILLO)
            pantalla.blit(boton_inicio, (150, 125))

        # Condiciones para observar un cambio de movimientos en el jugador
        if pasos_cont + 1 >= 4:
            pasos_cont = 0

        # Se cambia el movimiento del jugador de acuerdo
        # a los condiciones cumplidas
        if mov_izquierda:
            pantalla.blit(izquierda[pasos_cont//2], (posicion_x,
                                                     posicion_y))
            pasos_cont += 1
        elif mov_derecha:
            pantalla.blit(derecha[pasos_cont//2], (posicion_x,
                                                   posicion_y))
            pasos_cont += 1
        elif saltando:
            pantalla.blit(salto, (posicion_x, posicion_y))
            pasos_cont += 1
        else:
            pantalla.blit(personaje, (posicion_x, posicion_y))
            pasos_cont = 0

        # Se crea el manejo del personaje a partir de entradas en el teclado
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                jugando = False

            # Usos y condiciones de teclado cuando el juego no está activo
            if event.type == pygame.KEYDOWN and not activo:
                if event.key == pygame.K_SPACE:
                    mov_izquierda = False
                    mov_derecha = False
                    saltando = False
                    pygame.mixer.Sound.play(sonido_fondo, -1)
                    posicion_x = 50
                    activo = True
                if event.key == pygame.K_t:
                    jugando = False

            # Usos y condiciones de teclado cuando el juego está activo
            if event.type == pygame.KEYDOWN and activo:
                if event.key == pygame.K_UP and cambio_y == 0:
                    pygame.mixer.Sound.play(sonido_salto)
                    mov_izquierda = False
                    saltando = True
                    mov_derecha = False
                    cambio_y = 19
                if event.key == pygame.K_RIGHT:
                    mov_izquierda = False
                    saltando = False
                    mov_derecha = True
                    cambio_x = 2
                if event.key == pygame.K_LEFT:
                    mov_izquierda = True
                    saltando = False
                    mov_derecha = False
                    cambio_x = -2
                if event.key == pygame.K_t:
                    jugando = False

            # Usos y condiciones de teclas cuando no están precionadas
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    mov_izquierda = False
                    mov_derecha = False
                    cambio_x = 0
                if event.key == pygame.K_LEFT:
                    mov_izquierda = False
                    mov_derecha = False
                    cambio_x = 0

        # Condiciones para el correcto movimiento del personaje
        # dentro de la ventana
        if 0 <= posicion_x <= 420:
            posicion_x += cambio_x
        if posicion_x < 0:
            posicion_x = 0
        if posicion_x > 420:
            posicion_x = 420

        if cambio_y > 0 or posicion_y < 200:
            posicion_y -= cambio_y
            cambio_y -= GRAVEDAD
        if posicion_y > 200 and activo:
            posicion_y = 200
        if posicion_y == 200 and cambio_y < 0:
            saltando = False
            cambio_y = 0

        pygame.display.flip()

    pygame.quit()


def puntaje(button):
    """
    Esta función muestra el puntaje más alto obtenido en el juego.
    Cabe destacar que este código contiene secciones previamente
    comentadas, por lo que en este caso no se explicarán a fondo.
    Esta función no incluye todo el código de los obstáculos.
    También se modificó el límite del personaje y el fondo.
    """
    pygame.init()

    # Constantes del juego
    AMARILLO = (255, 255, 0)
    BLANCO = (255, 255, 255)
    ANCHO = 450
    ALTO = 300
    GRAVEDAD = 1
    FPS = 60

    # Variables del juego
    posicion_x = 50
    posicion_y = 200
    cambio_y = 0
    cambio_x = 0
    activo = True
    jugando = True
    mov_izquierda = False
    mov_derecha = False
    saltando = False
    pasos_cont = 0

    # Se cargan imagenes desde archivos
    fondo = pygame.image.load("fondoPokemonArceus.png")
    derecha = [pygame.image.load('Paso_1.png'),
               pygame.image.load('Paso_2.png')]
    izquierda = [pygame.image.load('Paso_i_1.png'),
                 pygame.image.load('Paso_i_2.png')]
    personaje = pygame.image.load('Quieto.png')
    salto = pygame.image.load('Salto.png')

    # Se crean los objetos de sonido a partir de archivos
    sonido_fondo = pygame.mixer.Sound("pokemonVB.wav")
    sonido_salto = pygame.mixer.Sound("salto.wav")
    pygame.mixer.Sound.play(sonido_fondo, -1)

    # Configuración del modo de visualización
    pantalla = pygame.display.set_mode([ANCHO, ALTO])
    pygame.display.set_caption('Pokémon Runner')
    fuente = pygame.font.Font('freesansbold.ttf', 16)
    fuente_1 = pygame.font.Font('freesansbold.ttf', 20)
    temp = pygame.time.Clock()

    def puntuacion_mayor():
        """
        Permite leer el valor del puntaje más alto obtenido del
        archivo donde fue guardado
        """
        with open("highestscorePRUEBA.txt", "r") as f:
            return f.read()

    try:
        puntaje_mayor = int(puntuacion_mayor())
    except Exception:
        puntaje_mayor = 0

    while jugando:
        temp.tick(FPS)
        pantalla.blit(fondo, (0, 0))

        # Se crean los objetos de texto
        boton_salida = fuente.render('T: Para volver al menú', True,
                                     BLANCO)
        pantalla.blit(boton_salida, (10, 270))
        tex_mayor_puntaje = fuente_1.render('Puntaje más alto', True,
                                            AMARILLO)
        valor_mayor_puntaje = fuente_1.render(f'{puntaje_mayor}', True,
                                              AMARILLO)

        # Se colocan en pantalla los objetos de texto creados
        pantalla.blit(tex_mayor_puntaje, (260, 20))
        pantalla.blit(valor_mayor_puntaje, (330, 45))

        # Condiciones para observar un cambio de movimientos en el jugador
        if pasos_cont + 1 >= 4:
            pasos_cont = 0

        # Se cambia el movimiento del jugador de acuerdo
        # a los condiciones cumplidas
        if mov_izquierda:
            pantalla.blit(izquierda[pasos_cont//2], (posicion_x,
                                                     posicion_y))
            pasos_cont += 1
        elif mov_derecha:
            pantalla.blit(derecha[pasos_cont//2], (posicion_x,
                                                   posicion_y))
            pasos_cont += 1
        elif saltando:
            pantalla.blit(salto, (posicion_x, posicion_y))
            pasos_cont += 1
        else:
            pantalla.blit(personaje, (posicion_x, posicion_y))
            pasos_cont = 0

        # Se crea el manejo del personaje a partir de entradas en el teclado
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                jugando = False

            # Usos y condiciones de teclado cuando el juego no está activo
            if event.type == pygame.KEYDOWN and activo:
                if event.key == pygame.K_UP and cambio_y == 0:
                    pygame.mixer.Sound.play(sonido_salto)
                    mov_izquierda = False
                    saltando = True
                    mov_derecha = False
                    cambio_y = 19
                if event.key == pygame.K_RIGHT:
                    mov_izquierda = False
                    saltando = False
                    mov_derecha = True
                    cambio_x = 2
                if event.key == pygame.K_LEFT:
                    mov_izquierda = True
                    saltando = False
                    mov_derecha = False
                    cambio_x = -2
                if event.key == pygame.K_t:
                    jugando = False
                    pygame.mixer.Sound.stop(sonido_fondo)

            # Usos y condiciones de teclado cuando el juego está activo
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    mov_izquierda = False
                    mov_derecha = False
                    cambio_x = 0
                if event.key == pygame.K_LEFT:
                    mov_izquierda = False
                    mov_derecha = False
                    cambio_x = 0

        # Condiciones para el correcto movimiento del personaje
        # dentro de la ventana. Se cambia el límite del personaje
        if 0 <= posicion_x <= 230:
            posicion_x += cambio_x
        if posicion_x < 0:
            posicion_x = 0
        if posicion_x > 230:
            posicion_x = 230

        if cambio_y > 0 or posicion_y < 200:
            posicion_y -= cambio_y
            cambio_y -= GRAVEDAD
        if posicion_y > 200 and activo:
            posicion_y = 200
        if posicion_y == 200 and cambio_y < 0:
            saltando = False
            cambio_y = 0

        pygame.display.flip()

    pygame.quit()


def salir(button):
    """
    Esta función se encarga de cerrar el programa
    """
    sys.exit()


# Se crean asociaciones entre los botones y las funciones correspondientes
boton_jugar.connect('clicked', main)
boton_tutorial.connect('clicked', tutorial)
boton_puntaje.connect('clicked', puntaje)
boton_salir.connect('clicked', salir)

# Se muestran todos los widgets contenidos en la ventana, toda la jeraquía
ventana.show_all()

# Se ejecuta el ciclo principal de GTK
# Llamada bloqueante
Gtk.main()
