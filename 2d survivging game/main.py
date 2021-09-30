import pygame
import time
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
scrollSpeed = 0
scrollDirection = 1
iterNum = 0

characterX = 10
characterY = 10

#inits backround and foreground
ForeGround.__init__(1)
Block.BlockGrid.__init__()

#defines background image
bgImage = BackGround.bgImage("/Users/jerth/source/repos/GameSolution/2d survivging game/Images/background images/cloud.png")

#main game loop
while True:
  #gets pygame events
  pg.event.get()
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
  
  #block rendering logic is to be placed at the bottom

  #draws row of blocks at the bottom
  for i in range(20):
    Block.BlockRenderer.drawBlock(ForeGround.display,Block.BlockType.sand,(i,20))

 

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
  any ending functions such as iteration numbers or updates of that kind
  """

  #number of times the while loop has run
  iterNum +=1

  #END
  #end of main loop. all code goes in between
  pg.display.flip()
  time.sleep(0.0033)
