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
#screen scroll values
scrollSpeed = 0
scrollDirection = 1
#checks for iterations against a modulo operator. used for screens croll
iterNum = 0
#turns true for that frame if the player clicked on a square
placeBlockAtEnd = False

characterX = 10
characterY = 10

#inits backround and foreground
ForeGround.__init__(1)

#defines background image
bgImage = BackGround.bgImage("/Users/jerth/source/repos/GameSolution/2d survivging game/Images/background images/cloud.png")

#main game loop
while True:
  #gets pygame events
  ev = pg.event.get()
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


  #iterates through all events processed that frame and checks if event pg.MOUSEBUTTONDOWN occured

  if pg.mouse.get_pressed(3) == (True,False,False):
    Block.Grid.placeBlock((ForeGround.getMousePos()[0],ForeGround.getMousePos()[1]),Block.Type.sand)
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
  keyboardInput = pg.key.get_pressed()
  if keyboardInput[pg.K_a]:
    Character.Move.Left(3)

  elif keyboardInput[pg.K_d]:
    Character.Move.Right(5)

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