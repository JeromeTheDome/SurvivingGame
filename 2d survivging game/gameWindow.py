import pygame
import math
from enum import IntEnum
from Character import Character

pg = pygame

worldLength = 1000
worldHeight = 1000

yCharacterRenderOffset = 72


#blockSize used for rendering
blockSize = 32
numBlocks = int(800/blockSize)

class ForeGround():
  cursorIcon = pg.image.load("./Images/background images/cursor.png")

  #inits the pygame window
  def __init__(self):
    pg.init()
    ForeGround.display = pg.display.set_mode((800,800))
  def getMousePos():
   mousePos = [pg.mouse.get_pos()[0], pg.mouse.get_pos()[1]]
   return mousePos
         

class BackGround():

    bgImage = pg.image.load
    Surface = pg.Surface((800,800))

    #used to put background on display surface and scroll it
    def BlitToSurface(surface,image,X):
        global bgImage
        X = X*15
        surface.blit(image,(X,0))


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
            lastentry = 6
        
        List = [pg.image] * BlockType.lastentry
        List[BlockType.air] = pg.image.load("./Images/block icons/air.png")
        List[BlockType.stone] = pg.image.load("./Images/block icons/stone.png")
        List[BlockType.dirt] = pg.image.load("./Images/block icons/dirt.png")
        List[BlockType.grass] = pg.image.load("./Images/block icons/grass.png")
        List[BlockType.sand] = pg.image.load("./Images/block icons/sand.png")
        List[BlockType.wood] = pg.image.load("./Images/block icons/wood.png")

    global worldLength
    global numBlocks
    global worldHeight
    #all of these are defined at the top as many subclasses of block rely on them

    #defines air for default block type
    air = pg.image.load("./Images/block icons/air.png")

    #list variable for storing block data. structure is BlockMatrix[Horizontal Columns(uses y input)][Block in column(uses x input)][blockType]
    BlockMatrix = [[[]for i in range(worldLength +1)]for i in range(worldHeight)]

    #sets every block to air
    for y in range(worldHeight):
        for x in range(worldLength):
            BlockMatrix[y][x] = Type.BlockType.air



    class Grid():
        global worldLength
        global blockSize

        blockBreakingPos = [0,0]

        #inits the BlockGrid

        def SetBlockBreakCoord(position):
            x = math.floor(position[0]/blockSize)
            y = math.floor(position[1]/blockSize)

            Block.Grid.blockBreakingPos[0] = x
            Block.Grid.blockBreakingPos[1] = y

        def placeBlock(position,blockType,skipRowTranslation = False):
            #translate grid based input into screen cords
            if skipRowTranslation != True:

                x = math.floor(position[0]/blockSize)
                y = math.floor(position[1]/blockSize)
            else:
                x = position[0]
                y = position[1]
            if Block.BlockMatrix[y][x] == Block.Type.BlockType.air:
                Block.BlockMatrix[y][x] = blockType
        def breakBlock(position):
            #translate grid based input into screen cords
            
            x = math.floor(position[0]/blockSize)
            y = math.floor(position[1]/blockSize)
         
            Block.BlockMatrix[y][x] = 0

        def getBlockAtLocation(location):

            return Block.BlockMatrix[location[1]][location[0]]

    class Renderer():
        global blockSize
        #takes coordinates from 0 to 20 on both axis
        def drawBlock(surface,blockType,position):

            #translate grid based input into screen cords
            x = position[0] - Character.characterLocation[0]
            y = position[1] - (Character.characterLocation[1]) + 19

            x = x * blockSize
            y = y * blockSize

            surface.blit(blockType,(x,y))

        def drawBreakingOverlay(blockBreakNumber):
            if blockBreakNumber > 1 and Block.Grid.getBlockAtLocation((Block.Grid.blockBreakingPos[0],Block.Grid.blockBreakingPos[1])) != Block.Type.BlockType.air:
                   Block.Renderer.drawBlock(ForeGround.display,pg.image.load("./Images/block icons/breakingOverlays/stage"+str(blockBreakNumber)+".png"),(Block.Grid.blockBreakingPos[0],Block.Grid.blockBreakingPos[1]))
        def drawBlocksOnScreen():
            for y in range(math.floor(Character.characterLocation[1]-20),math.floor(Character.characterLocation[1]+7)):
                for x in range(math.floor(Character.characterLocation[0]),math.floor(Character.characterLocation[0]+26)): 
                        Block.Renderer.drawBlock(ForeGround.display,Block.Type.List[Block.BlockMatrix[y][x]],(x,y))
