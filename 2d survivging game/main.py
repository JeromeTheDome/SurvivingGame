import pygame
import time
import math
from gameWindow import ForeGround
from gameWindow import BackGround
from gameWindow import Block
from CharacterFile import Character
from inventory import Inventory
from itemIds import Items
from pygame.locals import *
from entity import Entity
import noise
import random

"""
to do list:
make sand edible
"""
"""
notes: 
"""

pg = pygame
pygame.font.init()

#inits

#default values
inventoryBackGround = pg.image.load("./Images/hud/openInventoryBackground.png").convert()
entities = []

selectedBox = None

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

myfont = pygame.font.SysFont('Comic Sans MS', 18)

#screen scroll values
scrollSpeed = 0
scrollDirection = 1

#checks for iterations against a modulo operator. used for screens croll
iterNum = 0

characterX = 10
characterY = 10

#defines background image
bgImage = BackGround.bgImage("./Images/background images/cloud.png").convert()

#sets up bottom squares
seed = random.randint(0,500)

for x in range(worldLength):
    for y in range(10,500):
       if not(0.135 <= noise.snoise2((x+seed)*0.07,(y+seed)*0.07,repeaty=999999,repeatx=999999,octaves = 1,persistence=1,lacunarity=10) <= 0.7):
        Block.Grid.placeBlock((x,500 + y),Block.Type.BlockType.stone,True)
        Block.Grid.placeBlockBg((x,500 + y),Block.Type.BlockType.stone,True)
       else:
           Block.Grid.placeBlockBg((x,500 + y),Block.Type.BlockType.stone,True)


for x in range(worldLength):
    frequency = 0.2

    treeTrue = random.randint(0,10)

    y =  int(noise.pnoise1((x+seed)*0.07,repeat=999999999)*5)+495

    if x == 500:
        Character.characterLocation[1] = y-2


    if treeTrue == 5:
        Block.Grid.placeBlockBg((x,y-1),Block.Type.BlockType.log,True)
        Block.Grid.placeBlockBg((x,y-2),Block.Type.BlockType.log,True)
        Block.Grid.placeBlockBg((x,y-3),Block.Type.BlockType.log,True)
        Block.Grid.placeBlockBg((x,y-4),Block.Type.BlockType.log,True)

        #first row of leaves
        Block.Grid.placeBlockBg((x-1,y-5),Block.Type.BlockType.leaves,True)
        Block.Grid.placeBlockBg((x-2,y-5),Block.Type.BlockType.leaves,True)
        Block.Grid.placeBlockBg((x,y-5),Block.Type.BlockType.leaves,True)
        Block.Grid.placeBlockBg((x+1,y-5),Block.Type.BlockType.leaves,True)
        Block.Grid.placeBlockBg((x+2,y-5),Block.Type.BlockType.leaves,True)
        #second row
        Block.Grid.placeBlockBg((x-1,y-6),Block.Type.BlockType.leaves,True)
        Block.Grid.placeBlockBg((x-2,y-6),Block.Type.BlockType.leaves,True)
        Block.Grid.placeBlockBg((x,y-6),Block.Type.BlockType.leaves,True)
        Block.Grid.placeBlockBg((x+1,y-6),Block.Type.BlockType.leaves,True)
        Block.Grid.placeBlockBg((x+2,y-6),Block.Type.BlockType.leaves,True)
        #third row
        Block.Grid.placeBlockBg((x-1,y-7),Block.Type.BlockType.leaves,True)
        Block.Grid.placeBlockBg((x,y-7),Block.Type.BlockType.leaves,True)
        Block.Grid.placeBlockBg((x+1,y-7),Block.Type.BlockType.leaves,True)

        for i in range(random.randint(5,7)):
            pass
            #Block.Grid.placeBlock((x,y-i),Block.Type.BlockType.log,True)

    Block.Grid.placeBlock((x,y),Block.Type.BlockType.grass,True)
    Block.Grid.placeBlock((x,y+1),Block.Type.BlockType.dirt,True)
    Block.Grid.placeBlock((x,y+2),Block.Type.BlockType.dirt,True)
    Block.Grid.placeBlock((x,y+3),Block.Type.BlockType.dirt,True)
    Block.Grid.placeBlock((x,y+4),Block.Type.BlockType.dirt,True)


    for y in range(y,510):
       if not(0 <= noise.snoise2(x*0.07,y*0.07,repeaty=999999,repeatx=999999,octaves = 1,persistence=1) <= 0.6):
        Block.Grid.placeBlock((x,y),Block.Type.BlockType.dirt,True)
       Block.Grid.placeBlockBg((x,y),Block.Type.BlockType.dirt,True)



Inventory.grid[0][0] = Items.Id.defaultPick
Inventory.stackAmount[0][0] = 1
Inventory.grid[0][1] = Items.Id.defaultAxe
Inventory.stackAmount[0][1] = 1
Inventory.grid[0][2] = Items.Id.defaultShovel
Inventory.stackAmount[0][2] = 1

def deleteEnt(index,entites):
	if len(entities) > index:
		if len(entities) > 0:
			entities[index].deleteEntity(index)
		del entities[index]

clock = pygame.time.Clock()
#main game loop
while True:
  #gets pygame events
  ev = pg.event.get()
  keyboardInput = pg.key.get_pressed()
  pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))
  #START

  #checks mouse input
  if pg.mouse.get_pressed(3) == (False,False,True):

    if Inventory.open == False:
        ySize = 48
        for i in range(9):
         if math.floor(ForeGround.getMousePos()[0]/48) == i and math.floor(ForeGround.getMousePos()[1]/48) == 0:
              Inventory.selectedSlot = i
    elif Inventory.open == True:
        ySize = 240
        for y in range(5):
            for x in range(9):
                if math.floor(ForeGround.getMousePos()[0]/48) == x and math.floor(ForeGround.getMousePos()[1]/48) == y:

                    for event in ev:
                        if event.type == pygame.MOUSEBUTTONDOWN:

                            if Inventory.itemOnCursor != Items.Id.empty and Inventory.grid[y][x] != Items.Id.empty:
                                temporaryItem = Inventory.itemOnCursor
                                temporaryItemCount = Inventory.itemCountOnCursor

                                Inventory.itemOnCursor = Inventory.grid[y][x]
                                Inventory.itemCountOnCursor = Inventory.stackAmount[y][x]

                                Inventory.grid[y][x] = temporaryItem
                                Inventory.stackAmount[y][x] = temporaryItemCount

                            elif Inventory.itemOnCursor == Items.Id.empty:
                                Inventory.itemOnCursor = Inventory.grid[y][x]
                                Inventory.itemCountOnCursor = Inventory.stackAmount[y][x]

                                Inventory.grid[y][x] = Items.Id.empty
                                Inventory.stackAmount[y][x] = 0

                            elif Inventory.itemOnCursor != Items.Id.empty:
                                Inventory.grid[y][x] = Inventory.itemOnCursor
                                Inventory.stackAmount[y][x] = Inventory.itemCountOnCursor

                                Inventory.itemOnCursor = Items.Id.empty
                                Inventory.itemCountOnCursor = 0

              
      
    if Inventory.selectedSlot != None and (ForeGround.getMousePos()[0] > 432 or ForeGround.getMousePos()[1] > ySize) and 1 <= Inventory.grid[0][Inventory.selectedSlot] <= 50:
        if Inventory.stackAmount[0][Inventory.selectedSlot] <= 0:
            Inventory.grid[0][Inventory.selectedSlot] = Items.Id.empty
            Inventory.stackAmount[0][Inventory.selectedSlot] = 0

        elif Block.Grid.getBlockAtLocation((ForeGround.getMousePos()[0],ForeGround.getMousePos()[1])) == Block.Type.BlockType.air:
            Inventory.stackAmount[0][Inventory.selectedSlot] -= 1
        Block.Grid.placeBlock((ForeGround.getMousePos()[0],ForeGround.getMousePos()[1]),Inventory.grid[0][Inventory.selectedSlot])

  #right click
  if pg.mouse.get_pressed(3) == (True,False,False):

    if 224 < ForeGround.getMousePos()[0] < 576 and 352 < ForeGround.getMousePos()[1] < 736:
        if Block.Grid.blockBreakingPos != Block.Grid.blockBreakingPosLast:
           blockBreakNumber = 1

        Block.Grid.SetBlockBreakCoord((ForeGround.getMousePos()[0]+Character.characterDrawLocation[0], (ForeGround.getMousePos()[1]+Character.characterDrawLocation[1])-600))

        blockBreakSpeed = Block.Type.determineBreakingSpeed()
        if Block.Grid.getBlockAtLocation2(Block.Grid.blockBreakingPos) == Block.Type.BlockType.air:
                blockBreakNumber = 1

        if iterNum%blockBreakSpeed == 0:
           blockBreakNumber += 1
        if blockBreakNumber%6 == 0:
            Inventory.addItem(Block.Grid.getBlockAtLocation2(Block.Grid.blockBreakingPos))
            Block.Grid.breakBlock((ForeGround.getMousePos()[0],ForeGround.getMousePos()[1]),1)
            blockBreakNumber = 1
  else:
        blockBreakNumber = 1    
  if pg.mouse.get_pressed(3) == (True,False,False):

    if 224 < ForeGround.getMousePos()[0] < 576 and 352 < ForeGround.getMousePos()[1] < 736:
        if Block.Grid.blockBreakingPos != Block.Grid.blockBreakingPosLast:
           blockBreakNumber = 1

        Block.Grid.SetBlockBreakCoord((ForeGround.getMousePos()[0]+Character.characterDrawLocation[0], (ForeGround.getMousePos()[1]+Character.characterDrawLocation[1])-600))

        blockBreakSpeed = Block.Type.determineBreakingSpeed()
        if Block.Grid.getBlockAtLocation2(Block.Grid.blockBreakingPos) == Block.Type.BlockType.air:
                blockBreakNumber = 1

        if iterNum%blockBreakSpeed == 0:
           blockBreakNumber += 1
        if blockBreakNumber%6 == 0:
            Inventory.addItem(Block.Grid.getBlockAtLocation2(Block.Grid.blockBreakingPos))
            Block.Grid.breakBlock((ForeGround.getMousePos()[0],ForeGround.getMousePos()[1]),1)
            blockBreakNumber = 1
  else:
        blockBreakNumber = 1   

  if pg.mouse.get_pressed(3) == (False,True,False) and Inventory.selectedSlot != None and Block.Grid.getBlockAtLocation((ForeGround.getMousePos()[0],ForeGround.getMousePos()[1])) != Block.Type.BlockType.air:
      Inventory.grid[0][Inventory.selectedSlot] = Block.Grid.getBlockAtLocation((ForeGround.getMousePos()[0],ForeGround.getMousePos()[1]))
  

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
             
  """
  player logic
  """
  if Character.characterLocation[1]%1 != 0 and yVelocity == 0:
      Character.characterLocation[1] = math.floor(Character.characterLocation[1])

  

  yVelocity += 0.2

  if yVelocity > 1:
      yVelocity = 1

  if Character.Pos.CollisionCheck("under",False,1,-2) == True and Character.Input.direction == "right":
      yVelocity = 0

  if Character.Pos.CollisionCheck("under",False,1) == True and Character.Input.direction == "right":
      yVelocity = 0
  if Character.Pos.CollisionCheck("under",False,2) == True and Character.Input.direction == "left":
      yVelocity = 0

  #keyboard input

  #for event in ev:
     #if event.type == pg.KEYDOWN:
  for event in ev:
     if event.type == pg.KEYDOWN:
        if keyboardInput[pg.K_TAB]:
            Inventory.open = not Inventory.open
     if keyboardInput[pg.K_SPACE]:
        if Character.Pos.CollisionCheck("under",False,1) == True:
         yVelocity -= 0.5
         print(yVelocity)
            

  if Character.Pos.CollisionCheck("under",False,1,-3) == True and Character.Input.direction == "right":
      if yVelocity < 0:
        yVelocity = 0
  if Character.Pos.CollisionCheck("under",False,2,-3) == True and Character.Input.direction == "left":
      if yVelocity < 0:
        yVelocity = 0

  Character.Input.inputKey(keyboardInput,iterNum,entities)

  Character.Pos.update()
  #draw character at the end AFTER(DO NOT FORGOR💀) setting game logic for position
  Character.Render.drawStillX(ForeGround.display,Character.characterImage)

  Character.characterLocation[1] += yVelocity

  """
  hud/inventory code
  """

  if Inventory.selectedSlot != None and Inventory.stackAmount[0][Inventory.selectedSlot] <= 0:
    Inventory.grid[0][Inventory.selectedSlot] = Items.Id.empty
    Inventory.stackAmount[0][Inventory.selectedSlot] = 0

  #hud rendering code
  if Inventory.open == True:
      ForeGround.display.blit(inventoryBackGround,(0,0))
      for y in range(1,5):
        for x in range(9):
                Inventory.Render.renderBox(((x*48),(y*48)),Inventory.grid[y][x])
                ForeGround.display.blit(myfont.render(str(Inventory.stackAmount[y][x]), False, (150, 150, 150)),(x*48+30,y*48+24))

  for i in range(9):
    if i == Inventory.selectedSlot:
        Inventory.Render.renderBox(((i*48),1),Inventory.grid[0][i],True)
        ForeGround.display.blit(myfont.render(str(Inventory.stackAmount[0][i]), False, (150, 150, 150)),(i*48+30,25))
    else:
        Inventory.Render.renderBox(((i*48),1),Inventory.grid[0][i])
        ForeGround.display.blit(myfont.render(str(Inventory.stackAmount[0][i]), False, (150, 150, 150)),(i*48+30,25))

  

  """
  entity logic
  """
  for i in range(len(entities)):
    try:
        ForeGround.display.blit(Items.iconList[entities[i].id],(entities[i].drawCoordinates))
        entities[i].update()
        entities[i].gravityUpdate()

        if Character.characterBoundingBox.colliderect(entities[i].boundingBox):
          Inventory.addItem(entities[i].id)
          deleteEnt(i,entities)
    except:
        pass

  for event in ev:
     if event.type == pg.KEYDOWN:
        if keyboardInput[pg.K_q]:
              Inventory.dropItem(Inventory.selectedSlot,entities)



  """
  any ending functions such as iteration numbers or updates of that kind or misc renderings
  """

  #draws cursor with block where player cursor is
  ForeGround.display.blit(ForeGround.cursorIcon,(ForeGround.getMousePos()[0]-12,ForeGround.getMousePos()[1]-9))
  ForeGround.display.blit(Items.iconList[Inventory.itemOnCursor],(ForeGround.getMousePos()[0]-12,ForeGround.getMousePos()[1]-9))

  #number of times the while loop has run
  iterNum +=1

  #END
  #end of main loop. all code goes in between
  pg.display.flip()