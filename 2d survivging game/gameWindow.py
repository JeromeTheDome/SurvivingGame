import pygame

pg = pygame

class ForeGround():
  #inits the pygame window
  def __init__(self):
    pg.init()
    ForeGround.display = pg.display.set_mode((800,800))
  def getMousePos():
   mousePos = [pg.mouse.get_pos()[0], pg.mouse.get_pos()[1]]

class BackGround():

    bgImage = pg.image.load
    Surface = pg.Surface((800,800))

    #used to put background on display surface and scroll it
    def BlitToSurface(surface,image,X):
        global bgImage
        X = X*15
        surface.blit(image,(X,0))


class Block():

    #all of these are defined at the top as many subclasses of block rely on them

    #defines air for default block type
    air = pg.image.load("C:/Users/jerth/source/repos/GameSolution/2d survivging game/Images/block icons/air.png")

    #list variable for storing block data. structure is BlockMatrix[Horizontal Columns(uses y input)][Block in column(uses x input)][blockType]
    BlockMatrix = [[[]for i in range(40)]for i in range(40)]

    #sets every block to air
    for y in range(40):
        for x in range(40):
            BlockMatrix[y][x] = air

    


    #start of subclasses
    class BlockType():

            air = pg.image.load("C:/Users/jerth/source/repos/GameSolution/2d survivging game/Images/block icons/air.png")
            stone = None
            dirt = None
            grass = None
            sand = pg.image.load("C:/Users/jerth/source/repos/GameSolution/2d survivging game/Images/block icons/sand.png")


    class BlockGrid():

        #inits the BlockGrid
        def __init__():
            print("")



    class BlockRenderer():
        
        air = pg.image.load("C:/Users/jerth/source/repos/GameSolution/2d survivging game/Images/block icons/air.png")
        stone = pg.image.load("C:/Users/jerth/source/repos/GameSolution/2d survivging game/Images/block icons/sand.png")
        dirt = pg.image.load("C:/Users/jerth/source/repos/GameSolution/2d survivging game/Images/block icons/sand.png")
        grass = pg.image.load("C:/Users/jerth/source/repos/GameSolution/2d survivging game/Images/block icons/sand.png")
        sand = pg.image.load("C:/Users/jerth/source/repos/GameSolution/2d survivging game/Images/block icons/sand.png")

        #takes coordinates from 0 to 20 on both axis
        def drawBlock(surface,blockType,position):

            #translate grid based input into screen cords
            if position[0] >= 20:
               x = 760
            else:
                x = position[0] * 40
            if position[1] >= 20:
                y = 760
            else:
                y = position[1] * 40
            #draw block
            surface.blit(blockType,(x,y))

            #set index of coordinates to 
            Block.BlockMatrix[position[1]][position[0]] = blockType

class Character():
    #things defined at top are used in many functions and subclasses
    characterLocation = [400,440]
    characterImage = pg.image.load("C:/Users/jerth/source/repos/GameSolution/2d survivging game/Images/Character Icons/John.png")
    class Move():

        #moves the character left or right
        def Left(moveSpeed):
            Character.characterLocation[0]-= moveSpeed + 2
        def Right(moveSpeed):
            Character.characterLocation[0]+=moveSpeed
    class Render():

        def still(surface,imageIn):
        #renders the character still
            surface.blit(imageIn,(Character.characterLocation[0],Character.characterLocation[1]))
         