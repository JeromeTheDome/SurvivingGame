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
    Block.Grid.placeBlock((ForeGround.getMousePos()[0]+Character.characterDrawLocation[0],  (ForeGround.getMousePos()[1]+Character.characterDrawLocation[1])-600),blockType)
  if pg.mouse.get_pressed(3) == (False,False,True):
    Block.Grid.SetBlockBreakCoord((ForeGround.getMousePos()[0]+Character.characterDrawLocation[0], (ForeGround.getMousePos()[1]+Character.characterDrawLocation[1])-600))

    if Block.Grid.getBlockAtLocation(Block.Grid.blockBreakingPos) == Block.Type.BlockType.dirt:
        blockBreakSpeed = 15
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
        Block.Grid.breakBlock((ForeGround.getMousePos()[0]+Character.characterDrawLocation[0], (ForeGround.getMousePos()[1]+Character.characterDrawLocation[1])-600), Block.Type.BlockType.air)
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
             Block.Renderer.drawBlock(ForeGround.display,Block.Type.List[Block.BlockMatrix[y][x]],(x-Character.characterLocation[0],(y-Character.characterLocation[1])+19),False)
         
  x1 = math.floor(ForeGround.getMousePos()[0]/blockSize)
  x1+= math.floor(Character.characterLocation[0])
  y1 = math.floor(ForeGround.getMousePos()[1]/blockSize)
  y1+= math.floor(Character.characterLocation[1])

  if blockBreakNumber > 1 and Block.Grid.getBlockAtLocation((Block.Grid.blockBreakingPos[0],Block.Grid.blockBreakingPos[1])) != Block.Type.BlockType.air:
    Block.Renderer.drawBlock(ForeGround.display,pg.image.load("./Images/block icons/breakingOverlays/stage"+str(blockBreakNumber)+".png"),(Block.Grid.blockBreakingPos[0]-Character.characterLocation[0],(Block.Grid.blockBreakingPos[1]-Character.characterLocation[1])+19),False)
             
  #ForeGround.display.blit(pg.image.load("./Images/block icons/breakingOverlays/stage1.png"),((math.floor(ForeGround.getMousePos()[0]/blockSize)+Character.characterLocation[0]%1)*blockSize,(math.floor(ForeGround.getMousePos()[1]/blockSize)+Character.characterLocation[1]%1)*blockSize))
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
  if keyboardInput[pg.K_LSHIFT]:
      playerSpeed =  0.4
      animationSpeed = 2
  else:
      playerSpeed = 0.3
      animationSpeed = 4


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
            Character.characterLocation[0] -= playerSpeed
    Character.Pos.update()
    #decides what animation to use for the character
    if moving == True and iterNum%animationSpeed == 0:
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
            Character.characterLocation[0] += playerSpeed
    #decides what animation to use for the character
    if moving == True and iterNum%animationSpeed == 0:
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