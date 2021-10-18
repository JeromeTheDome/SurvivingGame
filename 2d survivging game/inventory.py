import pygame as pg
import gameWindow
from itemIds import Items

class Inventory():
    selectedSlot = None
    grid = [[[]for i in range(9)]for i in range(6)]
    stackAmount = [[[]for i in range(9)]for i in range(6)]
    open = False

    itemOnCursor = Items.Id.empty
    itemCountOnCursor = 0

    for y in range(6):
        for x in range(9):
            grid[y][x] = Items.Id.empty
            stackAmount[y][x] = 0

    def addItem(type):
        #adds to pre existing stack
        for y in range(6):
            for x in range(9):
                if Inventory.grid[y][x] == type and Inventory.stackAmount[y][x]<=99:
                    Inventory.stackAmount[y][x] += 1
                    return False

        #adds to new stack
        for y in range(6):
            for x in range(9):
                if Inventory.grid[y][x] == Items.Id.empty:
                    Inventory.grid[y][x] = type
                    Inventory.stackAmount[y][x] += 1
                    return False

        return True

    class Render():
        inventoryBox = pg.image.load("./Images/hud/inventoryBox.png")
        inventoryBoxSelected = pg.image.load("./Images/hud/inventoryBoxSelected.png")

        def renderBox(coordinates,itemId,active = False):
            if active == False:
                gameWindow.ForeGround.display.blit(Inventory.Render.inventoryBox,(coordinates[0],coordinates[1]))
            elif active == True:
                gameWindow.ForeGround.display.blit(Inventory.Render.inventoryBoxSelected,(coordinates[0],coordinates[1]))
            gameWindow.ForeGround.display.blit(Items.iconList[itemId],(coordinates[0]+16,coordinates[1]+16))