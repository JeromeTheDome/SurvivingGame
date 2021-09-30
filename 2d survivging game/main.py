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
blockType = Block.Type.dirt

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
for i in range(100):
   Block.Grid.placeBlock((i,18),Block.Type.grass,True)
for i in range(100):
   Block.Grid.placeBlock((i,19),Block.Type.dirt,True)




#main game loop
while True:
  #gets pygame events
  ev = pg.event.get()
  keyboardInput = pg.key.get_pressed()
  pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))
  #START

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
    blockType = Block.Type.grass
  elif keyboardInput[pg.K_2]:
    blockType = Block.Type.dirt
  elif keyboardInput[pg.K_3]:
      blockType = Block.Type.stone
  elif keyboardInput[pg.K_4]:
    blockType = Block.Type.sand

  #checks mouse input
  if pg.mouse.get_pressed(3) == (True,False,False):
    Block.Grid.placeBlock((ForeGround.getMousePos()[0]+Character.characterDrawLocation[0],ForeGround.getMousePos()[1]),blockType)
  if pg.mouse.get_pressed(3) == (False,False,True):
    Block.Grid.placeBlock((ForeGround.getMousePos()[0]+Character.characterDrawLocation[0],ForeGround.getMousePos()[1]),Block.Type.air)



  #block rendering logic is to be placed at the bottom

  #places blocks
  for y in range(0,20):
        for x in range(0,99):
          if Block.BlockMatrix[y][x] != Block.Type.air and (x > (Character.characterLocation[0])-10 and x < (Character.characterLocation[0])+20):
              Block.Renderer.drawBlock(ForeGround.display,Block.BlockMatrix[y][x],(x-Character.characterLocation[0],y),False)

  #removes blocks
  for y in range(0,20):
        for x in range(0,99):
          if Block.BlockMatrix[y][x] != Block.Type.air and (x > (Character.characterLocation[0])-10 and x < (Character.characterLocation[0])+20):
              Block.Renderer.drawBlock(ForeGround.display,Block.Type.air,(x,y),False)

 

  """
  player logic
  """

  #player movement Logic
  #keyboard input
  if keyboardInput[pg.K_a]:
    Character.characterLocation[0] -= 1
    Character.Pos.update()

  elif keyboardInput[pg.K_d]:
    Character.characterLocation[0] += 1
    Character.Pos.update()

  #draw character at the end AFTER(DO NOT FORGOR💀) setting game logic for position
  Character.Render.drawStill(ForeGround.display,Character.characterImage)




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