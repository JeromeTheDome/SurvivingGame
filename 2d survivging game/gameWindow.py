import pygame
import math
from pygame.locals import *
pg = pygame
import numpy as np
import json
from container import Container
import random
import noise

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

class World():
    time = 0
    openWorld = None
    spawnCoords = [0,0]
    deltaTime = 0
    def generateWorld():
        for y in range(worldHeight):
            for x in range(worldLength):
                Block.BlockMatrix[y][x] = Block.Type.BlockType.air
                Block.bgBlockMatrix[y][x] = Block.Type.BlockType.air
        #sets up bottom squares
        for x in range(worldLength):
            for y in range(10,500):
                try:
                    if not(0.45-y/1000 <= noise.snoise2(x*0.07,y*0.07,repeaty=999999,repeatx=999999,octaves = 1,persistence=1,lacunarity=10) <= 1-y/1000):
                        Block.Grid.placeBlock((x,500 + y),Block.Type.BlockType.stone,True)
                        Block.Grid.placeBlockBg((x,500 + y),Block.Type.BlockType.stone,True)
                    else:
                        Block.Grid.placeBlockBg((x,500 + y),Block.Type.BlockType.stone,True)
                except:
                    pass

        seed = random.randint(0,500)


        for x in range(worldLength):
            frequency = 0.2

            treeTrue = random.randint(0,10)

            y =  int(noise.pnoise1((x/5+seed)*0.3,repeat=999999999)*5)+495

            if x == 500:
                Character.characterLocation[1] = y-2


            if treeTrue == 5:
                Block.Grid.placeBlockBg((x,y-1),Block.Type.BlockType.log,True)
                Block.Grid.placeBlockBg((x,y-2),Block.Type.BlockType.log,True)
                Block.Grid.placeBlockBg((x,y-3),Block.Type.BlockType.log,True)
                Block.Grid.placeBlockBg((x,y-4),Block.Type.BlockType.log,True)

                #first row of leaves
                Block.Grid.placeBlockBg((x-1,y-5),Block.Type.BlockType.leaves,True)
                Block.Grid.placeBlockBg((x-2,y-5),Block.Type.BlockType.leaves,True)
                Block.Grid.placeBlockBg((x,y-5),Block.Type.BlockType.leaves,True)
                Block.Grid.placeBlockBg((x+1,y-5),Block.Type.BlockType.leaves,True)
                Block.Grid.placeBlockBg((x+2,y-5),Block.Type.BlockType.leaves,True)
                #second row
                Block.Grid.placeBlockBg((x-1,y-6),Block.Type.BlockType.leaves,True)
                Block.Grid.placeBlockBg((x-2,y-6),Block.Type.BlockType.leaves,True)
                Block.Grid.placeBlockBg((x,y-6),Block.Type.BlockType.leaves,True)
                Block.Grid.placeBlockBg((x+1,y-6),Block.Type.BlockType.leaves,True)
                Block.Grid.placeBlockBg((x+2,y-6),Block.Type.BlockType.leaves,True)
                #third row
                Block.Grid.placeBlockBg((x-1,y-7),Block.Type.BlockType.leaves,True)
                Block.Grid.placeBlockBg((x,y-7),Block.Type.BlockType.leaves,True)
                Block.Grid.placeBlockBg((x+1,y-7),Block.Type.BlockType.leaves,True)
            
            try:
                Block.Grid.placeBlock((x,y),Block.Type.BlockType.grass,True)
                Block.Grid.placeBlock((x,y+1),Block.Type.BlockType.dirt,True)
                Block.Grid.placeBlock((x,y+2),Block.Type.BlockType.dirt,True)
                Block.Grid.placeBlock((x,y+3),Block.Type.BlockType.dirt,True)
                Block.Grid.placeBlock((x,y+4),Block.Type.BlockType.dirt,True)


                for y in range(y,510):
                    if not(0 <= noise.snoise2(x*0.07,y*0.07,repeaty=999999,repeatx=999999,octaves = 1,persistence=1) <= 0.6):
                        Block.Grid.placeBlock((x,y),Block.Type.BlockType.dirt,True)
                    Block.Grid.placeBlockBg((x,y),Block.Type.BlockType.dirt,True)
            except:
                pass
        World.time = 20000
        World.spawnCoords = [500,500]

class Block():
    #start of subclasses
    class Type():
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
            glowBlock = 10
            glass = 11
            doorTop = 12
            doorBottom = 13
            doorOpen = 14
            lastentry = 15
        
        xCollideBlocks = [14] #any block ids in this list will have collisions disabled

        #list of foreground blocks
        List = [pg.image] * BlockType.lastentry
        List[BlockType.air] = pg.image.load("./Images/block icons/air.png").convert_alpha()
        List[BlockType.stone] = pg.image.load("./Images/block icons/stone.png").convert()
        List[BlockType.dirt] = pg.image.load("./Images/block icons/dirt.png").convert()
        List[BlockType.grass] = pg.image.load("./Images/block icons/grass.png").convert()
        List[BlockType.sand] = pg.image.load("./Images/block icons/sand.png").convert()
        List[BlockType.wood] = pg.image.load("./Images/block icons/wood.png").convert()
        List[BlockType.log] = pg.image.load("./Images/block icons/log.png").convert()
        List[BlockType.leaves] = pg.image.load("./Images/block icons/leaves.png").convert()
        List[BlockType.craftingTable] = pg.image.load("./Images/block icons/craftingTable.png").convert()
        List[BlockType.chest] = pg.image.load("./Images/block icons/chest.png").convert()
        List[BlockType.glowBlock] = pg.image.load("./Images/block icons/glowBlock.png").convert()
        List[BlockType.glass] = pg.image.load("./Images/block icons/glass.png").convert()
        List[BlockType.doorTop] = pg.image.load("./Images/block icons/doorTop.png").convert()
        List[BlockType.doorBottom] = pg.image.load("./Images/block icons/doorBottom.png").convert()
        List[BlockType.doorOpen] = pg.image.load("./Images/block icons/doorOpen.png").convert()
        #list of background blocks
        bgList = [pg.image] * BlockType.lastentry
        bgList[BlockType.stone] = pg.image.load("./Images/bg block icons/stone.png").convert()
        bgList[BlockType.dirt] = pg.image.load("./Images/bg block icons/dirt.png").convert()
        bgList[BlockType.grass] = pg.image.load("./Images/bg block icons/grass.png").convert()
        bgList[BlockType.sand] = pg.image.load("./Images/bg block icons/sand.png").convert()
        bgList[BlockType.wood] = pg.image.load("./Images/bg block icons/wood.png").convert()
        bgList[BlockType.log] = pg.image.load("./Images/bg block icons/log.png").convert()
        bgList[BlockType.leaves] = pg.image.load("./Images/bg block icons/leaves.png").convert_alpha()
        bgList[BlockType.craftingTable] = pg.image.load("./Images/bg block icons/craftingTable.png").convert()
        bgList[BlockType.chest] = pg.image.load("./Images/bg block icons/chest.png").convert()
        bgList[BlockType.glowBlock] = pg.image.load("./Images/bg block icons/glowBlock.png").convert()
        bgList[BlockType.glass] = pg.image.load("./Images/bg block icons/glass.png").convert_alpha()
        #set colorkey for transparent textures
        List[BlockType.leaves].set_colorkey((255,0,255))
        List[BlockType.glass].set_colorkey((255,0,255))
        List[BlockType.doorTop].set_colorkey((255,0,255))
        List[BlockType.doorBottom].set_colorkey((255,0,255))
        List[BlockType.doorOpen].set_colorkey((255,0,255))

        def determineBreakingSpeed(layer):
                pickBreakSpeedMod = 1
                shovelBreakSpeedMod = 1
                axeBreakSpeedMod = 1
                blockAtBreakPos = Block.Grid.getBlockAtLocation2(Block.Grid.blockBreakingPos,layer)
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
                breakSpeedDict = {
                    Block.Type.BlockType.dirt:10*shovelBreakSpeedMod, #dirt
                    Block.Type.BlockType.grass:20 * shovelBreakSpeedMod, #grass
                    Block.Type.BlockType.sand:20 * shovelBreakSpeedMod, #sand
                    Block.Type.BlockType.stone:30 * pickBreakSpeedMod, #stone
                    Block.Type.BlockType.wood:30 * axeBreakSpeedMod, #wood
                    Block.Type.BlockType.log:30 * axeBreakSpeedMod, #log
                    Block.Type.BlockType.leaves:5, #leaves
                    "defaultBreakSpeed":20
                }
                try: #catch exception in case of undefined breakspeed
                    blockBreakSpeed = breakSpeedDict[blockAtBreakPos]
                except:
                    blockBreakSpeed = breakSpeedDict['defaultBreakSpeed']
                return blockBreakSpeed

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
        
        def translateToScreenCoords(cameraPos,blockPos):
            """
            takes player pos and block coordinates and calculates the blocks position relative to zero zero on the display surface
            returns a tuple

            the function has 2 values:
            cameraPos: the position of the players viewpoint
            blockPos: the position of the block being translated 
            """

            xPos = ((blockPos[0]-cameraPos[0])+12.5)*blockSize
            yPos = ((blockPos[1]-cameraPos[1])+12.5)*blockSize

            return (xPos,yPos)


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
                },
                "worldData":{
                "spawnCoords":World.spawnCoords,
                "time":World.time
                }
            }
            
            with open(f"./saves/{worldName}_data.json",'w') as jsonFile:
                json.dump(jsonData,jsonFile)
                jsonFile.close()

            if World.openWorld == None:
                World.openWorld = worldName
            worldFile = open(f"./saves/{worldName}.txt",'w')
            worldFileBg = open(f"./saves/{worldName}_bg.txt",'w')
            for row in range(len(Block.BlockMatrix)):
                np.savetxt(worldFile,Block.BlockMatrix[row])
                np.savetxt(worldFileBg,Block.bgBlockMatrix[row])
            worldFile.close()
            worldFileBg.close()

        def loadWorld(fileName):
            with open(f"./saves/{fileName}_data.json", "r") as inputData:
                data = json.load(inputData)
            Character.characterLocation = data['playerData']['playerPos']
            inventory.Inventory.grid = data['playerData']['playerInventoryGrid']
            inventory.Inventory.stackAmount = data['playerData']['playerInventoryStackGrid']
            World.spawnCoords = data['worldData']['spawnCoords']
            World.time = data['worldData']['time']
            for i in data['containerData']['containers']:
                inventory.Inventory.containers += [Container(i[0],i[1],i[2],i[3])]
            World.openWorld = fileName
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

        def placeBlock(position,blockType,skipRowTranslation = False,offset = (0,0)):
            #translate grid based input into screen cords
            if skipRowTranslation != True:

                x = math.floor((position[0]+Character.characterDrawLocation[0])/blockSize)
                y = math.floor((position[1]+Character.characterDrawLocation[1]-600)/blockSize)
            else:
                x = position[0]
                y = position[1]
            if Block.BlockMatrix[y+offset[1]][x+offset[0]] == Block.Type.BlockType.air:
                Block.BlockMatrix[y+offset[1]][x+offset[0]] = blockType

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

        def getBlockAtLocation(location,layer = 1,offset = (0,0)):

            x = math.floor((location[0]+Character.characterDrawLocation[0])/blockSize)
            y = math.floor((location[1]+Character.characterDrawLocation[1]-600)/blockSize)

            if layer == 1:
                return Block.BlockMatrix[y+offset[1]][x+offset[0]]
            elif layer == 2:
                return Block.bgBlockMatrix[y+offset[1]][x+offset[0]]

        def getBlockAtLocation2(location,layer = 1):
            if layer == 1:
                return Block.BlockMatrix[location[1]][location[0]]
            elif layer == 2:
                return Block.bgBlockMatrix[location[1]][location[0]]
            

    class Renderer(): 
                        #glow block
        emmisiveBlocks = [[10,15,(255,0,0)]]
        transparentBlocks = [0,11]

        lightingOverlayList = []
        #colored light overlay list
        rLightingOverlayList = []
        gLightingOverlayList = []
        bLightingOverlayList = []
        wLightingOverlayList = []

        lightingOverlayList += [pg.image.load("./Images/block icons/lightingOverlays/0.png").convert_alpha()]
        lightingGrid = [[1 for i in range(worldLength)]for i in range(worldHeight)]
        #colored lighting grid
        coloredLightingGrid = [[(1,1,1) for i in range(worldLength)]for i in range(worldHeight)]

        minLightValue = 1
        naturalLightLevel = 15

        colorInvertTable = {
            1:15,
            2:14,
            3:13,
            4:12,
            5:11,
            6:10,
            7:9,
            8:8,
            9:7,
            10:6,
            11:5,
            12:4,
            13:3,
            14:2,
            15:1
        }

        for i in range(0,15):
            lightingOverlayList += [pg.image.load(f"./Images/block icons/lightingOverlays/{i}.png").convert_alpha()]
        for g in range(3):
            if g == 0:
                color = (255,0,0)
                lightingList = rLightingOverlayList
            elif g == 1:
                color = (0,255,0)
                lightingList = gLightingOverlayList
            elif g == 2:
                color = (0,0,255)
                lightingList = bLightingOverlayList
            for i in reversed(range(0,15)):
                overlay = pygame.Surface((32,32))
                overlay.set_alpha(i*17)
                overlay.fill(color)
                lightingList += [overlay]

        global blockSize
        #takes coordinates from 0 to 20 on both axis
        def drawBlock(surface,blockType,position):

            #translate grid based input into screen cords
            x = position[0] - Character.characterLocation[0]
            y = position[1] - (Character.characterLocation[1]) + 19

            x = x * blockSize
            y = y * blockSize
            
            surface.blit(blockType,(x,y))
        
        def blendColors(colors,brightness):
            blendedColor = [0,0,0]
            for i in range(len(colors)):
                if i != (1,1,1):
                    blendedColor[0]+=colors[i][0]
                    blendedColor[1]+=colors[i][1]
                    blendedColor[2]+=colors[i][2]
            blendedColor = [int(blendedColor[0]/i+1),int(blendedColor[1]/i+1),int(blendedColor[2]/i+1)]
            if blendedColor[0] > 255:
                blendedColor[0] = 255
            if blendedColor[1] > 255:
                blendedColor[1] = 255
            if blendedColor[2] > 255:
                blendedColor[2] = 255
            return (blendedColor[0],blendedColor[1],blendedColor[2])
                

        def calcLighting(grid,pos):
            x = pos[0]
            y = pos[1]
            lightGrid = grid
            coloredLightGrid = Block.Renderer.coloredLightingGrid

            maxSurrounding = max(lightGrid[y-1][x],
                   lightGrid[y][x-1],lightGrid[y][x+1],
                   lightGrid[y+1][x])
            numColor = 0
            maxPos = [y-1,x]
            #coloredBool = coloredLightGrid[y-1][x] != (1,1,1) or coloredLightGrid[y+1][x] != (1,1,1) or coloredLightGrid[y][x+1] != (1,1,1) or coloredLightGrid[y][x-1] != (1,1,1)
            #blendBool = coloredLightGrid[y-1][x] != coloredLightGrid[y+1][x] != coloredLightGrid[y][x+1] != coloredLightGrid[y][x-1]
            #if coloredBool and blendBool: 
            #    blendedColor = Block.Renderer.blendColors((coloredLightGrid[y-1][x],coloredLightGrid[y][x-1],coloredLightGrid[y][x+1],coloredLightGrid[y+1][x]))
            #else:
            #blendedColor = "maxpos"

            for i in Block.Renderer.emmisiveBlocks:
                if Block.BlockMatrix[y][x] == i[0] or Block.bgBlockMatrix[y][x] == i[0]:
                    Block.Renderer.coloredLightingGrid[y][x] = i[2]
                    return i[1]

            if lightGrid[y+1][x] >= lightGrid[maxPos[1]][maxPos[0]] and coloredLightGrid[y+1][x] != (1,1,1):
                maxPos = [y+1,x]

            if lightGrid[y][x+1] >= lightGrid[maxPos[1]][maxPos[0]] and coloredLightGrid[y][x+1] != (1,1,1):
                maxPos = [y,x+1]

            if lightGrid[y][x-1] >= lightGrid[maxPos[1]][maxPos[0]] and coloredLightGrid[y][x-1] != (1,1,1):
                maxPos = [y,x-1]
            #checks if blocks are transparent
            for i in Block.Renderer.transparentBlocks:
                if Block.bgBlockMatrix[y][x] == i:
                    bgTransparent = True
                else:
                    bgTransparent = False
                if Block.BlockMatrix[y][x] == i:
                    fgTranparent = True
                else:
                    fgTranparent = False

            if maxSurrounding-2 > Block.Renderer.naturalLightLevel:
                Block.Renderer.coloredLightingGrid[y][x] = Block.Renderer.coloredLightingGrid[maxPos[0]][maxPos[1]]
            if (Block.bgBlockMatrix[y][x] == 0 or bgTransparent == True) and (Block.BlockMatrix[y][x] == 0 or fgTranparent == True) and y < 550:
                return max(Block.Renderer.naturalLightLevel,maxSurrounding-2)
            elif Block.BlockMatrix[y][x] == 0 and maxSurrounding > Block.Renderer.minLightValue:
                return maxSurrounding-2

            if maxSurrounding > Block.Renderer.minLightValue:
                return int(maxSurrounding*0.5)
            return Block.Renderer.minLightValue

        def drawLightOverlay(surface,level,pos):
            #translate grid based input into screen cords
            x = pos[0] - Character.characterLocation[0]
            y = pos[1] - (Character.characterLocation[1]) + 19

            x = x * blockSize
            y = y * blockSize
            
            overlay = pygame.Surface((32,32))
            if Block.Renderer.coloredLightingGrid[pos[1]][pos[0]] == (1,1,1):
                level = Block.Renderer.colorInvertTable[level]
                multiplier = 17
            else:
                multiplier = 8.5
            overlay.set_alpha(int(level*multiplier))
            overlay.fill(Block.Renderer.coloredLightingGrid[pos[1]][pos[0]])

            surface.blit(overlay,(x,y))


        def drawBreakingOverlay(blockBreakNumber,lay):
            if blockBreakNumber > 1 and Block.Grid.getBlockAtLocation2(Block.Grid.blockBreakingPos,lay) != Block.Type.BlockType.air:
                   Block.Renderer.drawBlock(ForeGround.display,pg.image.load("./Images/block icons/breakingOverlays/stage"+str(blockBreakNumber)+".png").convert_alpha(),(Block.Grid.blockBreakingPos[0],Block.Grid.blockBreakingPos[1]))
        def drawBlocksOnScreen(drawSize):
            for y in range(math.floor(Character.characterLocation[1]-20),math.floor(Character.characterLocation[1]+drawSize[1])):
                for x in range(math.floor(Character.characterLocation[0]),math.floor(Character.characterLocation[0]+drawSize[0])): 
                        #draws background blocks
                        if Block.bgBlockMatrix[y][x] != Block.Type.BlockType.air:
                            Block.Renderer.drawBlock(ForeGround.display,Block.Type.bgList[Block.bgBlockMatrix[y][x]],(x,y))
                        #draws foreground blocks and lighting overlay
                        if Block.Renderer.lightingGrid[y][x] != 1:
                            Block.Renderer.drawBlock(ForeGround.display,Block.Type.List[Block.BlockMatrix[y][x]],(x,y))
                        Block.Renderer.lightingGrid[y][x] = Block.Renderer.calcLighting(Block.Renderer.lightingGrid,(x,y))
                        if Block.Renderer.lightingGrid[y][x] != 15 or Block.Renderer.coloredLightingGrid[y][x] != (1,1,1):
                            Block.Renderer.drawLightOverlay(ForeGround.display,Block.Renderer.lightingGrid[y][x],(x,y))
        def drawUiBg(blockType):
            for y in range(25):
                for x in range(25):
                    ForeGround.display.blit(Block.Type.List[blockType],(x*32,y*32))
                        