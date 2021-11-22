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
    characterScreenCoords = [383,505]
    characterLocation = [math.floor(worldLength/2),500]
    characterDrawLocation = [400,400]
    characterBoundingBox = pg.Rect(383,505,36,72)
                    #top left               #bottom left           #top right             #bottom right          #bottom          #head hitbox
    boundingBoxes = [pg.Rect(383,519,18,16),pg.Rect(383,545,18,16),pg.Rect(401,518,18,16),pg.Rect(401,545,18,16),pg.Rect(387,561,28,16),pg.Rect(392,503,18,8)]
    playerSpeed = 0.1
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
                if Character.Pos.newCollisionCheck()[0] == 1 or Character.characterLocation[0] < 20:
                        doMove1 = False
                #updates player pos
                if doMove1 == True:
                    if Character.Pos.newCollisionCheck()[0] != 1:
                        Character.characterLocation[0] -= Character.playerSpeed
                    if Character.Pos.newCollisionCheck()[1] == 1 and iterNum%3 == 0 and Character.Pos.newCollisionCheck()[5] != 1:
                        Character.characterLocation[1] -= 1
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
                if Character.Pos.newCollisionCheck()[2] == 1 or Character.characterLocation[0] > 950:
                        doMove = False    
                #updates player pos
                if doMove == True:
                    if Character.Pos.newCollisionCheck()[2] != 1:
                        Character.characterLocation[0] += Character.playerSpeed
                    if Character.Pos.newCollisionCheck()[3] == 1 and iterNum%3 == 0 and Character.Pos.newCollisionCheck()[5] != 1:
                        Character.characterLocation[1] -= 1
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
        characterStillRight = pg.image.load("./Images/Character Icons/stillRight.png").convert_alpha()
        characterStillLeft = pg.image.load("./Images/Character Icons/stillLeft.png").convert_alpha()

    class Pos():

        #moves the character left or right
        def update():
            Character.characterDrawLocation[0] = Character.characterLocation[0]*blockSize
            Character.characterDrawLocation[1] = Character.characterLocation[1]*blockSize

        def updateDrawCoords(screenSize):

            #[383,505]

            Character.characterScreenCoords[0] = screenSize[0]/2-18
            Character.characterScreenCoords[1] = screenSize[1]-288

            Character.boundingBoxes = [pg.Rect(Character.characterScreenCoords[0],Character.characterScreenCoords[1]+14,18,16), #top left
                             pg.Rect(Character.characterScreenCoords[0],Character.characterScreenCoords[1]+40,18,16), #bottom left
                             pg.Rect(Character.characterScreenCoords[0]+18,Character.characterScreenCoords[1]+13,18,16),#top right
                             pg.Rect(Character.characterScreenCoords[0]+18,Character.characterScreenCoords[1]+40,18,16),#bottom right
                             pg.Rect(Character.characterScreenCoords[0]+3,Character.characterScreenCoords[1]+56,28,16), #bottom
                             pg.Rect(Character.characterScreenCoords[0]+8,Character.characterScreenCoords[1],18,8)] #head 

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
                    if (gameWindow.Block.BlockMatrix[math.floor(Character.characterLocation[1])-4+yOffset][math.floor(Character.characterLocation[0])+12+xOffset] != gameWindow.Block.Type.BlockType.air) :
                        return True
                else:
                    return False
            elif custom == True:
                if(gameWindow.Block.BlockMatrix[math.floor(Character.characterLocation[1])-(yOffset+-8)][math.floor(Character.characterLocation[0])+(xOffset+12)] != gameWindow.Block.Type.BlockType.air):
                    return True
                else:
                    return False
        def newCollisionCheck():
            returnValue = [0,0,0,0,0,0]

            yOff = math.floor(Character.characterScreenCoords[1]/32-16)
            xOff = math.floor(Character.characterScreenCoords[0]/32-11)

            for y in range(math.floor(Character.characterLocation[1]-5+yOff),math.floor(Character.characterLocation[1]+3+yOff)):
                for x in range(math.floor(Character.characterLocation[0]+9+xOff),math.floor(Character.characterLocation[0]+17+xOff)): 
                    if gameWindow.Block.BlockMatrix[y][x] != gameWindow.Block.Type.BlockType.air:
                        rectX = x - Character.characterLocation[0]# + math.floor(Character.characterScreenCoords[0]/32)
                        rectY = y - (Character.characterLocation[1]) + 19# + math.floor(Character.characterScreenCoords[1]/32)
                    

                        rectX = rectX * blockSize# - 352
                        rectY = rectY * blockSize# - 512

                        blockChecking = pg.Rect((rectX,rectY),(32,32))

                        if blockChecking.colliderect(Character.boundingBoxes[0]):
                            returnValue[0] = 1
                        if blockChecking.colliderect(Character.boundingBoxes[1]):
                            returnValue[1] = 1
                        if blockChecking.colliderect(Character.boundingBoxes[2]):
                            returnValue[2] = 1
                        if blockChecking.colliderect(Character.boundingBoxes[3]):
                            returnValue[3] = 1
                        if blockChecking.colliderect(Character.boundingBoxes[4]):
                            returnValue[4] = 1
                        if blockChecking.colliderect(Character.boundingBoxes[5]):
                            returnValue[5] = 1
                        if returnValue == [1,1,1,1,1,1]:
                            break
            return returnValue
                            
    class Render():
        global yCharacterRenderOffset
        global blockSize
        def SpritePick(Direction,AnimationFrameIter):
            #used to decide which frame to display for character 
            if Direction == "left":
                return pg.image.load("./Images/Character Icons/movingLeftFrame"+str(AnimationFrameIter)+".png").convert_alpha()
            elif Direction == "right":
                return pg.image.load("./Images/Character Icons/movingRightFrame"+str(AnimationFrameIter)+".png").convert_alpha()


        def draw(surface,imageIn,x,y):
        #renders the character still
            x = x * blockSize
            y = y * blockSize
            surface.blit(imageIn,(x,y))

        def drawStillX(surface,imageIn):
            surface.blit(imageIn,(Character.characterScreenCoords[0],Character.characterScreenCoords[1]-8))