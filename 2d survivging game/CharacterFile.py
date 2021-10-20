import pygame as pg
import gameWindow
import math
import inventory
import itemIds

worldLength = 1000
worldHeight = 1000

yCharacterRenderOffset = 72


#blockSize used for rendering
blockSize = 32
numBlocks = int(800/blockSize)

class Character():
    global worldLength
    #things defined at top are used in many functions and subclasses
    characterLocation = [math.floor(worldLength/2),501]
    characterDrawLocation = [400,400]
    characterBoundingBox = pg.Rect(383,505,36,72)
    playerSpeed = 0.3
    characterImage = 1

    #character images
    class Input():
        movingIter = 1
        direction = "right"
        animationSpeed = 2
        blockType = 2 #dirt. .Block dosent exist just right here for some reason
        def inputKey(keyboardInput,iterNum,entities):
            #blockType logic
            if keyboardInput[pg.K_1]:
                inventory.Inventory.selectedSlot = 0
            elif keyboardInput[pg.K_2]:
                inventory.Inventory.selectedSlot = 1
            elif keyboardInput[pg.K_3]:
                inventory.Inventory.selectedSlot = 2
            elif keyboardInput[pg.K_4]:
                inventory.Inventory.selectedSlot = 3
            elif keyboardInput[pg.K_5]:
                inventory.Inventory.selectedSlot = 4
            elif keyboardInput[pg.K_6]:
                inventory.Inventory.selectedSlot = 5
            elif keyboardInput[pg.K_7]:
                inventory.Inventory.selectedSlot = 6
            elif keyboardInput[pg.K_8]:
                inventory.Inventory.selectedSlot = 7
            elif keyboardInput[pg.K_9]:
                inventory.Inventory.selectedSlot = 8

            if keyboardInput[pg.K_a]:
                moving = True
                doMove1 = True
                Character.Input.direction = "left"
                #checks for player collisions with adjacent blocks
                if Character.Pos.CollisionCheck("left",False,-1,-1) or Character.characterLocation[0] < 20:
                        doMove1 = False
                #updates player pos
                if doMove1 == True:
                    if Character.Pos.CollisionCheck("left",False,-1,0) == True and iterNum%3 == 0 and Character.Pos.CollisionCheck('above',False) != True:
                        Character.characterLocation[1] -= 1
                        Character.characterLocation[0] -= 1
                    elif Character.Pos.CollisionCheck("left",False,-1,0) != True:
                        Character.characterLocation[0] -= Character.playerSpeed
                Character.Pos.update()
                #decides what animation to use for the character
                if moving == True and iterNum%Character.Input.animationSpeed == 0:
                    Character.characterImage = Character.Render.SpritePick(Character.Input.direction,Character.Input.movingIter)
                    if Character.Input.movingIter >= 4:
                        Character.Input.movingIter = 1
                    else:
                        Character.Input.movingIter+= 1
            elif keyboardInput[pg.K_d]:
                moving = True
                doMove = True
                Character.Input.direction = "right"
                #checks for player collisions with adjacent blocks
                if Character.Pos.CollisionCheck("right",False,2,-1) or Character.characterLocation[0] > 950:
                        doMove = False    
                #updates player pos
                if doMove == True:
                    if Character.Pos.CollisionCheck("right",False,2,0) == True and iterNum%3 == 0 and Character.Pos.CollisionCheck('above',False) != True:
                        Character.characterLocation[1] -= 1
                        Character.characterLocation[0] += 1
                    elif Character.Pos.CollisionCheck("right",False,2,0) != True:
                        Character.characterLocation[0] += Character.playerSpeed
                #decides what animation to use for the character
                if moving == True and iterNum%Character.Input.animationSpeed == 0:
                    Character.characterImage = Character.Render.SpritePick(Character.Input.direction,Character.Input.movingIter)
                    if Character.Input.movingIter >= 4:
                        Character.Input.movingIter = 1
                    else:
                        Character.Input.movingIter+= 1
            else:
                   moving = False
                   if Character.Input.direction == "right":
                    Character.characterImage = Character.Image.characterStillRight
                   elif Character.Input.direction == "left":
                    Character.characterImage = Character.Image.characterStillLeft
                   Character.Input.movingIter = 1

            if keyboardInput[pg.K_k]:
                inventory.Inventory.grid[0][0] = itemIds.Items.Id.stone
                inventory.Inventory.stackAmount[0][0] = 100
                inventory.Inventory.grid[0][1] = itemIds.Items.Id.dirt
                inventory.Inventory.stackAmount[0][1] = 100
                inventory.Inventory.grid[0][2] = itemIds.Items.Id.grass
                inventory.Inventory.stackAmount[0][2] = 100
                inventory.Inventory.grid[0][3] = itemIds.Items.Id.sand
                inventory.Inventory.stackAmount[0][3] = 100
                inventory.Inventory.grid[0][4] = itemIds.Items.Id.wood
                inventory.Inventory.stackAmount[0][4] = 100
            
           

            if keyboardInput[pg.K_LSHIFT]:
              Character.playerSpeed =  0.4
              Character.Input.animationSpeed = 2
            else:
              Character.playerSpeed = 0.3
              Character.Input.animationSpeed = 4

    class Image():
        global blockSize
        #character still images
        characterStillRight = pg.image.load("./Images/Character Icons/stillRight.png")
        characterStillLeft = pg.image.load("./Images/Character Icons/stillLeft.png")

    class Pos():

        #moves the character left or right
        def update(moveAmount = 1):
            Character.characterDrawLocation[0] = Character.characterLocation[0]*blockSize
            Character.characterDrawLocation[1] = Character.characterLocation[1]*blockSize

        #checks for collisions in a specified position relative to the player and returns true or false
        
        #hard coding offsets dont forget to make them variable later
        def CollisionCheck(direction ,custom = False,xOffset = 0,yOffset = 0):
            if custom == False:
                if direction == "right":
                    if(gameWindow.Block.BlockMatrix[math.floor(Character.characterLocation[1])-2+yOffset][math.floor(Character.characterLocation[0])+11+xOffset] != gameWindow.Block.Type.BlockType.air):
                        return True
                elif direction == "left":
                    if(gameWindow.Block.BlockMatrix[math.floor(Character.characterLocation[1])-2+yOffset][math.floor(Character.characterLocation[0])+13+xOffset] != gameWindow.Block.Type.BlockType.air):
                        return True

                elif direction == "under":
                    if(gameWindow.Block.BlockMatrix[math.floor(Character.characterLocation[1])-1+yOffset][math.floor(Character.characterLocation[0])+11+xOffset] != gameWindow.Block.Type.BlockType.air):
                        return True
                elif direction == "above":
                    if (gameWindow.Block.BlockMatrix[math.floor(Character.characterLocation[1])-4+yOffset][math.floor(Character.characterLocation[0])+12+xOffset] != gameWindow.Block.Type.BlockType.air):
                        return True
                else:
                    return False
            elif custom == True:
                if(gameWindow.Block.BlockMatrix[math.floor(Character.characterLocation[1])-(yOffset+-8)][math.floor(Character.characterLocation[0])+(xOffset+12)] != gameWindow.Block.Type.BlockType.air):
                    return True
                else:
                    return False
        def newCollisionCheck(blockCoordX,blockCoordY):
            
            x = blockCoordX - Character.characterLocation[0]
            y = blockCoordY - (Character.characterLocation[1]) + 19

            x = x * blockSize
            y = y * blockSize

            boundingBox = pg.Rect(Character.characterBoundingBox[0],Character.characterBoundingBox[1],Character.characterBoundingBox[2],Character.characterBoundingBox[3])

            #debug stuff
            pg.draw.rect(gameWindow.ForeGround.display,(255,0,0),pg.Rect(x,y,32,32))

            if boundingBox.colliderect(pg.Rect(x,y,32,32)) and gameWindow.Block.BlockMatrix[math.floor(blockCoordY)][math.floor(blockCoordX)] != gameWindow.Block.Type.BlockType.air:
                return True
            else:
                return False
    class Render():
        global yCharacterRenderOffset
        global blockSize
        def SpritePick(Direction,AnimationFrameIter):
            #used to decide which frame to display for character 
            if Direction == "left":
                return pg.image.load("./Images/Character Icons/movingLeftFrame"+str(AnimationFrameIter)+".png")
            elif Direction == "right":
                return pg.image.load("./Images/Character Icons/movingRightFrame"+str(AnimationFrameIter)+".png")


        def draw(surface,imageIn,x,y):
        #renders the character still
            x = x * blockSize
            y = y * blockSize
            surface.blit(imageIn,(x,y))

        def drawStillX(surface,imageIn):
            surface.blit(imageIn,(383,505))
