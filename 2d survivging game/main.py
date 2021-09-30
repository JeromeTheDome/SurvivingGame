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
!move block logic update function ouside of block renderer class!
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

#main game loop
while True:
  #gets pygame events
  ev = pg.event.get()
  keyboardInput = pg.key.get_pressed()
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
  elif keyboardInput[pg.K_4]:
    blockType = Block.Type.sand

  #checks mouse input
  if pg.mouse.get_pressed(3) == (True,False,False):
    Block.Grid.placeBlock((ForeGround.getMousePos()[0],ForeGround.getMousePos()[1]),blockType)
  if pg.mouse.get_pressed(3) == (False,False,True):
    Block.Grid.placeBlock((ForeGround.getMousePos()[0],ForeGround.getMousePos()[1]),Block.Type.air)

  #for event in ev:
    #if event.type == pg.MOUSEBUTTONDOWN:
       # Block.Grid.placeBlock((ForeGround.getMousePos()[0],ForeGround.getMousePos()[1]),Block.Type.sand)

  #block rendering logic is to be placed at the bottom

  #places blocks
  for y in range(0,19):
        for x in range(0,19):
          if Block.BlockMatrix[y][x] != Block.Type.air:
              Block.Renderer.drawBlock(ForeGround.display,Block.BlockMatrix[y][x],(x,y),False)

  #removes blocks
  for y in range(0,19):
        for x in range(0,19):
          if Block.BlockMatrix[y][x] != Block.Type.air:
              Block.Renderer.drawBlock(ForeGround.display,Block.Type.air,(x,y),False)


  #draws row of blocks at the bottom
  for i in range(20):
    Block.Renderer.drawBlock(ForeGround.display,Block.Type.sand,(i,20),False)

 

  """
  player logic
  """

  #player movement Logic
  if keyboardInput[pg.K_a]:
    Character.Move.Left()
    #Block.Grid.shiftBlockMatrix()

  elif keyboardInput[pg.K_d]:
    #Character.Move.Right()
    Block.Grid.shiftBlockMatrix((Character.characterLocation[0])-10,(Character.characterLocation[0])+10)
    #draw character at the end AFTER(DO NOT FORGOR💀) setting game logic for position
  Character.Render.still(ForeGround.display,Character.characterImage)


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
  time.sleep(0.000033)