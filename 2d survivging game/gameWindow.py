import pygame
import math
from pygame.locals import *
pg = pygame
import numpy as np
import json
from container import Container

class ForeGround():
  cursorIcon = pg.image.load("./Images/background images/cursor.png")

  #inits the pygame window
  def __init__(self):
    pg.init()
    flags = DOUBLEBUF|RESIZABLE
    ForeGround.display = pg.display.set_mode((800,800),flags)
  def getMousePos():
   mousePos = [pg.mouse.get_pos()[0], pg.mouse.get_pos()[1]]
   return mousePos

ForeGround.__init__(1)

from enum import IntEnum
from CharacterFile import Character
import inventory
import itemIds

worldLength = 1000
worldHeight = 1000

yCharacterRenderOffset = 72


#blockSize used for rendering
blockSize = 32
numBlocks = int(800/blockSize)
         

class BackGround():

    bgImage = pg.image.load
    Surface = pg.Surface((800,800))

    #used to put background on display surface and scroll it
    def BlitToSurface(surface,image,X):
        global bgImage
        X = X*15
        surface.blit(image,(X,0))

    bgBlockOverlay = pg.image.load("./Images/background images/bgOverlay.png").convert_alpha()

class Gui():
    loadGameButton = pg.image.load("./Images/Gui/load game button.png").convert_alpha()
    newGameButton = pg.image.load("./Images/Gui/new game button.png").convert_alpha()
    backButton = pg.image.load("./Images/Gui/back button.png").convert_alpha()
    selectFileButton = pg.image.load("./Images/Gui/load screen button.png").convert_alpha()
    saveButton = pg.image.load("./Images/Gui/save button.png").convert_alpha()
    exitToMenuButton = pg.image.load("./Images/Gui/exit to menu button.png").convert_alpha()

class Block():
    #start of subclasses
    openWorld = None
    class Type():
        def determineBreakingSpeed():
            pickBreakSpeedMod = 1
            shovelBreakSpeedMod = 1
            axeBreakSpeedMod = 1
            if inventory.Inventory.selectedSlot != None and 51 <= inventory.Inventory.grid[0][inventory.Inventory.selectedSlot] <= 100:
                if inventory.Inventory.grid[0][inventory.Inventory.selectedSlot] == itemIds.Items.Id.defaultPick:
                    pickBreakSpeedMod = 0.15
                    shovelBreakSpeedMod = 1
                    axeBreakSpeedMod = 1
                elif inventory.Inventory.grid[0][inventory.Inventory.selectedSlot] == itemIds.Items.Id.defaultAxe:
                    pickBreakSpeedMod = 1
                    shovelBreakSpeedMod = 1
                    axeBreakSpeedMod = 0.15
                elif inventory.Inventory.grid[0][inventory.Inventory.selectedSlot] == itemIds.Items.Id.defaultShovel:
                    pickBreakSpeedMod = 1
                    shovelBreakSpeedMod = 0.15
                    axeBreakSpeedMod = 1
            if Block.Grid.getBlockAtLocation2(Block.Grid.blockBreakingPos) == Block.Type.BlockType.dirt:
                blockBreakSpeed = 10 * shovelBreakSpeedMod
            elif Block.Grid.getBlockAtLocation2(Block.Grid.blockBreakingPos) == Block.Type.BlockType.grass:
                blockBreakSpeed = 20 * shovelBreakSpeedMod
            elif Block.Grid.getBlockAtLocation2(Block.Grid.blockBreakingPos) == Block.Type.BlockType.sand:
                blockBreakSpeed = 20 * shovelBreakSpeedMod
            elif Block.Grid.getBlockAtLocation2(Block.Grid.blockBreakingPos) == Block.Type.BlockType.stone:
                blockBreakSpeed = 30 * pickBreakSpeedMod
            elif Block.Grid.getBlockAtLocation2(Block.Grid.blockBreakingPos) == Block.Type.BlockType.wood:
                blockBreakSpeed = 30 * axeBreakSpeedMod
            elif Block.Grid.getBlockAtLocation2(Block.Grid.blockBreakingPos) == Block.Type.BlockType.log:
                blockBreakSpeed = 30 * axeBreakSpeedMod
            elif Block.Grid.getBlockAtLocation2(Block.Grid.blockBreakingPos) == Block.Type.BlockType.leaves:
                blockBreakSpeed = 5
            else:
                blockBreakSpeed = 20
            return blockBreakSpeed

        class BlockType(IntEnum):
            air = 0
            stone = 1
            dirt = 2
            grass = 3
            sand = 4
            wood = 5
            log = 6
            leaves = 7
            craftingTable = 8
            chest = 9
            lastentry = 10
        
        List = [pg.image] * BlockType.lastentry
        List[BlockType.air] = pg.image.load("./Images/block icons/air.png").convert_alpha()
        List[BlockType.stone] = pg.image.load("./Images/block icons/stone.png").convert()
        List[BlockType.dirt] = pg.image.load("./Images/block icons/dirt.png").convert()
        List[BlockType.grass] = pg.image.load("./Images/block icons/grass.png").convert()
        List[BlockType.sand] = pg.image.load("./Images/block icons/sand.png").convert()
        List[BlockType.wood] = pg.image.load("./Images/block icons/wood.png").convert()
        List[BlockType.log] = pg.image.load("./Images/block icons/log.png").convert()
        List[BlockType.leaves] = pg.image.load("./Images/block icons/leaves.png").convert_alpha()
        List[BlockType.craftingTable] = pg.image.load("./Images/block icons/craftingTable.png").convert_alpha()
        List[BlockType.chest] = pg.image.load("./Images/block icons/chest.png").convert_alpha()

    global worldLength
    global numBlocks
    global worldHeight
    #all of these are defined at the top as many subclasses of block rely on them

    #list variable for storing block data. structure is BlockMatrix[Horizontal Columns(uses y input)][Block in column(uses x input)][blockType]
    BlockMatrix = [[[]for i in range(worldLength)]for i in range(worldHeight)]
    bgBlockMatrix = [[[]for i in range(worldLength)]for i in range(worldHeight)]

    #sets every block to air
    for y in range(worldHeight):
        for x in range(worldLength):
            BlockMatrix[y][x] = Type.BlockType.dirt
            bgBlockMatrix[y][x] = Type.BlockType.air



    class Grid():
        global worldLength
        global blockSize

        blockBreakingPos = [0,0]
        blockBreakingPosLast = [0,0]

        #inits the BlockGrid
        def translateToBlockCoords(position):
            #translate grid based input into screen cords
            x = math.floor((position[0]+Character.characterDrawLocation[0])/blockSize)
            y = math.floor((position[1]+Character.characterDrawLocation[1]-600)/blockSize)
            returnValue = [x,y]
            return returnValue

        def saveWorld(worldName):
            jsonContainers = []

            for i in inventory.Inventory.containers:
                jsonContainers += [[i.position,i.type,i.grid,i.stackGrid]]

            jsonData = {
                "playerData":{
                "playerPos":[round(Character.characterLocation[0],2),round(Character.characterLocation[1],2)],
                "playerInventoryGrid":inventory.Inventory.grid,
                "playerInventoryStackGrid":inventory.Inventory.stackAmount,
                },
                "containerData":{
                    "containers":jsonContainers,
                }
            }
            
            with open(f"./saves/{worldName}_data.json",'w') as jsonFile:
                json.dump(jsonData,jsonFile)
                jsonFile.close()

            if Block.openWorld == None:
                Block.openWorld = worldName
            worldFile = open(f"./saves/{worldName}.txt",'w')
            worldFileBg = open(f"./saves/{worldName}_bg.txt",'w')
            for row in range(len(Block.BlockMatrix)):
                np.savetxt(worldFile,Block.BlockMatrix[row])
                np.savetxt(worldFileBg,Block.bgBlockMatrix[row])
            worldFile.close()

        def loadWorld(fileName):
            with open(f"./saves/{fileName}_data.json", "r") as inputData:
                data = json.load(inputData)
            Character.characterLocation = data['playerData']['playerPos']
            inventory.Inventory.grid = data['playerData']['playerInventoryGrid']
            inventory.Inventory.stackAmount = data['playerData']['playerInventoryStackGrid']
            for i in data['containerData']['containers']:
                inventory.Inventory.containers += [Container(i[0],i[1],i[2],i[3])]
            Block.openWorld = fileName
            worldData = np.loadtxt(f"./saves/{fileName}.txt").reshape(worldHeight,worldLength)
            Block.BlockMatrix = worldData.astype(int)
            worldBgData = np.loadtxt(f"./saves/{fileName}_bg.txt").reshape(worldHeight,worldLength)
            Block.bgBlockMatrix = worldBgData.astype(int)
            print(f"loaded world: {fileName}")
        def SetBlockBreakCoord(position):
            x = math.floor((position[0])/blockSize)
            y = math.floor((position[1]-8)/blockSize)

            Block.Grid.blockBreakingPosLast[0] = Block.Grid.blockBreakingPos[0]
            Block.Grid.blockBreakingPosLast[1] = Block.Grid.blockBreakingPos[1]

            Block.Grid.blockBreakingPos[0] = x
            Block.Grid.blockBreakingPos[1] = y

        def placeBlock(position,blockType,skipRowTranslation = False):
            #translate grid based input into screen cords
            if skipRowTranslation != True:

                x = math.floor((position[0]+Character.characterDrawLocation[0])/blockSize)
                y = math.floor((position[1]+Character.characterDrawLocation[1]-600)/blockSize)
            else:
                x = position[0]
                y = position[1]
            if Block.BlockMatrix[y][x] == Block.Type.BlockType.air:
                Block.BlockMatrix[y][x] = blockType

        def placeBlockBg(position,blockType,skipRowTranslation = False):
            #translate grid based input into screen cords
            if skipRowTranslation != True:

                x = math.floor((position[0]+Character.characterDrawLocation[0])/blockSize)
                y = math.floor((position[1]+Character.characterDrawLocation[1]-600)/blockSize)
            else:
                x = position[0]
                y = position[1]
            if Block.bgBlockMatrix[y][x] == Block.Type.BlockType.air:
                Block.bgBlockMatrix[y][x] = blockType
        def breakBlock(position,layer = 0):
            #translate grid based input into screen cords
            
            x = math.floor((position[0]+Character.characterDrawLocation[0])/blockSize)
            y = math.floor((position[1]+Character.characterDrawLocation[1]-608)/blockSize)
            
            if layer == 1:
                Block.BlockMatrix[y][x] = 0
            elif layer == 2:
                Block.bgBlockMatrix[y][x] = 0
            else:
                Block.BlockMatrix[y][x] = 0
                Block.bgBlockMatrix[y][x] = 0

        def getBlockAtLocation(location):

            x = math.floor((location[0]+Character.characterDrawLocation[0])/blockSize)
            y = math.floor((location[1]+Character.characterDrawLocation[1]-600)/blockSize)

            return Block.BlockMatrix[y][x]

        def getBlockAtLocation2(location):
            return Block.BlockMatrix[location[1]][location[0]]

    class Renderer():
        global blockSize
        #takes coordinates from 0 to 20 on both axis
        def drawBlock(surface,blockType,position,bg = False):

            #translate grid based input into screen cords
            x = position[0] - Character.characterLocation[0]
            y = position[1] - (Character.characterLocation[1]) + 19

            x = x * blockSize
            y = y * blockSize

            surface.blit(blockType,(x,y))

            if bg == True:
                surface.blit(BackGround.bgBlockOverlay,(x,y))


        def drawBreakingOverlay(blockBreakNumber):
            if blockBreakNumber > 1 and Block.Grid.getBlockAtLocation2(Block.Grid.blockBreakingPos) != Block.Type.BlockType.air:
                   Block.Renderer.drawBlock(ForeGround.display,pg.image.load("./Images/block icons/breakingOverlays/stage"+str(blockBreakNumber)+".png").convert_alpha(),(Block.Grid.blockBreakingPos[0],Block.Grid.blockBreakingPos[1]))
        def drawBlocksOnScreen(drawSize):
            for y in range(math.floor(Character.characterLocation[1]-20),math.floor(Character.characterLocation[1]+drawSize[1])):
                for x in range(math.floor(Character.characterLocation[0]),math.floor(Character.characterLocation[0]+drawSize[0])): 
                        if Block.bgBlockMatrix[y][x] != Block.Type.BlockType.air and Block.BlockMatrix[y][x] == Block.Type.BlockType.air:
                            Block.Renderer.drawBlock(ForeGround.display,Block.Type.List[Block.bgBlockMatrix[y][x]],(x,y),True)
                        Block.Renderer.drawBlock(ForeGround.display,Block.Type.List[Block.BlockMatrix[y][x]],(x,y))

                        