import pygame
import numpy as np
import time

pygame.init()

#  pantalla

width, height = 1000, 1000  
screen = pygame.display.set_mode((height, width))

bg = 100, 50, 50    # intensidad colores
screen.fill(bg)

nxC, nyC = 70, 70    #celdas del juego

# ancho y alto de celdas
dimCW = width / nxC     
dimCH = height / nyC

# Estado de las celdas. Vivas =1 , Muertas =0
gameState = np.zeros((nxC, nyC))

# Autómata móvil.
gameState[21, 21] = 1
gameState[22, 22] = 1
gameState[22, 23] = 1
gameState[21, 23] = 1
gameState[20, 23] = 1

# Control de la ejecución
pauseExect = False

# Bucle de la ejecución
while True:
    
    newGameState = np.copy(gameState)

    screen.fill(bg)
    time.sleep(0.0005)

    # Registramos eventos de teclado y mouse.
    ev = pygame.event.get()

    for event in ev:
        # Detectamos si se presiona una tecla
        if event.type == pygame.KEYDOWN:
            pauseExect = not pauseExect

        # Detectamos si se presiona el mouse
        mouseClick = pygame.mouse.get_pressed()
        
        if sum(mouseClick) > 0:
            posX, posY = pygame.mouse.get_pos()
            celX, celY = int(np.floor(posX / dimCW)), int(np.floor(posY / dimCH))
            newGameState[celX, celY] = not mouseClick[2]

    for y in range(0, nxC):
        for x in range(0, nyC):

            if not pauseExect:
                

                # Calculamos el número de vecinos cercanos.
                n_neigh = gameState[(x - 1) % nxC, (y - 1) % nyC ] + \
                        gameState[(x) % nxC    , (y - 1) % nyC] + \
                        gameState[(x + 1) % nxC, (y - 1) % nyC] + \
                        gameState[(x - 1) % nxC, (y) % nyC] + \
                        gameState[(x + 1) % nxC, (y) % nyC] + \
                        gameState[(x - 1) % nxC, (y + 1) % nyC] + \
                        gameState[(x) % nxC    , (y + 1) % nyC] + \
                        gameState[(x + 1) % nxC, (y + 1) % nyC] 

                #Regla #1 : Una célula muerta con exactamente 3 vecinas vivas, "revive"         
                if gameState[x, y] == 0 and n_neigh == 3:
                    newGameState[x, y] = 1
                
                # Regla  #2 : Una célula viva con menos de 2 o más de 3 vecinas vivas, "muere"
                elif gameState[x, y] ==1 and (n_neigh < 2 or n_neigh > 3):
                    newGameState[x, y] =0
            # Creamos el polígono de cada celda a dibujar
            poly = [((x) * dimCW, y * dimCH),
                    ((x+1) * dimCW, y * dimCH),
                    ((x+1) * dimCW, (y+1) * dimCH),
                    ((x) * dimCW, (y+1) * dimCH)]

            # Dibujamos la celda para cada par de x e y.
            if newGameState[x, y] == 0:
                pygame.draw.polygon(screen, (128, 128, 128), poly, 1 ) 
            else:
                pygame.draw.polygon(screen, (225, 225, 225), poly, 0 ) 
    
    # Actualizamos el estado del juego.
    gameState = np.copy(newGameState)

    # Actualizamos la pantalla
    pygame.display.flip()

          