import pygame
import random
import sys

# Inicialización
pygame.init()
ANCHO, ALTO = 600, 400
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Canasta vs. Monstruos")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (200, 0, 0)
VERDE = (0, 200, 0)

# Fuente
fuente = pygame.font.SysFont(None, 36)

# Reloj
reloj = pygame.time.Clock()
FPS = 60

# Cargar imágenes
canasta_img = pygame.transform.scale(pygame.image.load("assets//images//canasta.png"), (60, 40))
fruta_img = pygame.transform.scale(pygame.image.load("assets//images//fresa.png"), (30, 30))
monstruo_img = pygame.transform.scale(pygame.image.load("assets//images//mounstruo.png"), (30, 30))

# Jugador
jugador = canasta_img.get_rect()
jugador.midbottom = (ANCHO // 2, ALTO - 10)
vel_jugador = 7

# Objetos
objetos = []
TIPOS = ['fruta', 'monstruo']

def generar_objeto():
    tipo = random.choice(TIPOS)
    x = random.randint(0, ANCHO - 30)
    rect = pygame.Rect(x, 0, 30, 30)
    return {'tipo': tipo, 'rect': rect}

def mover_jugador(teclas):
    if teclas[pygame.K_LEFT] and jugador.left > 0:
        jugador.x -= vel_jugador
    if teclas[pygame.K_RIGHT] and jugador.right < ANCHO:
        jugador.x += vel_jugador

def dibujar_objetos():
    for obj in objetos:
        if obj['tipo'] == 'fruta':
            ventana.blit(fruta_img, obj['rect'])
        else:
            ventana.blit(monstruo_img, obj['rect'])

def dibujar_texto(texto, x, y):
    img = fuente.render(texto, True, NEGRO)
    ventana.blit(img, (x, y))

def menu_inicio():
    ventana.fill(VERDE)
    dibujar_texto("Presiona cualquier tecla para comenzar", 80, ALTO // 2)
    pygame.display.flip()
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                esperando = False

def game_over(puntaje):
    ventana.fill(ROJO)
    dibujar_texto(f"Perdiste. Puntaje: {puntaje}", 150, ALTO // 2 - 20)
    dibujar_texto("Presiona cualquier tecla para salir", 100, ALTO // 2 + 20)
    pygame.display.flip()
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                pygame.quit()
                sys.exit()

# Bucle principal
menu_inicio()
puntaje = 0
contador = 0

juego_en_ejecucion = True
while juego_en_ejecucion:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            juego_en_ejecucion = False

    teclas = pygame.key.get_pressed()
    mover_jugador(teclas)

    # Generar objetos
    contador += 1
    if contador % 60 == 0:
        objetos.append(generar_objeto())

    # Mover objetos y verificar colisiones
    for obj in objetos[:]:
        obj['rect'].y += 5

        if jugador.colliderect(obj['rect']):
            if obj['tipo'] == 'fruta':
                puntaje += 1
            else:
                game_over(puntaje)
            objetos.remove(obj)

        elif obj['rect'].top > ALTO:
            if obj['tipo'] == 'fruta':
                game_over(puntaje)
            objetos.remove(obj)

    # Dibujar todo
    ventana.fill(BLANCO)
    ventana.blit(canasta_img, jugador)
    dibujar_objetos()
    dibujar_texto(f"Puntaje: {puntaje}", 10, 10)

    pygame.display.flip()
    reloj.tick(FPS)

pygame.quit()
