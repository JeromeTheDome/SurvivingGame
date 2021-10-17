import pygame as pg
import gameWindow
from itemIds import Items

class Inventory():
    selectedSlot = None
    grid = [[[]for i in range(9)]for i in range(6)]
    open = False

    for y in range(6):
        for x in range(9):
            grid[y][x] = Items.Id.dirt

    class Render():
        def renderBox(coordinates,itemId,active = False):
            if active == False:
                gameWindow.ForeGround.display.blit(pg.image.load("./Images/hud/inventoryBox.png"),(coordinates[0],coordinates[1]))
            elif active == True:
                gameWindow.ForeGround.display.blit(pg.image.load("./Images/hud/inventoryBoxSelected.png"),(coordinates[0],coordinates[1]))
            gameWindow.ForeGround.display.blit(Items.iconList[itemId],(coordinates[0]+16,coordinates[1]+16))