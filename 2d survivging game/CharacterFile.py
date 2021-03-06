from numpy.lib.npyio import recfromtxt
import pygame as pg
import gameWindow
import math
import inventory

worldLength = 1000
worldHeight = 1000

yCharacterRenderOffset = 72


#blockSize used for rendering
blockSize = 32
numBlocks = int(800/blockSize)

class Character():
    global worldLength
    #things defined at top are used in many functions and subclasses
    health = 100
    characterScreenCoords = [383,505]
    characterLocation = [math.floor(worldLength/2),500]
    characterDrawLocation = [400,400]
    characterBoundingBox = pg.Rect(383,505,36,72)
                    #top left               #bottom left           #top right             #bottom right          #bottom          #head hitbox
    boundingBoxes = [pg.Rect(383,519,18,16),pg.Rect(383,545,18,16),pg.Rect(401,518,18,16),pg.Rect(401,545,18,16),pg.Rect(387,561,28,11),pg.Rect(392,503,18,8)]
    playerSpeed = 0.1
    characterImage = 1

    #character images
    def healthUpdate(entities):
        if Character.health <= 0:
            inventory.Inventory.clearInventory(True,entities)
            Character.characterLocation = [gameWindow.World.spawnCoords[0],gameWindow.World.spawnCoords[1]]
            Character.health = 100
    class Input():
        movingIter = 1
        direction = "right"
        animationSpeed = 4
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
                    moveCount = 0
                    while moveCount <= Character.playerSpeed*gameWindow.World.deltaTime:
                        if Character.Pos.newCollisionCheck()[0] != 1 and Character.Pos.newCollisionCheck()[1] != 1:
                            Character.characterLocation[0] -= 0.1
                            moveCount += 0.1
                        elif Character.Pos.newCollisionCheck()[1] == 1 and iterNum%3 == 0 and Character.Pos.newCollisionCheck()[5] != 1 and Character.Pos.newCollisionCheck()[0] != 1 and Character.Pos.newCollisionCheck()[4] == 1:
                            Character.characterLocation[1] -= 1
                            Character.characterLocation[0] -= 0.1
                            if Character.Pos.newCollisionCheck()[0] == 1:
                                Character.characterLocation[1] += 1
                                Character.characterLocation[0] += 0.1
                            break
                        else:
                            break
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
                    moveCount = 0
                    while moveCount <= Character.playerSpeed*gameWindow.World.deltaTime:
                        if (Character.Pos.newCollisionCheck()[2] != 1) and Character.Pos.newCollisionCheck()[3] != 1:
                            Character.characterLocation[0] += 0.1
                            moveCount += 0.1
                        elif Character.Pos.newCollisionCheck()[3] == 1 and iterNum%3 == 0 and Character.Pos.newCollisionCheck()[5] != 1 and Character.Pos.newCollisionCheck()[2] != 1 and Character.Pos.newCollisionCheck()[4] == 1:
                            Character.characterLocation[1] -= 1
                            Character.characterLocation[0] += 0.1
                            if Character.Pos.newCollisionCheck()[2] == 1:
                                Character.characterLocation[1] += 1
                                Character.characterLocation[0] -= 0.1
                            break
                        else:
                            break
                #decides what animation to use for the character
                if moving == True and iterNum%Character.Input.animationSpeed == 0:
                    Character.characterImage = Character.Render.SpritePick(Character.Input.direction,Character.Input.movingIter)
                    if Character.Input.movingIter >= 4:
                        Character.Input.movingIter = 1
                    else:
                        Character.Input.movingIter+= 1
            else:
                   moving = False
                   moveCount = 0
                   if Character.Input.direction == "right":
                    Character.characterImage = Character.Image.characterStillRight
                   elif Character.Input.direction == "left":
                    Character.characterImage = Character.Image.characterStillLeft
                   Character.Input.movingIter = 1
            

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
                             pg.Rect(Character.characterScreenCoords[0]+3,Character.characterScreenCoords[1]+56,28,11), #bottom
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
        def newCollisionCheck(drawHitboxes = False):
            """
            checks collisions with the players hitboxes against nearby blocks and returns a list of boxes that have detected a collision
            returns a list with 6 values 1 or 0 corelating to colided boxes
            [top left, bottom left, top right, bottom right, bottom, head]
            takes one optional param:
            
            drawHitBoxes: if set to true, it will draw the players hitboxes while checking for collisions. used for debugging.
            """
            returnValue = [0,0,0,0,0,0]

            yOff = math.floor(Character.characterScreenCoords[1]/32-16)
            xOff = math.floor(Character.characterScreenCoords[0]/32-11)

            if drawHitboxes == True:
                for i in Character.boundingBoxes:
                    pg.draw.rect(gameWindow.ForeGround.display,(255,255,255),i)

            for y in range(math.floor(Character.characterLocation[1]-5+yOff),math.floor(Character.characterLocation[1]+3+yOff)):
                for x in range(math.floor(Character.characterLocation[0]+9+xOff),math.floor(Character.characterLocation[0]+17+xOff)): 
                    #loops through list of blocks with collisions disabled
                    noCollide = False
                    for i in gameWindow.Block.Type.xCollideBlocks:
                        if gameWindow.Block.BlockMatrix[y][x] == i:
                            noCollide = True
                            break
                    if gameWindow.Block.BlockMatrix[y][x] != gameWindow.Block.Type.BlockType.air:
                        if noCollide == True:
                            continue
                        rectX = x - Character.characterLocation[0]
                        rectY = y - (Character.characterLocation[1]) + 19

                        rectX = rectX * blockSize
                        rectY = rectY * blockSize

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