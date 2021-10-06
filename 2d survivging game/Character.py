import pygame as pg
from gameWindow import Block
import math

worldLength = 1000
worldHeight = 1000

yCharacterRenderOffset = 72


#blockSize used for rendering
blockSize = 32
numBlocks = int(800/blockSize)

class Character():
    global worldLength
    #things defined at top are used in many functions and subclasses
    characterLocation = [(worldLength/2),501]
    characterDrawLocation = [400,400]
    characterBoundingBox = [383,505,36,72]
    playerSpeed = 0.3
    characterImage = 1

    #character images
    class Input():
        movingIter = 1
        direction = "right"
        animationSpeed = 2
        def inputKey(keyboardInput,iterNum):
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
            Character.characterDrawLocation[1] = (Character.characterLocation[1]*blockSize)

        #checks for collisions in a specified position relative to the player and returns true or false
        
        #hard coding offsets dont forget to make them variable later
        def CollisionCheck(direction ,custom = False,xOffset = 0,yOffset = 0):
            if custom == False:
                if direction == "right":
                    if(Block.BlockMatrix[math.floor(Character.characterLocation[1])-2+yOffset][math.floor(Character.characterLocation[0])+11+xOffset] != Block.Type.BlockType.air):
                        return True
                elif direction == "left":
                    if(Block.BlockMatrix[math.floor(Character.characterLocation[1])-2+yOffset][math.floor(Character.characterLocation[0])+13+xOffset] != Block.Type.BlockType.air):
                        return True
                elif direction == "leftunder":
                    if(Block.BlockMatrix[math.floor(Character.characterLocation[1])-2+yOffset][math.floor(Character.characterLocation[0])+11+xOffset] != Block.Type.BlockType.air):
                        return True
                elif direction == "rightunder":
                    if(Block.BlockMatrix[math.floor(Character.characterLocation[1])-2+yOffset][math.floor(Character.characterLocation[0])+13+xOffset] != Block.Type.BlockType.air):
                        return True
                elif direction == "under":
                    if(Block.BlockMatrix[math.floor(Character.characterLocation[1])-1+yOffset][math.floor(Character.characterLocation[0])+11+xOffset] != Block.Type.BlockType.air):
                        return True
                elif direction == "above":
                    if (Block.BlockMatrix[math.floor(Character.characterLocation[1])-4+yOffset][math.floor(Character.characterLocation[0])+12+xOffset] != Block.Type.BlockType.air):
                        return True
                else:
                    return False
            elif custom == True:
                if(Block.BlockMatrix[math.floor(Character.characterLocation[1])-(yOffset+-8)][math.floor(Character.characterLocation[0])+(xOffset+12)] != Block.Type.BlockType.air):
                    return True
                else:
                    return False
        def newCollisionCheck(blockCoordX,blockCoordY,xBoundsOffset=0,yBoundsOffset=0,calcOffset=False,moving=0,direction=0):
            #adding a .30 offset while moving was the only way i could get it to work for moving blocks. this code has made me want to hang myself
            offset = 0
            if calcOffset == True and moving == True:
                if direction == 'left':
                    offset = 0.30
                elif direction == 'right':
                    offset = -0.30
                else:
                    offset = 0
            #calculates the fraction at the end of the character location value to add to the offset
            xOffset = round(Character.characterLocation[0],1)%1
            yOffset = round(Character.characterLocation[1],1)%1

            #does offsetting and translates into screen coords
            blockCoordX -= Character.characterLocation[0]+xOffset
            blockCoordX = blockCoordX * blockSize

            #does offsetting and translates into screen coords
            blockCoordY -= Character.characterLocation[1]+yOffset
            blockCoordY = blockCoordY * blockSize

            #defines bounding box locally so i can add offsets
            boundingBox = pg.Rect(Character.characterBoundingBox[0]+xBoundsOffset,Character.characterBoundingBox[1]+yBoundsOffset,Character.characterBoundingBox[2],Character.characterBoundingBox[3])
            pg.draw.rect(ForeGround.display,(255,0,0),pg.Rect(blockCoordX,blockCoordY,32,32))
            if boundingBox.colliderect(pg.Rect(blockCoordX,blockCoordY,32,32)):
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
