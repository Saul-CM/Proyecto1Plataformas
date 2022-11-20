#!/usr/bin/python3
import pygame
from pygame import mixer
import sys
from pygame.locals import QUIT
import time
from datetime import datetime

pygame.init()

#Se crea la pantalla de fondo
pantalla = pygame.display.set_mode((1280, 700))

pygame.display.set_caption("Tomatoe game")

# Contadores para saber si ha jugado, bañado
# o dado de comer al tomate
global contadorComer
global contadorBanhar
global contadorJugar
global vida
vida = 1000
contadorComer = 0
contadorBanhar = 0
contadorJugar = 0
#Reloj del juego
mainclock = pygame.time.Clock()
global tick_count
tick_count = 0
global score
score = 0


# Clase que permite detectar y activar botones
class Boton():

    def __init__(self, imagen, pos):
        self.imagen = imagen
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.rect = self.imagen.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, pantallas):
        if self.imagen is not None:
            pantallas.blit(self.imagen, self.rect)

    def checkForInput(self, posicion):
        if posicion[0] in range(self.rect.left,
                                self.rect.right) and posicion[1] in range(
                                    self.rect.top, self.rect.bottom):
            return True
        return False


# Función para alimentar a la mascota
def comer(comida):
    #VARIABLES GLOBALES PARA EL CONTADOR DE VIDA
    global contadorComer
    global vida
    contadorComer += 1
    vida += 150

    # Si la imagen se puede mover
    movimiento = False

    # Posición inicial de la comida
    comida_x = 1075
    comida_y = 575

    # Variables para ejecutar las animaciones del tomate comiendo
    contador_comer = 0
    abrir = False
    anim_comiendo = [
        pygame.image.load("tomatemain2.png"),
        pygame.image.load("tomatecome_1.png"),
        pygame.image.load("tomatecome_2.png"),
        pygame.image.load("tomatecome_3.png"),
        pygame.image.load("tomatecome_4.png"),
        pygame.image.load("tomatecome_5.png"),
        pygame.image.load("tomatecome_6.png"),
        pygame.image.load("tomatecome_7.png"),
        pygame.image.load("tomatecome_8.png"),
        pygame.image.load("tomatecome_9.png")
    ]
    masticando = [
        pygame.image.load("tomatecome_1.png"),
        pygame.image.load("tomatecome_2.png"),
        pygame.image.load("tomatecome_4.png"),
        pygame.image.load("tomatecome_6.png"),
        pygame.image.load("tomatecome_7.png"),
        pygame.image.load("tomatecome_9.png"),
        pygame.image.load("tomatecome_7.png"),
        pygame.image.load("tomatecome_6.png"),
        pygame.image.load("tomatecome_4.png"),
        pygame.image.load("tomatecome_2.png"),
        pygame.image.load("tomatecome_1.png")
    ]

    while True:
        #Posición del mouse
        mouse_pos = pygame.mouse.get_pos()
        pantalla.fill((249, 171, 104))
        tomate()

        # Traer icono de devolver
        devolver = pygame.image.load('volver.png').convert()
        devolver.set_colorkey([255, 255, 255])
        boton_regresar = Boton(devolver, pos=(110, 90))
        boton_regresar.update(pantalla)

        #Icono de refri
        refri = pygame.image.load("refri.png")
        refri.set_colorkey([0, 0, 0])
        boton_refri = Boton(refri, pos=(110, 550))
        boton_refri.update(pantalla)

        # Mostrar comida en la pantalla
        boton_comida = Boton(comida, pos=(comida_x, comida_y))
        boton_comida.update(pantalla)
        comida_w, comida_h = comida.get_size()

        # Coordenadas del tomate
        tomate_x = 640
        tomate_y = 350
        tomate_w = 300
        tomate_h = 300

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Evento que se ejcuta al presionar el mouse
            if event.type == pygame.MOUSEBUTTONDOWN:
                if boton_regresar.checkForInput(mouse_pos):
                    main()
                if boton_refri.checkForInput(mouse_pos):
                    menu_comida()

                # Ver si mouse se encuentra dentro de la imagen de comida
                if boton_comida.checkForInput(mouse_pos):
                    movimiento = True

            # Al soltar el boton del mouse, la comida no se puede mover
            if event.type == pygame.MOUSEBUTTONUP:
                movimiento = False

            # Evento que se encarga del movimiento del mouse
            if event.type == pygame.MOUSEMOTION:
                if movimiento:
                    x, y = mouse_pos
                    # Mouse en el centro de la imagen
                    comida_y = y
                    comida_x = x
                    abrir = True

                    # Si la comida se mueve, el tomate abre la boca
                    if contador_comer + 1 >= 10:
                        pantalla.blit(anim_comiendo[9], (0, 0))
                    elif abrir:
                        pantalla.blit(anim_comiendo[contador_comer // 1],
                                      (0, 0))
                        contador_comer += 1

                    boton_comida.checkForInput([comida_x, comida_y])
                    boton_comida.update(pantalla)
                    pygame.display.update()

            # Si la comida se coloca en la boca del tomate, este la come
            if comida_x + comida_w > tomate_x + 20 and \
                   comida_x < tomate_x + tomate_w/2 -90 and \
                   comida_y + comida_h > tomate_y -30 and \
                   comida_y < tomate_y + tomate_h/2 -80:

                # Coordenadas para que la comida
                # desaparezca de la pantalla
                comida_x = -150
                comida_y = -150
                movimiento = False

                # Efectos de sonido al comer
                comiendo = mixer.Sound('comiendo.mp3')
                comiendo.play()

                # Movimiento del tomate masticando
                for i in range(0, 2):
                    contador_comer = 0
                    while contador_comer < 11:
                        pantalla.blit(masticando[contador_comer // 1], (0, 0))
                        pygame.display.update()
                        contador_comer += 1

        pygame.display.update()


# Función para el menú de comida
def menu_comida():
    while True:
        #Posición del mouse
        mouse_pos = pygame.mouse.get_pos()
        pantalla.fill((249, 171, 104))
        fondo = pygame.image.load('fondo1.jpg').convert()
        pantalla.blit(fondo, (0, 0))

        # Letras del Menú
        font = pygame.font.SysFont("Jokerman", 90)
        text = font.render("Menú", True, [0, 0, 0])
        pantalla.blit(text, [510, 30])

        # Galleta
        galleta = pygame.image.load('galleta.png').convert()
        galleta.set_colorkey([0, 0, 0])
        boton_galleta = Boton(galleta, pos=(225, 250))
        boton_galleta.update(pantalla)

        # Pastelito
        pastelito = pygame.image.load('pastelito.png').convert()
        pastelito.set_colorkey([0, 0, 0])
        boton_pastelito = Boton(pastelito, pos=(500, 250))
        boton_pastelito.update(pantalla)

        # Huevo chocolate
        huevito = pygame.image.load('huevo_choco.png').convert()
        huevito.set_colorkey([0, 0, 0])
        boton_huevito = Boton(huevito, pos=(800, 260))
        boton_huevito.update(pantalla)

        #Queque
        queque = pygame.image.load('pastel.png').convert()
        queque.set_colorkey([0, 0, 0])
        boton_queque = Boton(queque, pos=(1080, 265))
        boton_queque.update(pantalla)

        # Pizza
        pizza = pygame.image.load('Pizza.png').convert()
        pizza.set_colorkey([0, 0, 0])
        boton_pizza = Boton(pizza, pos=(225, 450))
        boton_pizza.update(pantalla)

        #Palomitas
        palomitas = pygame.image.load('palomitas.png').convert()
        palomitas.set_colorkey([0, 0, 0])
        boton_palomitas = Boton(palomitas, pos=(500, 450))
        boton_palomitas.update(pantalla)

        #Sushi
        sushi = pygame.image.load('sushi.png').convert()
        sushi.set_colorkey([0, 0, 0])
        boton_sushi = Boton(sushi, pos=(800, 460))
        boton_sushi.update(pantalla)

        #Hamburguesa
        hamburguesa = pygame.image.load('hamburguesa.png').convert()
        hamburguesa.set_colorkey([0, 0, 0])
        boton_hamburguesa = Boton(hamburguesa, pos=(1080, 460))
        boton_hamburguesa.update(pantalla)

        # Manzana
        manzana = pygame.image.load('manzana.png').convert()
        manzana.set_colorkey([0, 0, 0])
        boton_manzana = Boton(manzana, pos=(225, 635))
        boton_manzana.update(pantalla)

        # Banano
        banano = pygame.image.load('banana.png').convert()
        banano.set_colorkey([0, 0, 0])
        boton_banano = Boton(banano, pos=(500, 635))
        boton_banano.update(pantalla)

        # Sandía
        sandia = pygame.image.load('sandia.png').convert()
        sandia.set_colorkey([0, 0, 0])
        boton_sandia = Boton(sandia, pos=(800, 635))
        boton_sandia.update(pantalla)

        # Uvas
        uvas = pygame.image.load('uvas.png').convert()
        uvas.set_colorkey([0, 0, 0])
        boton_uvas = Boton(uvas, pos=(1080, 635))
        boton_uvas.update(pantalla)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if boton_galleta.checkForInput(mouse_pos):
                    comer(galleta)
                if boton_pastelito.checkForInput(mouse_pos):
                    comer(pastelito)
                if boton_huevito.checkForInput(mouse_pos):
                    comer(huevito)
                if boton_queque.checkForInput(mouse_pos):
                    comer(queque)
                if boton_pizza.checkForInput(mouse_pos):
                    comer(pizza)
                if boton_palomitas.checkForInput(mouse_pos):
                    comer(palomitas)
                if boton_sushi.checkForInput(mouse_pos):
                    comer(sushi)
                if boton_hamburguesa.checkForInput(mouse_pos):
                    comer(hamburguesa)
                if boton_manzana.checkForInput(mouse_pos):
                    comer(manzana)
                if boton_banano.checkForInput(mouse_pos):
                    comer(banano)
                if boton_sandia.checkForInput(mouse_pos):
                    comer(sandia)
                if boton_uvas.checkForInput(mouse_pos):
                    comer(uvas)

        pygame.display.update()


# Función para asear a la mascota
def banar():
    #VARIABLES GLOBALES PARA EL CONTADOR DE VIDA
    global contadorBanhar
    global vida
    contadorBanhar += 1
    vida += 150

    global score
    global tick_count
    score = 0
    while True:
        #Posición del mouse
        mouse_pos = pygame.mouse.get_pos()

        pantalla.fill((249, 171, 104))

        # Traer icono de devolver
        devolver = pygame.image.load('volver.png').convert()
        devolver.set_colorkey([255, 255, 255])
        boton_regresar = Boton(devolver, pos=(110, 90))
        boton_regresar.update(pantalla)

        #Se definen tiempos de baño

        tick_count += 1 / 60
        if tick_count >= 1:
            tick_count = 0
            score += 1
        if score <= 4:
            background = pygame.image.load('baño.jpg').convert()
            background.set_colorkey([0, 0, 0])
            backgroundimgX = 0
            backgroundimgY = 0
            pantalla.blit(background, (backgroundimgX, backgroundimgY))
            mixer.music.load('goldfish.mp3')
            baño = mixer.Sound('afterbubblebath.wav')
            baño.play()
        if score >= 4:
            background = pygame.image.load('tomatebañado.jpg').convert()
            background.set_colorkey([0, 0, 0])
            backgroundimgX = 0
            backgroundimgY = 0
            pantalla.blit(background, (backgroundimgX, backgroundimgY))
            baño = mixer.Sound('sparkle.mp3')
            baño.play()
            # Traer icono de devolver
            devolver = pygame.image.load('volver.png').convert()
            devolver.set_colorkey([255, 255, 255])
            boton_regresar = Boton(devolver, pos=(110, 90))
            boton_regresar.update(pantalla)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if boton_regresar.checkForInput(mouse_pos):
                    main()

        #tomate()
        pygame.display.update()


# Función para jugar con la mascota
def jugar():
    #VARIABLES GLOBALES PARA EL CONTADOR DE VIDA
    global contadorJugar
    global vida
    contadorJugar += 1
    vida += 50
    global score
    global tick_count
    score = 0

    while True:
        #Posición del mouse
        mouse_pos = pygame.mouse.get_pos()

        pantalla.fill((249, 171, 104))

        # Traer icono de devolver
        devolver = pygame.image.load('volver.png').convert()
        devolver.set_colorkey([255, 255, 255])
        boton_regresar = Boton(devolver, pos=(110, 90))
        boton_regresar.update(pantalla)

        #Se definen tiempos de baño

        tick_count += 1 / 60
        if tick_count >= 0.2:
            tick_count = 0
            score += 0.5
        #Secuencia de imagenes para jugar
        if score == 0.5:
            background = pygame.image.load('tomate1.gif').convert()
            background.set_colorkey([0, 0, 0])
            backgroundimgX = 0
            backgroundimgY = 0
            pantalla.blit(background, (backgroundimgX, backgroundimgY))

            bola = mixer.Sound("boing.mp3")
            bola.play()
        if score == 1:
            background = pygame.image.load('tomate2.gif').convert()
            background.set_colorkey([0, 0, 0])
            backgroundimgX = 0
            backgroundimgY = 0
            pantalla.blit(background, (backgroundimgX, backgroundimgY))
            

        if score == 1.5:
            background = pygame.image.load('tomate3.gif').convert()
            background.set_colorkey([0, 0, 0])
            backgroundimgX = 0
            backgroundimgY = 0
            pantalla.blit(background, (backgroundimgX, backgroundimgY))
            bola = mixer.Sound("boing.mp3")
            bola.play()
        if score == 2:
            background = pygame.image.load('tomate4.gif').convert()
            background.set_colorkey([0, 0, 0])
            backgroundimgX = 0
            backgroundimgY = 0
            pantalla.blit(background, (backgroundimgX, backgroundimgY))
            
        if score == 2.5:
            background = pygame.image.load('tomate5.gif').convert()
            background.set_colorkey([0, 0, 0])
            backgroundimgX = 0
            backgroundimgY = 0
            pantalla.blit(background, (backgroundimgX, backgroundimgY))
        if score == 3:
            background = pygame.image.load('tomate6.gif').convert()
            background.set_colorkey([0, 0, 0])
            backgroundimgX = 0
            backgroundimgY = 0
            pantalla.blit(background, (backgroundimgX, backgroundimgY))
            bola = mixer.Sound("boing.mp3")
            bola.play()
        if score == 3.5:
            background = pygame.image.load('tomate7.gif').convert()
            background.set_colorkey([0, 0, 0])
            backgroundimgX = 0
            backgroundimgY = 0
            pantalla.blit(background, (backgroundimgX, backgroundimgY))
          
        if score == 4:
            background = pygame.image.load('tomate8.gif').convert()
            background.set_colorkey([0, 0, 0])
            backgroundimgX = 0
            backgroundimgY = 0
            pantalla.blit(background, (backgroundimgX, backgroundimgY))

        if score == 4.5:
            background = pygame.image.load('tomate9.gif').convert()
            background.set_colorkey([0, 0, 0])
            backgroundimgX = 0
            backgroundimgY = 0
            pantalla.blit(background, (backgroundimgX, backgroundimgY))
            bola = mixer.Sound("boing.mp3")
            bola.play()
        if score == 5:
            background = pygame.image.load('tomate10.gif').convert()
            background.set_colorkey([0, 0, 0])
            backgroundimgX = 0
            backgroundimgY = 0
            pantalla.blit(background, (backgroundimgX, backgroundimgY))
            
        if score == 5.5:
            background = pygame.image.load('tomate11.gif').convert()
            background.set_colorkey([0, 0, 0])
            backgroundimgX = 0
            backgroundimgY = 0
            pantalla.blit(background, (backgroundimgX, backgroundimgY))
            bola = mixer.Sound("boing.mp3")
            bola.play()
        if score >= 6:
            background = pygame.image.load('tomate12.gif').convert()
            background.set_colorkey([0, 0, 0])
            backgroundimgX = 0
            backgroundimgY = 0
            pantalla.blit(background, (backgroundimgX, backgroundimgY))
            bola = mixer.Sound("boing.mp3")
            bola.stop()
            # Traer icono de devolver
            devolver = pygame.image.load('volver.png').convert()
            devolver.set_colorkey([255, 255, 255])
            boton_regresar = Boton(devolver, pos=(110, 90))
            boton_regresar.update(pantalla)
            bola = mixer.Sound("boing.mp3")
            bola.stop()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if boton_regresar.checkForInput(mouse_pos):
                    main()

        #tomate()
        pygame.display.update()


# Función que permite dibujar el tomate
def tomate():
    global vida
    tomateimg = pygame.image.load('tomatemain2.png').convert()
    tomateimg.set_colorkey([0, 0, 0])
    tomateimgX = 0
    tomateimgY = 0
    pantalla.blit(tomateimg, (tomateimgX, tomateimgY))
    if (vida <= 700):
        caquitaImg = pygame.image.load('caquita.png')
        caquitax = 730
        caquitay = 450
        pantalla.blit(caquitaImg, (caquitax, caquitay))

    if (vida <= 500):
        caquitaImg = pygame.image.load('caquita.png')
        caquitax = 710
        caquitay = 450
        pantalla.blit(caquitaImg, (caquitax, caquitay))
    if (vida <= 400):
        caquitaImg = pygame.image.load('caquita.png')
        caquitax = 470
        caquitay = 450
        pantalla.blit(caquitaImg, (caquitax, caquitay))
    if (vida <= 300):
        caquitaImg = pygame.image.load('caquita.png')
        caquitax = 450
        caquitay = 450
        pantalla.blit(caquitaImg, (caquitax, caquitay))

    if (vida <= 200):
        caquitaImg = pygame.image.load('caquita.png')
        caquitax = 430
        caquitay = 450
        pantalla.blit(caquitaImg, (caquitax, caquitay))
    if (vida <= 0):
        tomate_muerto()


def barra_de_corazones():
    global vida
    if (vida > 700):
        V_corazones = pygame.image.load('Vida5.png').convert()
        V_corazones.set_colorkey([0, 0, 0])
        V_corazonesX = 400
        V_corazonesY = 61
        pantalla.blit(V_corazones, (V_corazonesX, V_corazonesY))
    if (vida <=700 and vida > 500):
        IV_corazones = pygame.image.load('Vida4.png').convert()
        IV_corazones.set_colorkey([0, 0, 0])
        IV_corazonesX = 400
        IV_corazonesY = 61
        pantalla.blit(IV_corazones, (IV_corazonesX, IV_corazonesY))
    if (vida <= 500 and vida > 300):
        III_corazones = pygame.image.load('Vida3.png').convert()
        III_corazones.set_colorkey([0, 0, 0])
        III_corazonesX = 400
        III_corazonesY = 61
        pantalla.blit(III_corazones, (III_corazonesX, III_corazonesY))
    if (vida <= 300 and vida > 200):
        II_corazones = pygame.image.load('Vida2.png').convert()
        II_corazones.set_colorkey([0, 0, 0])
        II_corazonesX = 400
        II_corazonesY = 61
        pantalla.blit(II_corazones, (II_corazonesX, II_corazonesY))
    if (vida <= 200 and vida > 0):
        I_corazones = pygame.image.load('Vida1.png').convert()
        I_corazones.set_colorkey([0, 0, 0])
        I_corazonesX = 400
        I_corazonesY = 61
        pantalla.blit(I_corazones, (I_corazonesX, I_corazonesY))
      
def tomate_muerto():
    global vida
    tomateimg = pygame.image.load('ripTomate.jpg').convert()
    tomateimg.set_colorkey([0, 0, 0])
    tomateimgX = 0
    tomateimgY = 0
    pantalla.blit(tomateimg, (tomateimgX, tomateimgY))
    mixer.music.stop()
    muerte = mixer.Sound('mixkit-sad-game-over-trombone-471.wav')
    muerte.play()


# Función principal
def main():
    global contadorComer
    global vida
    # Música de fondo
    mixer.music.load('goldfish.mp3')
    mixer.music.play(-1)

    # Traer icono que abre menú de baño
    bano = pygame.image.load('jabon1.png').convert()
    bano.set_colorkey([0, 0, 0])

    # Traer icono que abre menú de comida
    comida = pygame.image.load("Pizza.png")
    comida.set_colorkey([0, 0, 0])

    # Traer icono que abre menú de juego
    bola = pygame.image.load('Bola_futbol1.png').convert()
    bola.set_colorkey([0, 0, 0])

    # Traer icono de salida
    salida = pygame.image.load('Salida.png').convert()

    # Loop del juego
    running = True
    hora_inicio = datetime.now()
    while running:
        tiempo = (datetime.now() - hora_inicio).total_seconds()
        while (tiempo > 5.3):
            tiempo -= 5.3
        print(tiempo)
        pantalla.fill((249, 171, 104))
        #Posición del mouse
        mouse_pos = pygame.mouse.get_pos()
        # Se definen los botones del menú principal
        boton_comida = Boton(comida, pos=(1075, 150))
        boton_bano = Boton(bano, pos=(1075, 325))
        boton_jugar = Boton(bola, pos=(1075, 500))
        boton_salir = Boton(salida, pos=(150, 100))

        for button in [boton_comida, boton_bano, boton_jugar, boton_salir]:
            button.update(pantalla)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Condición que se activa si mouse presiona
            # cualquiera de los botones definidos
            if event.type == pygame.MOUSEBUTTONDOWN:
                if boton_comida.checkForInput(mouse_pos):
                    comer(comida)
                if boton_bano.checkForInput(mouse_pos):
                    banar()
                if boton_jugar.checkForInput(mouse_pos):
                    jugar()
                elif boton_salir.checkForInput(mouse_pos):
                    pygame.quit()
                    sys.exit()

        if (tiempo > 5):
            vida -= 8
        tomate()
        barra_de_corazones()
        print("------------------------")
        print("vida: ", vida)
        print("contador de bañar: " + str(contadorBanhar))
        print("contador de comer: " + str(contadorComer))
        print("contador de jugar: " + str(contadorJugar))

        pygame.display.update()


if __name__ == '__main__':
    main()
