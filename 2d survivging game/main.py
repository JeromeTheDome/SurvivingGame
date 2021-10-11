import pygame
import time
import math
from gameWindow import ForeGround
from gameWindow import BackGround
from gameWindow import Block
from CharacterFile import Character

"""
to do list:
make sand edible
make tools
"""
"""
notes: 
tools will act as a fractional multiplier to the break speed variable causing the time to break to go down when a given tool is equipped
"""

pg = pygame

#default values
direction = "right"
animationSpeed = 4
playerSpeed = 0.3

jump = False
jumpIterNum = 0
yVelocity = 0

blockBreakNumber = 1
blockBreakSpeed = 15

blockSize = 32
numBlocks = int(800 / blockSize)
worldHeight = 1000
worldLength = 1000

moving = False
movingIter = 1

blockType = Block.Type.BlockType.dirt

characterImage = Character.Image.characterStillRight
croutched = False

#screen scroll values
scrollSpeed = 0
scrollDirection = 1

#checks for iterations against a modulo operator. used for screens croll
iterNum = 0

characterX = 10
characterY = 10

#inits backround and foreground
ForeGround.__init__(1)

#defines background image
bgImage = BackGround.bgImage("./Images/background images/cloud.png")

#sets up bottom squares
for i in range(worldLength):
   Block.Grid.placeBlock((i,500),Block.Type.BlockType.grass,True)
   Block.Grid.placeBlock((i,501),Block.Type.BlockType.dirt,True)
   Block.Grid.placeBlock((i,502),Block.Type.BlockType.dirt,True)
   Block.Grid.placeBlock((i,503),Block.Type.BlockType.dirt,True)
   Block.Grid.placeBlock((i,504),Block.Type.BlockType.dirt,True)
   Block.Grid.placeBlock((i,505),Block.Type.BlockType.dirt,True)
for i in range(worldLength):
    for g in range(5,500):
       Block.Grid.placeBlock((i,500 + g),Block.Type.BlockType.stone,True)


#main game loop
while True:
  #gets pygame events
  ev = pg.event.get()
  keyboardInput = pg.key.get_pressed()
  pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))
  #START

  #checks mouse input
  if pg.mouse.get_pressed(3) == (True,False,False):
    Block.Grid.placeBlock((ForeGround.getMousePos()[0],ForeGround.getMousePos()[1]),Character.Input.blockType)
  if pg.mouse.get_pressed(3) == (False,False,True):
    Block.Grid.SetBlockBreakCoord((ForeGround.getMousePos()[0]+Character.characterDrawLocation[0], (ForeGround.getMousePos()[1]+Character.characterDrawLocation[1])-600))

    if Block.Grid.getBlockAtLocation(Block.Grid.blockBreakingPos) == Block.Type.BlockType.dirt:
        blockBreakSpeed = 10
    elif Block.Grid.getBlockAtLocation(Block.Grid.blockBreakingPos) == Block.Type.BlockType.grass:
        blockBreakSpeed = 20
    elif Block.Grid.getBlockAtLocation(Block.Grid.blockBreakingPos) == Block.Type.BlockType.sand:
        blockBreakSpeed = 20
    if Block.Grid.getBlockAtLocation(Block.Grid.blockBreakingPos) == Block.Type.BlockType.stone:
        blockBreakSpeed = 50
    else:
        blockBreakSpeed = 20

    if iterNum%blockBreakSpeed == 0:
       blockBreakNumber += 1
    if blockBreakNumber%6 == 0:
        Block.Grid.breakBlock((ForeGround.getMousePos()[0],ForeGround.getMousePos()[1]))
        blockBreakNumber = 1
  else:
    blockBreakNumber = 1

  """
  visual screen logic(background, screen scrolling ect.)
  """


  #draws background image
  BackGround.BlitToSurface(ForeGround.display,bgImage,scrollSpeed-4)

  #logic for setting the x value of the background to make it scroll 
  if scrollDirection == 0 and iterNum%50 == 0:
    scrollSpeed += 1
  elif scrollDirection == 1 and iterNum%50 == 0:
    scrollSpeed -= 1

  if scrollSpeed <= -4:
      scrollDirection = 0
  if scrollSpeed >= 4:
      scrollDirection = 1




  """
  block placement and properties logic
  """
  #grid matrix logic at top

  
#block rendering logic is to be placed at the bottom

  Block.Renderer.drawBlocksOnScreen()
       
  Block.Renderer.drawBreakingOverlay(blockBreakNumber)
             
  #ForeGround.display.blit(pg.image.load("./Images/block icons/breakingOverlays/stage1.png"),((math.floor(ForeGround.getMousePos()[0]/blockSize)+Character.characterLocation[0]%1)*blockSize,(math.floor(ForeGround.getMousePos()[1]/blockSize)+Character.characterLocation[1]%1)*blockSize))
  """
  player logic
  """

    

  

  yVelocity += 0.2

  if yVelocity > 1:
      yVelocity = 1

  if Character.Pos.CollisionCheck("under",False,1) == True:
      yVelocity = 0

  print(yVelocity)

  #keyboard input

  for event in ev:
     if event.type == pg.KEYDOWN:
        if keyboardInput[pg.K_SPACE]:
            if Character.Pos.CollisionCheck("under",False,1) == True:
                yVelocity -= 1


  Character.Input.inputKey(keyboardInput,iterNum)

  Character.Pos.update()
  #draw character at the end AFTER(DO NOT FORGOR💀) setting game logic for position
  Character.Render.drawStillX(ForeGround.display,Character.characterImage)

  Character.characterLocation[1] += yVelocity


  """
  any ending functions such as iteration numbers or updates of that kind or misc renderings
  """

  #draws cursor with block where player cursor is
  ForeGround.display.blit(ForeGround.cursorIcon,(ForeGround.getMousePos()[0]-12,ForeGround.getMousePos()[1]-9))

  #number of times the while loop has run
  iterNum +=1

  #END
  #end of main loop. all code goes in between
  pg.display.flip()