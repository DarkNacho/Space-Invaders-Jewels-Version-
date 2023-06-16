# -*- coding: utf-8 -*-
##########################################
#                                        #
#     Space Invaders (Jewels Version)    #
#                  by                    #
#    Ignacio Martinez and Carlos Ríos    #
#           November 30, 2017            #
#                                        #
##########################################
import pygame, sys ,random, time


def message(msg, xy, size, color):
    """Permite escribir un mensaje en la posición xy, definiedo tamaño y color"""
    font = pygame.font.Font("8-bit.ttf", size)
    text = font.render(msg, True, color)
    screen.blit(text, xy)


def createMatrix(nn=10, mm=12):
    """Crea una matriz aleatoria"""
    m = []
    for i in range(mm - 4):
        m.append([0] * nn)
    for i in range(4):
        temp = []
        for j in range(nn):
            temp.append(random.randint(1, 3))
        m.append(temp)
    return m


def drawMatrix(x, y, nn=[10, 12]):
    """Dibuja los marcos de la matriz en la ventana"""
    for i in range(nn[0]):
        for j in range(nn[1]):
            pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(x + 43 * i, y + 43 * j, 43, 43), 1)


def printMatrix():
    """Imprime la matriz actual por consola, solo para comprobar jugadas"""
    for i in range(len(board)):
        for j in range(len(board[i])):
            print board[i][j],
        print
    print
    print "------------------"
    print


def getEvent():
    """Obtiene los eventos de PyGame"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # En caso de seleccionar salir
            pygame.quit()
            sys.exit(0)
        if event.type == ENDEVENT:  # cuando se termina una cancion selecciona otra random
            pygame.mixer.music.load(playList[random.randint(0, len(playList) - 1)])
            pygame.mixer.music.play(0)
        if event.type == pygame.MOUSEBUTTONUP:  # en caso de hacer click con el mouse
            return "Click"
        if event.type == pygame.KEYDOWN:  # ve cual tecla se presiona y retorna el valor
            if event.key == pygame.K_RETURN:
                return "Enter"
            elif event.key == pygame.K_ESCAPE:
                return "Back"
            elif event.key == pygame.K_BACKSPACE:
                return "<-"
            elif event.key == pygame.K_w:
                winScreen()
            elif event.key == pygame.K_l:
                loseScreen()


def can(i, j):
    """Verifica que la posición a ingresar esté dentro de la matriz"""
    if i >= 0 and i < len(board) and j >= 0 and j < len(board[i]):
        return True
    else:
        return False


def newRow(level):
    """Añade una nueva fila en la parte inferior de la matriz"""
    row = []
    for i in range(len(board[0])):
        row.append(random.randint(1, level))
    return row


def emptyRow():
    """Verifica si en la primera fila todavía puede insertarse una fila"""
    empty = True
    for i in board[0]:
        if i != 0:
            empty = False
    return empty


def Up():
    """Corre las filas presentes hacia arriba para agregar la fila nueva"""
    for i in range(len(board) - 1):
        board[i], board[i + 1] = board[i + 1], board[i]


def Down():
    """Baja las otras filas cuando estas son eliminadas"""
    for x in range(len(board)):
        for k in range(len(board[x])):
            for i in range(len(board) - 1):
                for j in range(len(board[i])):
                    if board[i][j] != 0 and board[i + 1][j] == 0:
                        board[i][j], board[i + 1][j] = board[i + 1][j], board[i][j]


def emptyColumn(j):
    """Revisa si hay alguna columna vacía"""
    empty = True
    if board[len(board) - 1][j] != 0:
        empty = False
    return empty


def moveColumn(j, side):
    """Mueve la columna actual hacia el centro del tablero"""
    i = 0
    while i < len(board):
        if board[i][j] != 0:
            board[i][j + side], board[i][j] = board[i][j], board[i][j + side]
        i += 1


def removeFig(i, j, fig, l):
    """Función de backtracking para eliminar las fichas adyacentes"""
    board[i][j] = '?'
    l.append([i, j])
    if can(i - 1, j) and board[i - 1][j] == fig:
        removeFig(i - 1, j, fig, l)
    if can(i, j + 1) and board[i][j + 1] == fig:
        removeFig(i, j + 1, fig, l)
    if can(i + 1, j) and board[i + 1][j] == fig:
        removeFig(i + 1, j, fig, l)
    if can(i, j - 1) and board[i][j - 1] == fig:
        removeFig(i, j - 1, fig, l)


def removeElements(mouse, puntaje, bestScore, combo, live=-1):
    """Elimina los elementos de la matriz"""
    delElements = []
    j = (mouse[0] - 261) / 43
    i = (mouse[1] - 69) / 43
    if can(i, j):
        if board[i][j] != 0:
            fig = board[i][j]
            removeFig(i, j, fig, delElements)
            if len(delElements) >= 3:
                printMatrix()
                for items in delElements:
                    board[items[0]][items[1]] = 0
                Down()
                puntaje += points(fig, len(delElements))
            else:
                for items in delElements:
                    board[items[0]][items[1]] = fig
    if len(delElements) > 2 and 0 not in delElements:
        combo = len(delElements)
    return puntaje, combo, delElements


def winScreen():
    """Pantalla de Victoria"""
    pygame.mixer.music.stop()
    end = []
    gif = []
    for i in range(141):
        end.append(pygame.image.load("Resources/end/" + str(i) + ".png"))
        end[i] = pygame.transform.scale(end[i], (720, 500))
    for i in range(18):
        gif.append(pygame.image.load("Resources/end/gif_" + str(i) + ".png"))
    i = 0
    k = 0
    pygame.mixer.music.load("Resources/end/end.mp3")
    pygame.mixer.music.play(-1)
    while True:
        event = getEvent()
        if event == "Enter":
            pygame.mixer.music.stop()
            break
        if i >= 141:
            i = 0
        if k >= 18:  # 10 o 18
            k = 0
        screen.fill([0, 0, 0])
        screen.blit(end[i], (0, 10))
        screen.blit(gif[k], (110, 360))
        message('Congratulations!', (200, 30), 25, (72, 120, 199))
        message('You have complete the game', (70, 80), 25, (72, 120, 199))
        message('Thanks for playing', (90, 300), 30, (247, 136, 114))
        screen.blit(hearth, (585, 300))
        message('Press [Enter] to go back', (130, 650), 20, (255, 255, 255))
        pygame.display.update()
        clock.tick(10)
        i += 1
        if i % 3 == 0:
            k += 1


def loseScreen():
    """pantalla de derrota"""
    pygame.mixer.music.stop()
    loseImage = pygame.image.load('Resources/end/lose.png')
    loseImage = pygame.transform.scale(loseImage, (720, 700))
    pygame.mixer.music.load("Resources/end/lose.mp3")
    tiempoOriginal = time.time()
    tiempoCambioLose = 20
    playing = False
    while True:
        event = getEvent()
        if event == 'Enter':
            pygame.mixer.music.stop()
            break
        tiempoLose = time.time()
        if tiempoLose - tiempoOriginal <= tiempoCambioLose:
            screen.fill((0, 0, 0))
            message('Come on man!', (260, 150), 20, (255, 255, 255))
            message('This game is easy, you should not lose.', (40, 200), 20, (255, 255, 255))
            message('You even don\'t deserve a', (150, 240), 20, (255, 255, 255))
            message('Game Over Screen.', (200, 280), 20, (255, 255, 255))
            message('You should be ashamed...', (150, 320), 20, (255, 255, 255))
            message('Please, don\'t play this game again.', (60, 500), 20, (255, 255, 255))
            message('Close the window now.', (175, 540), 20, (255, 255, 255))
        else:
            screen.blit(loseImage, (0, 0))
            if not playing:
                pygame.mixer.music.play(-1)
                playing = True
            if tiempoLose - tiempoOriginal >= 30:
                message('Don\'t give up, try again!', (145, 615), 20, (255, 255, 255))
            if tiempoLose - tiempoOriginal >= 35:
                message('Press [Enter] to go back', (140, 650), 20, (255, 255, 255))
        pygame.display.update()



def centerColumns():
    """Junta las columnas que están separadas hacia el centro"""
    j = 4
    while j >= 0:
        veces = 0
        while emptyColumn(j) and veces < 4:
            while j - 1 >= 0:
                moveColumn(j - 1, 1)
                j -= 1
            veces += 1
        j -= 1
    j = 5
    while j < 10:
        veces = 0
        while emptyColumn(j) and veces < 4:
            while j + 1 < 10:
                moveColumn(j + 1, -1)
                j += 1
            veces += 1
        j += 1


def arcadeMode(live, bestScore):
    """Modo arcade del juego"""
    pygame.mixer.music.stop()
    pygame.mixer.music.load(playList[random.randint(0, len(playList) - 1)])
    pygame.mixer.music.play(0)
    puntaje = 0
    combo = 0
    speed = 5
    level = 3
    veces = 0
    lives = ['te', 'extraño', 'Cami']
    lost = False
    startTime = int(time.time())
    tiempoCambio = 1
    posImagen = 0
    X = [261, 266, 266, 261]
    Y = [69, 69, 74, 74]
    indiceMovimiento = 0
    delElements = []
    created = False
    while not lost:
        """Dibuja la matriz actual en la ventana, con todos los valores en juego"""
        screen.fill([0, 0, 0])
        screen.blit(fondo, (0, -150))
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(10, 129, 230, 525), 1)
        pygame.draw.rect(screen, (255, 255, 0), pygame.Rect(260, 600, 430, 50), 1)
        drawMatrix(260, 68)
        message("Best Score:", (20, 20), 16, (255, 255, 255))
        message(str(bestScore), (30, 50), 40, (255, 255, 255))
        message("Score:", (20, 150), 20, (255, 255, 255))
        message(str(puntaje), (40, 190), 25, (255, 255, 255))
        message('Combo: ', (20, 250), 20, (255, 255, 255))
        message(str(combo), (40, 290), 25, (255, 255, 255))
        message('Level: ', (20, 350), 20, (255, 255, 255))
        message(str(level - 2), (40, 390), 25, (255, 255, 255))
        message('Rows left:', (20, 450), 20, (255, 255, 255))
        message(str(10 - veces), (40, 490), 25, (255, 255, 255))
        if live != -1:
            message("lives:", [20, 550], 20, (255, 255, 255))
            for i in range(len(lives)):
                screen.blit(hearth, (40 + i * 60, 590))

        if not created:
            row = newRow(level)
            created = True

        tiempo = pygame.time.get_ticks() / 1000

        # Centrar las columnas que estén vacías
        centerColumns()

        # Calcula la animación y la posición de cada bloque
        if tiempo >= tiempoCambio:
            posImagen += 1
            indiceMovimiento += 1
            tiempoCambio += 1
            if posImagen > 1:
                posImagen = 0
            if indiceMovimiento >= len(X):
                indiceMovimiento = 0

        # Dibuja los bloques en pantalla
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] == 1:
                    screen.blit(verde[posImagen], (X[indiceMovimiento] + 43 * j, Y[indiceMovimiento] + 43 * i))
                if board[i][j] == 2:
                    screen.blit(celeste[posImagen], (X[indiceMovimiento] + 43 * j, Y[indiceMovimiento] + 43 * i))
                if board[i][j] == 3:
                    screen.blit(rosa[posImagen], (X[indiceMovimiento] + 43 * j, Y[indiceMovimiento] + 43 * i))
                if board[i][j] == 4:
                    screen.blit(blanco[posImagen], (X[indiceMovimiento] + 43 * j, Y[indiceMovimiento] + 43 * i))
                if board[i][j] == 5:
                    screen.blit(amarillo[posImagen], (X[indiceMovimiento] + 43 * j, Y[indiceMovimiento] + 43 * i))
                if board[i][j] == 6:
                    screen.blit(rojo[posImagen], (X[indiceMovimiento] + 43 * j, Y[indiceMovimiento] + 43 * i))
        for i in range(len(row)):
            if row[i] == 1:
                screen.blit(verde[posImagen], (265 + 43 * i, 605))
            if row[i] == 2:
                screen.blit(celeste[posImagen], (265 + 43 * i, 605))
            if row[i] == 3:
                screen.blit(rosa[posImagen], (265 + 43 * i, 605))
            if row[i] == 4:
                screen.blit(blanco[posImagen], (265 + 43 * i, 605))
            if row[i] == 5:
                screen.blit(amarillo[posImagen], (265 + 43 * i, 605))
            if row[i] == 6:
                screen.blit(rojo[posImagen], (265 + 43 * i, 605))

        """
        if len(delElements) > 2:
            for deleted in delElements:
                y, x = deleted[0], deleted[1]
                screen.blit(explosion, (X[0] + 43 * x, Y[0] + 43 * y))
        """
        pygame.display.update()

        endTime = int(time.time())
        event = getEvent()
        if endTime - startTime >= speed:
            startTime = int(time.time())
            if not emptyRow():
                live -= 1
                if len(lives) > 0:
                    lives.pop()
                veces = 0
                liveSound = pygame.mixer.Sound('Resources/die.wav')
                liveSound.play()
                for i in range(len(board[0])):
                        for i in range(len(board) - 4):
                            board[i] = [0] * len(board[i])
            else:
                Up()
                copyRow = []
                for item in row:
                    copyRow.append(item)
                board[len(board) - 1] = copyRow
                created = False
                veces += 1
            if veces >= 10:
                levelSound = pygame.mixer.Sound('Resources/levelcomplete.wav')
                levelSound.play()
                level += 1
                veces = 0
                if level > 6:
                    winScreen()
                    break
            if live < 0:
                lost = True
        if event == "Click":
            mouse = pygame.mouse.get_pos()
            puntaje, combo, delElements = removeElements(mouse, puntaje, bestScore, combo, live)
            if len(delElements) > 3:
                #why don't work??
                #explosionSound = pygame.mixer.Sound('Resources/explosion.mp3')
                #explosionSound.play()
                for deleted in delElements:
                    y, x = deleted[0], deleted[1]
                    screen.blit(explosion, (X[0] + 43 * x, Y[0] + 43 * y))
                    pygame.display.update()
                    clock.tick(50)
        elif event == "Back":
            break
    if lost:  # Si pierde busca max score y entra a ventana Game Over
        if puntaje > bestScore:
            writeSave(puntaje, maxlive)
        loseScreen()


def points(fig, combo):
    """Calcula el puntaje obtenido en una jugada"""
    valor = 0
    if fig == 1:
        valor = 10
    elif fig == 2:
        valor = 15
    elif fig == 3:
        valor = 20
    elif fig == 4:
        valor = 25
    elif fig == 5:
        valor = 30
    elif fig == 6:
        valor = 35
    valor *= combo
    if combo in range(5, 8):
        valor *= 2
    elif combo >= 8:
        valor *= 3
    return valor


def MainMenu():
    """Pantalla del menú principal"""
    selection = False
    pygame.mixer.music.load("Resources/main.mp3")
    pygame.mixer.music.play(-1)
    logo = pygame.image.load('Resources/main.png')
    logo = pygame.transform.scale(logo, (650, 290))
    while not selection:
        event = getEvent()
        if event == "Enter":
            selection = True
            arcadeMode(maxlive, bestScoreArcade)
        screen.fill([0, 0, 0])
        screen.blit(logo, (40, 100))
        message('Jewels Version', (150, 430), 30, (255, 255, 0))
        message('Press [Enter] to start', (110, 550), 25, (255, 255, 255))
        pygame.display.update()


def readSave():
    """Obtiene los puntajes máximos del juego desde archivo externo"""
    try:
        f = open("Resources/save", "r")
        bestScoreArcade = int(f.readline())
        maxlive = int(f.readline())
        f.close()
        return bestScoreArcade, maxlive
    except:
        return 0, 3


def writeSave(bestScoreArcade, maxlive):
    """Guarda los puntajes máximos del juego en archivo externo"""
    try:
        f = open("Resources/save", "w")
        f.write(str(bestScoreArcade) + "\n" + str(maxlive))
        f.close()
    except:
        pass


# Variables globales e iniciación de funciones
pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()
pygame.mixer.set_num_channels(64)
ENDEVENT = 42
pygame.mixer.music.set_endevent(ENDEVENT)
size = [720, 700]
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
pygame.display.set_caption("Space Invaders (Jewels Version)")

fondo = pygame.image.load('Resources/fondo2.png')
fondo = pygame.transform.scale(fondo, (720, 1000))

img1A = pygame.image.load("Resources/verdeA.png")
img1A = pygame.transform.scale(img1A, (35, 35))
img1B = pygame.image.load("Resources/verdeB.png")
img1B = pygame.transform.scale(img1B, (35, 35))
verde = [img1A, img1B]

img2A = pygame.image.load("Resources/celesteA.png")
img2A = pygame.transform.scale(img2A, (35, 35))
img2B = pygame.image.load("Resources/celesteB.png")
img2B = pygame.transform.scale(img2B, (35, 35))
celeste = [img2A, img2B]

img3A = pygame.image.load("Resources/rosaA.png")
img3A = pygame.transform.scale(img3A, (35, 35))
img3B = pygame.image.load("Resources/rosaB.png")
img3B = pygame.transform.scale(img3B, (35, 35))
rosa = [img3A, img3B]

img4A = pygame.image.load("Resources/blancoA.png")
img4A = pygame.transform.scale(img4A, (35, 35))
img4B = pygame.image.load("Resources/blancoB.png")
img4B = pygame.transform.scale(img4B, (35, 35))
blanco = [img4A, img4B]

img5A = pygame.image.load("Resources/amarilloA.png")
img5A = pygame.transform.scale(img5A, (35, 35))
img5B = pygame.image.load("Resources/amarilloB.png")
img5B = pygame.transform.scale(img5B, (35, 35))
amarillo = [img5A, img5B]

img6A = pygame.image.load("Resources/rojoA.png")
img6A = pygame.transform.scale(img6A, (35, 35))
img6B = pygame.image.load("Resources/rojoB.png")
img6B = pygame.transform.scale(img6B, (35, 35))
rojo = [img6A, img6B]

explosion = pygame.image.load('Resources/explosion.png')
explosion = pygame.transform.scale(explosion, (40, 40))

hearth = pygame.image.load('Resources/hearth.png')
hearth = pygame.transform.scale(hearth, (50, 50))

playList = ["Resources/song1.mp3", "Resources/song2.mp3", "Resources/song3.mp3"]
while True:
    pass
    bestScoreArcade, maxlive = readSave()
    board = createMatrix()
    MainMenu()