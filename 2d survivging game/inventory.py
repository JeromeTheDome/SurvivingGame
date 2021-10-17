import pygame as pg
import gameWindow
from itemIds import Items

class Inventory():
    grid = [[[]for i in range(9)]for i in range(6)]

    for y in range(6):
        for x in range(9):
            grid[y][x] = Items.Id.empty

    class Render():
        def renderBox(coordinates,active = False):
            gameWindow.ForeGround.display.blit(pg.image.load("./Images/hud/inventoryBox.png"),(coordinates[0],coordinates[1]))
