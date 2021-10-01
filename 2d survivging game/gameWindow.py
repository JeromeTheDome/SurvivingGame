import pygame
import math
from enum import IntEnum

pg = pygame

programEnv = "replit"

worldLength = 99

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
            lastentry = 5
        
        List = [pg.image] * BlockType.lastentry
        List[BlockType.air] = pg.image.load("./Images/block icons/air.png")
        List[BlockType.stone] = pg.image.load("./Images/block icons/stone.png")
        List[BlockType.dirt] = pg.image.load("./Images/block icons/dirt.png")
        List[BlockType.grass] = pg.image.load("./Images/block icons/grass.png")
        List[BlockType.sand] = pg.image.load("./Images/block icons/sand.png")

    global worldLength
    #all of these are defined at the top as many subclasses of block rely on them

    #defines air for default block type
    air = pg.image.load("./Images/block icons/air.png")

    #list variable for storing block data. structure is BlockMatrix[Horizontal Columns(uses y input)][Block in column(uses x input)][blockType]
    BlockMatrix = [[[]for i in range(worldLength +1)]for i in range(20)]

    #sets every block to air
    for y in range(20):
        for x in range(worldLength):
            BlockMatrix[y][x] = Type.BlockType.air



    class Grid():
        global worldLength

        #inits the BlockGrid
        def placeBlock(position,blockType,skipRowTranslation = False):
            #translate grid based input into screen cords
            if skipRowTranslation != True:
                x = math.floor(position[0]/40)
                y = math.floor(position[1]/40)
            else:
                x = position[0]
                y = position[1]
            if x > 99:
                x = 99
            Block.BlockMatrix[y][x] = blockType
        #shfits coordinate data for block matrix
        def shiftBlockMatrix(rangeStartCoord,rangeEndCoord):
          for y in range(0,25):
            for x in range(rangeStartCoord,rangeEndCoord):
              print("x:",x)
              print("y:",y)
              Block.BlockMatrix[y][x-1] = Block.BlockMatrix[y][x]
              Block.BlockMatrix[y][x] = Block.Type.air
      




    class Renderer():
        
        air = pg.image.load("./Images/block icons/air.png")
        stone = pg.image.load("./Images/block icons/stone.png")
        dirt = pg.image.load("./Images/block icons/dirt.png")
        grass = pg.image.load("./Images/block icons/grass.png")
        sand = pg.image.load("./Images/block icons/sand.png")

        #takes coordinates from 0 to 20 on both axis
        def drawBlock(surface,blockType,position,skipCoordTranslation):

            #translate grid based input into screen cords
            if skipCoordTranslation == False:
                x = position[0] * 40
                y = position[1] * 40
            #draw block
            if skipCoordTranslation == True:
                x = math.floor(position[0]/40)
                x = x*40
                y = math.floor(position[1]/40)
                y= y*40

            surface.blit(blockType,(x,y))

class Character():
    global worldLength
    #things defined at top are used in many functions and subclasses
    characterLocation = [worldLength/2,19]
    characterDrawLocation = [400,400]

    #character images
    class Image():
        characterImage = pg.image.load("./Images/Character Icons/john.png")
        rightLegUpImage = pg.image.load("./Images/Character Icons/johnRightFoot.png")
        leftLegUpImage = pg.image.load("./Images/Character Icons/johnLeftFoot.png")
        bothLegsUpImage = pg.image.load("./Images/Character Icons/johnBothFeet.png")
        croutchedImage = pg.image.load("./Images/Character Icons/johnCroutched.png")

        #special conditions images (crouched during collision)
        rightLegUpCroutchedImage = pg.image.load("./Images/Character Icons/johnCroutchedRightFoot.png")
        leftLegUpCroutchedImage = pg.image.load("./Images/Character Icons/johnCroutchedLeftFoot.png")
        bothLegsUpCroutchedImage = pg.image.load("./Images/Character Icons/johnCroutchedBothFeet.png")

    class Pos():

        #moves the character left or right
        def update(moveAmount = 1):
            Character.characterDrawLocation[0] = Character.characterLocation[0]*40
            Character.characterDrawLocation[1] = (Character.characterLocation[1]*40)-360

        #checks for collisions in a specified position relative to the player and returns true or false
        def CollisionCheck(direction ,custom = False,xOffset = 0,yOffset = 0):
            if custom == False:
                if direction == "right":
                    if(Block.BlockMatrix[int(Character.characterLocation[1])-2][int(Character.characterLocation[0])+10] != Block.Type.BlockType.air):
                        return True
                elif direction == "left":
                    if(Block.BlockMatrix[int(Character.characterLocation[1])-2][int(Character.characterLocation[0])+10] != Block.Type.BlockType.air):
                        return True
                elif direction == "leftunder":
                    if(Block.BlockMatrix[int(Character.characterLocation[1])-2][int(Character.characterLocation[0])+9] != Block.Type.BlockType.air):
                        return True
                elif direction == "rightunder":
                    if(Block.BlockMatrix[int(Character.characterLocation[1])-2][int(Character.characterLocation[0])+11] != Block.Type.BlockType.air):
                        return True
                elif direction == "under":
                    if(Block.BlockMatrix[int(Character.characterLocation[1])-1][int(Character.characterLocation[0])+10] != Block.Type.BlockType.air):
                        return True
                else:
                    return False
            elif custom == True:
                if(Block.BlockMatrix[int(Character.characterLocation[1])-(yOffset+-8)][int(Character.characterLocation[0])+(xOffset+10)] != Block.Type.BlockType.air):
                    return True
                else:
                    return False
    class Render():

        def SpritePick(Croutched):
            #if elif statement used to set sprites under certian conditions
          if Character.Pos.CollisionCheck("rightunder") == None and Character.Pos.CollisionCheck("leftunder") == None: #sets default image if no blocks collide with legs
            if Croutched == False:
                return Character.Image.characterImage
            elif Croutched == True:
                return Character.Image.croutchedImage

          if Character.Pos.CollisionCheck("leftunder") == True and Character.Pos.CollisionCheck("rightunder") == True: #sets image for if both legs collide with blocks
              if Croutched == False:
                return Character.Image.bothLegsUpImage
              elif Croutched == True:
                return Character.Image.bothLegsUpCroutchedImage

          elif Character.Pos.CollisionCheck("rightunder") == True:
              if Croutched == False:
                return Character.Image.rightLegUpImage
              elif Croutched == True:
                return Character.Image.rightLegUpCroutchedImage

          elif Character.Pos.CollisionCheck("leftunder") == True:
              if Croutched == False:
                return Character.Image.leftLegUpImage
              elif Croutched == True:
                return Character.Image.leftLegUpCroutchedImage


        def draw(surface,imageIn,x,y):
        #renders the character still
            x = x * 40
            y = y * 40
            surface.blit(imageIn,(x,y))

        def drawStillX(surface,imageIn):
            surface.blit(imageIn,(325,Character.characterDrawLocation[1]))

         