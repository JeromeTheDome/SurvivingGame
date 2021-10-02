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
"""
notes: 
make seperate gravity loop for when the player is moving that checks the players next coord for air and then moves them down
"""

pg = pygame

#default values
direction = "right"

jump = False
jumpIterNum = 0

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
for i in range(worldLength):
    for g in range(1,500):
       Block.Grid.placeBlock((i,500 + g),Block.Type.BlockType.dirt,True)





#main game loop
while True:
  #gets pygame events
  print('x',Character.characterLocation[0])
  print('y',Character.characterLocation[1])

  ev = pg.event.get()
  keyboardInput = pg.key.get_pressed()
  pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))
  #START

  #checks mouse input
  if pg.mouse.get_pressed(3) == (True,False,False):
    Block.Grid.placeBlock((ForeGround.getMousePos()[0]+Character.characterDrawLocation[0],  (ForeGround.getMousePos()[1]+Character.characterDrawLocation[1])-600),blockType)
  if pg.mouse.get_pressed(3) == (False,False,True):
    Block.Grid.placeBlock((ForeGround.getMousePos()[0]+Character.characterDrawLocation[0], (ForeGround.getMousePos()[1]+Character.characterDrawLocation[1])-600), Block.Type.BlockType.air)

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
  elif keyboardInput[pg.K_5]:
    blockType = Block.Type.BlockType.wood




  #block rendering logic is to be placed at the bottom



  #renders placed blocks
  for y in range(math.floor(Character.characterLocation[1]-20),math.floor(Character.characterLocation[1]+7)):
        for x in range(math.floor(Character.characterLocation[0]),math.floor(Character.characterLocation[0]+26)): 
             #checks if block attempting to be drawn is outside of view distance
             Block.Renderer.drawBlock(ForeGround.display  ,Block.Type.List[Block.BlockMatrix[y][x]],(x-Character.characterLocation[0],(y-Character.characterLocation[1])+19),False)

 

  """
  player logic
  """


  if jump == True:
      if jumpIterNum < 5:
        Character.characterLocation[1]-= 0.5
        jumpIterNum += 1
        if Character.Pos.CollisionCheck("under",False,1) == True:
            jumpIterNum = 14
      elif  5 <= jumpIterNum < 7:
        Character.characterLocation[1]-= 0.08
        jumpIterNum += 1
        if Character.Pos.CollisionCheck("under",False,1) == True:
            jumpIterNum = 14
      elif 7 <= jumpIterNum < 9:
        Character.characterLocation[1]+= 0.08
        jumpIterNum += 1
        if Character.Pos.CollisionCheck("under",False,1) == True:
            jumpIterNum = 14
      elif 9 <= jumpIterNum < 14:
        Character.characterLocation[1]+= 0.5
        jumpIterNum += 1
        if Character.Pos.CollisionCheck("under",False,1) == True:
            jumpIterNum = 14
      elif jumpIterNum >= 14:
        jump = False
        jumpIterNum = 0

    #gravity
  if Character.Pos.CollisionCheck("under",False,1) != True and jump != True and direction == 'right' and Character.characterLocation[1] < 900:
      Character.characterLocation[1] += 0.5
  if Character.Pos.CollisionCheck("under",False,2) != True and jump != True and direction == 'left' and Character.characterLocation[1] < 900:
      Character.characterLocation[1] += 0.5

  #keyboard input

  if keyboardInput[pg.K_SPACE]:
    if Character.Pos.CollisionCheck("under",False,1) == True:
        jump = True

  #move left
  if keyboardInput[pg.K_a]:
    moving = True
    doMove1 = True
    direction = "left"
    #checks for player collisions with adjacent blocks
    if Character.Pos.CollisionCheck("left",False,-1,-1) or Character.characterLocation[0] < 20:
            doMove1 = False
    #updates player pos
    if doMove1 == True:
        if Character.Pos.CollisionCheck("left",False,-1,0) == True and iterNum%3 == 0 and Character.Pos.CollisionCheck('above',False) != True:
            Character.characterLocation[1] -= 1
            Character.characterLocation[0] -= 1
        elif Character.Pos.CollisionCheck("left",False,-1,0) != True:
            Character.characterLocation[0] -= 0.3
    Character.Pos.update()
    #decides what animation to use for the character
    if moving == True and iterNum%4 == 0:
        characterImage = Character.Render.SpritePick(direction,movingIter)
        if movingIter >= 4:
            movingIter = 1
        else:
            movingIter+= 1


    #move right
  elif keyboardInput[pg.K_d]:
    moving = True
    doMove = True
    direction = "right"
    #checks for player collisions with adjacent blocks
    if Character.Pos.CollisionCheck("right",False,2,-1) or Character.characterLocation[0] > 950:
            doMove = False    
    #updates player pos
    if doMove == True:
        if Character.Pos.CollisionCheck("right",False,2,0) == True and iterNum%3 == 0 and Character.Pos.CollisionCheck('above',False) != True:
            Character.characterLocation[1] -= 1
            Character.characterLocation[0] += 1
        elif Character.Pos.CollisionCheck("right",False,2,0) != True:
            Character.characterLocation[0] += 0.3
    #decides what animation to use for the character
    if moving == True and iterNum%4 == 0:
        characterImage = Character.Render.SpritePick(direction,movingIter)
        if movingIter >= 4:
            movingIter = 1
        else:
            movingIter+= 1


  else:
       moving = False
       if direction == "right":
        characterImage = Character.Image.characterStillRight
       elif direction == "left":
        characterImage = Character.Image.characterStillLeft
       movingIter = 1


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