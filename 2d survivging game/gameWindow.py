import pygame
import math
from enum import IntEnum

pg = pygame

programEnv = "replit"

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
        def breakBlock(position,blockType,skipRowTranslation = False):
            #translate grid based input into screen cords
            if skipRowTranslation != True:
                x = math.floor(position[0]/blockSize)
                y = math.floor(position[1]/blockSize)
            else:
                x = position[0]
                y = position[1]
            Block.BlockMatrix[y][x] = blockType

        def getBlockAtLocation(location):

            #x = math.floor(location[0]/blockSize-Character.characterLocation[0])
            #y = math.floor(location[1]/blockSize-Character.characterLocation[1])-17

            return Block.BlockMatrix[location[1]][location[0]]

    class Renderer():
        global blockSize
        #takes coordinates from 0 to 20 on both axis
        def drawBlock(surface,blockType,position,skipCoordTranslation):

            #translate grid based input into screen cords
            if skipCoordTranslation == False:
                x = position[0] * blockSize
                y = position[1] * blockSize
            #draw block
            if skipCoordTranslation == True:
                x = math.floor(position[0]/blockSize)
                x = x*blockSize
                y = math.floor(position[1]/blockSize)
                y= y*blockSize

            surface.blit(blockType,(x,y))

        def drawBreakingOverlay(surface,position,breakingPhase):
            x = position[0]
            x += Character.characterDrawLocation[0]

            y = position[1]
            y += Character.characterDrawLocation[1]-600
            y = 400

            #draw block
            surface.blit(pg.image.load("./Images/block icons/breakingOverlays/stage"+str(breakingPhase)+".png"),(x,y))

class Character():
    global worldLength
    #things defined at top are used in many functions and subclasses
    characterLocation = [(worldLength/2),501]
    characterDrawLocation = [400,400]
    characterBoundingBox = [383,505,36,72]

    #character images
    class Image():
        global blockSize
        #character still images
        characterStillRight = pg.image.load("./Images/Character Icons/stillRight.png")
        characterStillLeft = pg.image.load("./Images/Character Icons/stillLeft.png")
        """

        debug icons are commented out
        characterImage = pg.image.load("./Images/Character Icons/john.png")
        rightLegUpImage = pg.image.load("./Images/Character Icons/johnRightFoot.png")
        leftLegUpImage = pg.image.load("./Images/Character Icons/johnLeftFoot.png")
        bothLegsUpImage = pg.image.load("./Images/Character Icons/johnBothFeet.png")
        croutchedImage = pg.image.load("./Images/Character Icons/johnCroutched.png")

        #special conditions images (crouched during collision)
        rightLegUpCroutchedImage = pg.image.load("./Images/Character Icons/johnCroutchedRightFoot.png")
        leftLegUpCroutchedImage = pg.image.load("./Images/Character Icons/johnCroutchedLeftFoot.png")
        bothLegsUpCroutchedImage = pg.image.load("./Images/Character Icons/johnCroutchedBothFeet.png")
        """
    class Pos():

        #moves the character left or right
        def update(moveAmount = 1):
            Character.characterDrawLocation[0] = Character.characterLocation[0]*blockSize
            Character.characterDrawLocation[1] = (Character.characterLocation[1]*blockSize)

        #checks for collisions in a specified position relative to the player and returns true or false
        
        #hard coding offsets dont forget to make them variable later
        def CollisionCheck(direction ,custom = False,xOffset = 0,yOffset = 0):
            if custom == False:
                if direction == "right":
                    if(Block.BlockMatrix[math.floor(Character.characterLocation[1])-2+yOffset][math.floor(Character.characterLocation[0])+11+xOffset] != Block.Type.BlockType.air):
                        return True
                elif direction == "left":
                    if(Block.BlockMatrix[math.floor(Character.characterLocation[1])-2+yOffset][math.floor(Character.characterLocation[0])+13+xOffset] != Block.Type.BlockType.air):
                        return True
                elif direction == "leftunder":
                    if(Block.BlockMatrix[math.floor(Character.characterLocation[1])-2+yOffset][math.floor(Character.characterLocation[0])+11+xOffset] != Block.Type.BlockType.air):
                        return True
                elif direction == "rightunder":
                    if(Block.BlockMatrix[math.floor(Character.characterLocation[1])-2+yOffset][math.floor(Character.characterLocation[0])+13+xOffset] != Block.Type.BlockType.air):
                        return True
                elif direction == "under":
                    if(Block.BlockMatrix[math.floor(Character.characterLocation[1])-1+yOffset][math.floor(Character.characterLocation[0])+11+xOffset] != Block.Type.BlockType.air):
                        return True
                elif direction == "above":
                    if (Block.BlockMatrix[math.floor(Character.characterLocation[1])-4+yOffset][math.floor(Character.characterLocation[0])+12+xOffset] != Block.Type.BlockType.air):
                        return True
                else:
                    return False
            elif custom == True:
                if(Block.BlockMatrix[math.floor(Character.characterLocation[1])-(yOffset+-8)][math.floor(Character.characterLocation[0])+(xOffset+12)] != Block.Type.BlockType.air):
                    return True
                else:
                    return False
        def newCollisionCheck(blockCoordX,blockCoordY,xBoundsOffset=0,yBoundsOffset=0,calcOffset=False,moving=0,direction=0):
            #adding a .30 offset while moving was the only way i could get it to work for moving blocks. this code has made me want to hang myself
            offset = 0
            if calcOffset == True and moving == True:
                if direction == 'left':
                    offset = 0.30
                elif direction == 'right':
                    offset = -0.30
                else:
                    offset = 0
            #calculates the fraction at the end of the character location value to add to the offset
            xOffset = round(Character.characterLocation[0],1)%1
            yOffset = round(Character.characterLocation[1],1)%1

            #does offsetting and translates into screen coords
            blockCoordX -= Character.characterLocation[0]+xOffset
            blockCoordX = blockCoordX * blockSize

            #does offsetting and translates into screen coords
            blockCoordY -= Character.characterLocation[1]+yOffset
            blockCoordY = blockCoordY * blockSize

            #defines bounding box locally so i can add offsets
            boundingBox = pg.Rect(Character.characterBoundingBox[0]+xBoundsOffset,Character.characterBoundingBox[1]+yBoundsOffset,Character.characterBoundingBox[2],Character.characterBoundingBox[3])
            pg.draw.rect(ForeGround.display,(255,0,0),pg.Rect(blockCoordX,blockCoordY,32,32))
            if boundingBox.colliderect(pg.Rect(blockCoordX,blockCoordY,32,32)):
                return True
            else:
                return False
    class Render():
        global yCharacterRenderOffset
        global blockSize
        def SpritePick(Direction,AnimationFrameIter):
            #used to decide which frame to display for character 
            if Direction == "left":
                return pg.image.load("./Images/Character Icons/movingLeftFrame"+str(AnimationFrameIter)+".png")
            elif Direction == "right":
                return pg.image.load("./Images/Character Icons/movingRightFrame"+str(AnimationFrameIter)+".png")


        def draw(surface,imageIn,x,y):
        #renders the character still
            x = x * blockSize
            y = y * blockSize
            surface.blit(imageIn,(x,y))

        def drawStillX(surface,imageIn):
            surface.blit(imageIn,(383,505))

  