import pygame
import time
import math
from gameWindow import ForeGround
from gameWindow import BackGround
from gameWindow import Block
from gameWindow import Character

"""
to do list:
make sand edible
"""

pg = pygame

#default values
moving = False
movingIter = 0

blockType = Block.Type.BlockType.dirt

characterImage = Character.Image.characterImage

worldLength = 99

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
   Block.Grid.placeBlock((i,18),Block.Type.BlockType.grass,True)
for i in range(worldLength):
   if i% 2 == 0:
       Block.Grid.placeBlock((i,19),Block.Type.BlockType.dirt,True)
   else:
       Block.Grid.placeBlock((i,19),Block.Type.BlockType.sand,True)




#main game loop
while True:
  #gets pygame events
  ev = pg.event.get()
  keyboardInput = pg.key.get_pressed()
  pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))
  #START

  #checks mouse input
  if pg.mouse.get_pressed(3) == (True,False,False):
    Block.Grid.placeBlock((ForeGround.getMousePos()[0]+Character.characterDrawLocation[0],ForeGround.getMousePos()[1]),blockType)
  if pg.mouse.get_pressed(3) == (False,False,True):
    Block.Grid.placeBlock((ForeGround.getMousePos()[0]+Character.characterDrawLocation[0],ForeGround.getMousePos()[1]),Block.Type.BlockType.air)

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
      

  #blockType logic
  if keyboardInput[pg.K_1]:
    blockType = Block.Type.BlockType.grass
  elif keyboardInput[pg.K_2]:
    blockType = Block.Type.BlockType.dirt
  elif keyboardInput[pg.K_3]:
      blockType = Block.Type.BlockType.stone
  elif keyboardInput[pg.K_4]:
    blockType = Block.Type.BlockType.sand




  #block rendering logic is to be placed at the bottom



  #renders placed blocks
  for y in range(0,20):
        for x in range(0,worldLength):
          if (x > (Character.characterLocation[0])-10 and x < (Character.characterLocation[0])+20) and Block.BlockMatrix[y][x] != Block.Type.BlockType.air:
              Block.Renderer.drawBlock(ForeGround.display,Block.Type.List[Block.BlockMatrix[y][x]],(x-Character.characterLocation[0],y),False)

 

  """
  player logic
  """

    #player movement Logic

  
  
  if moving == False:
    characterImage = Character.Render.SpritePick(croutched)

  #keyboard input
  #move left
  if keyboardInput[pg.K_a] and Character.characterLocation[0] >= -8:
    movingIter += 1
    moving = True
    doMove1 = True
    for i in range(11-int(19-Character.characterLocation[1]),18-int(19-Character.characterLocation[1])):
        if Character.Pos.CollisionCheck(None,True,-2,i):
            doMove1 = False
    #updates player pos
    if iterNum%5 == 0 and doMove1 == True:
        Character.characterLocation[0] -= 1
        if Character.Pos.CollisionCheck("right") == True:
            Character.characterLocation[1] -= 1
    if Character.Pos.CollisionCheck("under") != True:
      Character.characterLocation[1] += 1
    Character.Pos.update()
    #animates legs
    if movingIter>=0:
      characterImage = Character.Image.leftLegUpImage
    if movingIter >=25:
        characterImage = Character.Image.rightLegUpImage
        if movingIter >= 50:
            movingIter = 0

    #move right
  elif keyboardInput[pg.K_d] and Character.characterLocation[0] <= 87:
    movingIter += 1
    moving = True
    doMove = True
    for i in range(11-int(19-Character.characterLocation[1]),18-int(19-Character.characterLocation[1])):
        if Character.Pos.CollisionCheck(None,True,2,i):
            doMove = False
    #updates player pos
    if iterNum%5 == 0 and doMove == True:
        Character.characterLocation[0] += 1
        if Character.Pos.CollisionCheck("left") == True:
            Character.characterLocation[1] -= 1
    if Character.Pos.CollisionCheck("under") != True:
      Character.characterLocation[1] += 1
    #animates legs
    if movingIter >=0:
      characterImage = Character.Image.leftLegUpImage
    if movingIter>=25:
        characterImage = Character.Image.rightLegUpImage
        if movingIter >= 50:
            movingIter = 0

  else:
       moving = False


  if keyboardInput[pg.K_s] and moving == False:
      croutched = True
  else:
      croutched = False
  Character.Pos.update()
  #draw character at the end AFTER(DO NOT FORGOR💀) setting game logic for position
  Character.Render.drawStillX(ForeGround.display,characterImage)




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