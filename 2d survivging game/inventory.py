import pygame as pg
import gameWindow
from itemIds import Items
import CharacterFile
from entity import Entity

class Inventory():
    selectedSlot = None
    grid = [[[]for i in range(9)]for i in range(6)]
    stackAmount = [[[]for i in range(9)]for i in range(6)]

    craftingTableGrid = [[[]for i in range(3)]for i in range(3)]
    craftingTableStackAmount = [[[]for i in range(3)]for i in range(3)]
    craftingTableOutputBox = Items.Id.empty
    craftingTableOutputAmount = 1
    open = False
    craftingTableOpen = False
    activeCraftingTableCoords = [0,0]

    itemOnCursor = Items.Id.empty
    itemCountOnCursor = 0

    for y in range(6):
        for x in range(9):
            grid[y][x] = Items.Id.empty
            stackAmount[y][x] = 0
    
    for y in range(3):
        for x in range(3):
            craftingTableGrid[y][x] = Items.Id.empty
            craftingTableStackAmount[y][x] = 0

    def addItem(type,amount=1):
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

    def dropItem(slot,entities):
      if Inventory.stackAmount[0][slot] > 1:
        entities += [Entity((CharacterFile.Character.characterLocation[0]+14,CharacterFile.Character.characterLocation[1]-4),(16,16),0,Inventory.grid[0][slot])]

        Inventory.stackAmount[0][slot] -=1
				
      elif Inventory.stackAmount[0][slot] <= 1:
        entities += [Entity((CharacterFile.Character.characterLocation[0]+14,CharacterFile.Character.characterLocation[1]-4),(16,16),0,Inventory.grid[0][slot])]

        Inventory.grid[0][slot] = Items.Id.empty
        Inventory.stackAmount[0][slot] = 0


    class Render():
        inventoryBox = pg.image.load("./Images/hud/inventoryBox.png").convert_alpha()
        inventoryBoxSelected = pg.image.load("./Images/hud/inventoryBoxSelected.png").convert_alpha()
        craftingTableInterface = pg.image.load("./Images/hud/craftingUi.png").convert_alpha()
        arrowDown = pg.image.load("./Images/hud/arrowDown.png").convert_alpha()

        def renderBox(coordinates,itemId,active = False):
            if active == False:
                gameWindow.ForeGround.display.blit(Inventory.Render.inventoryBox,(coordinates[0],coordinates[1]))
            elif active == True:
                gameWindow.ForeGround.display.blit(Inventory.Render.inventoryBoxSelected,(coordinates[0],coordinates[1]))
            gameWindow.ForeGround.display.blit(Items.iconList[itemId],(coordinates[0]+16,coordinates[1]+16))