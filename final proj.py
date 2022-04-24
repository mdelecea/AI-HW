import pygame
import sys
import time
from pygame.locals import *
import numpy as np

COLUMNS = 7
ROWS = 6
WINAMOUNT = 4
WINDOWWIDTH = 800
WINDOWHEIGHT = 600
COUNTERDIAMETER = 50
PLAYWIDTH = COLUMNS*(COUNTERDIAMETER+25)+25
PLAYHEIGHT = ROWS*(COUNTERDIAMETER+25)+25
PLAYX = 50
PLAYY = 25
COLGAP = (PLAYWIDTH - COLUMNS*COUNTERDIAMETER) / (COLUMNS+1)
ROWGAP = (PLAYHEIGHT - ROWS*COUNTERDIAMETER) / (ROWS+1)
DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.init()
running = True
playing = True
playGrid = np.zeros((ROWS, COLUMNS), dtype=int)
gridCounterHeights = [ROWS-1]*COLUMNS
turn = 1

def checkWin(grid, col, row, turn, winAmount):
    return (checkWinInRow(grid[row, :], turn, winAmount) or checkWinInRow(grid[:, col], turn, winAmount)
    or checkWinInRow(np.diagonal(grid, offset=col-row), turn, winAmount)
    or checkWinInRow(np.diagonal(np.fliplr(grid), offset=COLUMNS-1-(col+row)), turn, winAmount))

def checkWinInRow(line, turn, winAmount):
    count = 0
    for c in range(len(line)):
        if line[c] == turn:
            count += 1
            if count >= winAmount:
                return True
        else:
            count = 0
    return False

while running:
    mouseX, mouseY = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONUP and playing:
            for col in range(COLUMNS):
                refX = PLAYX + col*COUNTERDIAMETER + (col+1)*COLGAP
                if refX < mouseX < refX + COUNTERDIAMETER and PLAYY < mouseY < PLAYY + PLAYHEIGHT:
                    if gridCounterHeights[col] >= 0:
                        playGrid[gridCounterHeights[col],col] = turn
                        winBool = checkWin(playGrid, col, gridCounterHeights[col], turn, WINAMOUNT)
                        gridCounterHeights[col] -= 1
                        turn = turn % 2 + 1
                        if winBool:
                            playing = False
                            print("Player: " + str(turn) + " wins!")
    DISPLAYSURF.fill((255, 255, 255))
    pygame.draw.rect(DISPLAYSURF, (0, 0, 255), (PLAYX, PLAYY, PLAYWIDTH,PLAYHEIGHT), 0)
    DISPLAYSURF.blit(mouseText, (10, 10))
    for row in range(ROWS):
        for col in range(COLUMNS):
            dcol = int(PLAYX + COUNTERDIAMETER * col + COLGAP *(col+1) + COUNTERDIAMETER/2)
            drow = int(PLAYY + COUNTERDIAMETER * row + ROWGAP * (row+1) + COUNTERDIAMETER/2)
            if playGrid[row][col] == 0:
                pygame.draw.circle(DISPLAYSURF, (255, 255, 255), (dcol,drow) ,int(COUNTERDIAMETER/2),0)
            elif playGrid[row][col] == 1:
                pygame.draw.circle(DISPLAYSURF, (255, 0, 0), (dcol,drow),int(COUNTERDIAMETER/2))
            else:
                pygame.draw.circle(DISPLAYSURF, (255, 255, 0), (dcol,drow),int(COUNTERDIAMETER/2))
    pygame.display.update()
    time.sleep(0.20)