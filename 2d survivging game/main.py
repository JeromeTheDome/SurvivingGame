import pygame
import time
import math
from gameWindow import ForeGround
from gameWindow import BackGround
from gameWindow import Block
from gameWindow import Gui
from CharacterFile import Character
from inventory import Inventory
from itemIds import Items
import craftingRecipies
from pygame.locals import *
from entity import Entity
import os
from container import Container
from gameWindow import World
from blockInteractionHandler import InteractionHandler
from blockPlaceLogic import blockPlaceLogicTable,PlaceLogic

"""
to do list:
make sand edible
code cleanup (high priority)
overhaul world generation system
add delta time to world events
"""
"""
notes: 
"""

pg = pygame
pygame.font.init()

#inits

#default values
skycolorGradient = [(4,11,68),(4,11,68),(4,11,68),(4,11,68),(4,11,68),(0,53,119),(12,81,91),(17,148,178),(16,107,119),(16,107,119),(21,135,150),(26,169,118),(31,201,224),(31,201,224),(31,201,224),(31,201,224),(31,201,224),(31,201,224),(31,201,224),(24,158,175),(23,151,168),(17,110,122),(4,11,68),(4,11,68)]
placingMatrix = "foreground"
realYVel = 0
windowWlast, windowHlast = [None,None]
exitButton = pg.Rect((725,665),(55,55))
saveButton = pg.Rect((725,725),(55,55))
textBoxText = ''
activeTextBox = None
inventoryBackGround = pg.image.load("./Images/hud/openInventoryBackground.png").convert_alpha()
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
bgImage = BackGround.bgImage("./Images/background images/morning.png").convert()
bgImage2 = BackGround.bgImage("./Images/background images/morning.png").convert()
bgImage2 = pygame.transform.flip(bgImage2,False,True)

Inventory.grid[0][0] = Items.Id.defaultPick
Inventory.stackAmount[0][0] = 1
Inventory.grid[0][1] = Items.Id.defaultAxe
Inventory.stackAmount[0][1] = 1
Inventory.grid[0][2] = Items.Id.defaultShovel
Inventory.stackAmount[0][2] = 1

def deleteEnt(index,entities):
	if len(entities) > index:
		if len(entities) > 0:
			entities[index].deleteEntity(index)
		del entities[index]

clock = pygame.time.Clock()

mainMenu = 1
mainGame = 2
loadGameScene= 3
createWorld = 4

scene = mainMenu

while True:
    frame = 0
    #main menu scene
    while scene == mainMenu:
        #gets window size and events
        windowW, windowH = pygame.display.get_surface().get_size()
        ev = pg.event.get()
        #sets cursor off screen
        pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))
        #clears screen
        pg.draw.rect(ForeGround.display,(255,255,255),pg.Rect((0,0),(800,800)))
        #renders the block background
        Block.Renderer.drawBlocksOnScreen((windowW/32+1,windowH/32-18))
        #defines the rectangle and checks for pressess on the load game button
        loadGameButton = pg.Rect((50,350),(300,100))
        ForeGround.display.blit(Gui.loadGameButton,(50,350))
        if loadGameButton.collidepoint(ForeGround.getMousePos()[0],ForeGround.getMousePos()[1]) and pg.mouse.get_pressed(3) == (True,False,False):
            scene = loadGameScene

        #does the same for the new game button
        newGameButton = pg.Rect((400,350),(300,100))
        ForeGround.display.blit(Gui.newGameButton,(400,350))
        if newGameButton.collidepoint(ForeGround.getMousePos()[0],ForeGround.getMousePos()[1]) and pg.mouse.get_pressed(3) == (True,False,False):
            scene = createWorld
        ForeGround.display.blit(ForeGround.cursorIcon,(ForeGround.getMousePos()[0]-12,ForeGround.getMousePos()[1]-9))
        pg.display.flip()
    
    #load game screen
    while scene == loadGameScene:
        windowW, windowH = pygame.display.get_surface().get_size()
        ev = pg.event.get()
        pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))
        #clears screen with while background
        pg.draw.rect(ForeGround.display,(255,255,255),pg.Rect((0,0),(800,800)))
        Block.Renderer.drawBlocksOnScreen((windowW/32+1,windowH/32-18))
        worlds = os.listdir("./saves")
        for i in range(len(worlds)):
            try:
                if str(worlds[i])[-7]+str(worlds[i])[-6]+str(worlds[i])[-5] == "_bg":
                    worlds.pop(i)
                if str(worlds[i])[-4]+str(worlds[i])[-3]+str(worlds[i])[-2]+str(worlds[i])[-1] == "json":
                    worlds.pop(i)
            except:
                pass

        #creates back button
        backButton = pg.Rect((20,30),(50,50))
        ForeGround.display.blit(Gui.backButton,(20,20))
        #places all world select buttons
        for i in range(len(worlds)):
            #defines world button
            worldButton = pg.Rect((200,(395+len(worlds)*15)-i*30),(400,20))
            ForeGround.display.blit(Gui.selectFileButton,(200,(395+len(worlds)*15)-i*30))
            #defines world button text
            fileNameText = myfont.render(str(worlds[i]), False, (0, 0, 0))
            fileNameTextWidth = fileNameText.get_rect().width
            ForeGround.display.blit(fileNameText,(400-(fileNameTextWidth/2),(390+len(worlds)*15)-i*30))
            #checks for mouse input
            for event in ev:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if worldButton.collidepoint(ForeGround.getMousePos()[0],ForeGround.getMousePos()[1]) and pg.mouse.get_pressed(3) == (True,False,False):
                        Block.Grid.loadWorld(str(worlds[i][:-4]))
                        scene = mainGame
                        break
                    elif backButton.collidepoint(ForeGround.getMousePos()[0],ForeGround.getMousePos()[1]) and pg.mouse.get_pressed(3) == (True,False,False):
                        scene = mainMenu
            
        ForeGround.display.blit(ForeGround.cursorIcon,(ForeGround.getMousePos()[0]-12,ForeGround.getMousePos()[1]-9))
        pg.display.flip()


    #create world scene
    while scene == createWorld:
        windowW, windowH = pygame.display.get_surface().get_size()
        ev = pg.event.get()
        pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))
        pg.draw.rect(ForeGround.display,(255,255,255),pg.Rect((0,0),(800,800)))
        Block.Renderer.drawBlocksOnScreen((windowW/32+1,windowH/32-18))
        #creates back button
        backButton = pg.Rect((20,30),(50,50))
        ForeGround.display.blit(Gui.backButton,(20,20))
        #defines all text boxes
        textBoxes = [pg.Rect((350, 375), (100, 25))]
        #creates make worl button
        createWorldButton = pg.Rect((350, 450), (100, 50))
        createWorldButtonText = myfont.render("create world", True, (255, 255, 255))
        pg.draw.rect(ForeGround.display,(180,180,180),createWorldButton)
        ForeGround.display.blit(createWorldButtonText,(350,450))
        #makes name world text
        nameWorldText = myfont.render("World Name: ", True, (255, 255, 255))
        ForeGround.display.blit(nameWorldText,(400-(nameWorldText.get_rect().width/2),355))
        #checks through all text boxes to process logic for them
        for i in range(len(textBoxes)):
            boxColor = (180,180,180)
            for event in ev:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if textBoxes[i].collidepoint(ForeGround.getMousePos()[0],ForeGround.getMousePos()[1]) and pg.mouse.get_pressed(3) == (True,False,False):
                            activeTextBox = i

            if activeTextBox == i:
                boxColor = (200,200,200)

        #keys key input for text box
        for event in ev:
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_BACKSPACE:
                    textBoxText = textBoxText[:-1]
                elif event.key == pygame.K_RETURN:
                    textBoxText = ''
                else:
                    textBoxText += event.unicode
            #mouse input
            if event.type == pygame.MOUSEBUTTONDOWN:
                        if createWorldButton.collidepoint(ForeGround.getMousePos()[0],ForeGround.getMousePos()[1]) and pg.mouse.get_pressed(3) == (True,False,False):
                            World.generateWorld()
                            World.openWorld = textBoxText
                            scene = mainGame
                        if backButton.collidepoint(ForeGround.getMousePos()[0],ForeGround.getMousePos()[1]) and pg.mouse.get_pressed(3) == (True,False,False):
                            scene = mainMenu

        textBoxTextSurface = myfont.render(textBoxText, True, (255, 255, 255))

        if activeTextBox != None:
            textBoxWidth = textBoxTextSurface.get_rect().width
            ForeGround.display.blit(textBoxTextSurface,(400-(textBoxWidth/2),375))

        frame += 1
        ForeGround.display.blit(ForeGround.cursorIcon,(ForeGround.getMousePos()[0]-12,ForeGround.getMousePos()[1]-9))
        pg.display.flip()

    #main game loop
    while scene == mainGame:
        #gets pygame events and window size
        ev = pg.event.get()
        windowW, windowH = pygame.display.get_surface().get_size()
        #gets keyboard input
        keyboardInput = pg.key.get_pressed()
        #sets the cursor off screen
        pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))
        #gets time since last frame also called the frame delta or delta time
        World.deltaTime = clock.tick(60)/10
        #START
        if placingMatrix == "foreground":
            layer = 1
        elif placingMatrix == "background":
            layer = 2

        #rounds the window size to the nearest number divisible by 32 and moves the player to the proper position
        for event in ev:
            if event.type == pg.VIDEORESIZE:
                flags = DOUBLEBUF
                ForeGround.display = pg.display.set_mode((math.floor(windowW/32)*32,math.floor(windowH/32)*32),flags)
                
                windowDeltaX = (windowW-windowWlast)/32
                windowDeltaY = (windowH-windowHlast)/32

                Character.characterLocation[0] -= windowDeltaX
                Character.characterLocation[1] -= windowDeltaY

        #world stuff
        if World.time >= 43200:
            World.time = 0
        World.time += World.deltaTime-1
        #checks mouse input
        #right click
        if pg.mouse.get_pressed(3) == (False,False,True):
            if Block.Grid.getBlockAtLocation((ForeGround.getMousePos()[0],ForeGround.getMousePos()[1]),layer) == Block.Type.BlockType.air and Inventory.selectedSlot != None:
                Inventory.stackAmount[0][Inventory.selectedSlot] -= 1

                if Inventory.grid[0][Inventory.selectedSlot] != None:
                    if Inventory.grid[0][Inventory.selectedSlot] == Items.Id.chest:
                        Inventory.containers += [Container((Block.Grid.translateToBlockCoords(ForeGround.getMousePos())[0],Block.Grid.translateToBlockCoords(ForeGround.getMousePos())[1]),1)]
                    if Inventory.grid[0][Inventory.selectedSlot] <= 50:
                        if placingMatrix == "foreground":
                            try:
                                blockPlaceLogicTable[Inventory.grid[0][Inventory.selectedSlot]]()
                            except KeyError:
                                blockPlaceLogicTable['default']()
                        elif placingMatrix == "background":
                            Block.Grid.placeBlockBg((ForeGround.getMousePos()[0],ForeGround.getMousePos()[1]),Inventory.grid[0][Inventory.selectedSlot])
        #left click
        if pg.mouse.get_pressed(3) == (True,False,False):
            if Inventory.open == False:
                ySize = 48
                for i in range(9):
                    if math.floor(ForeGround.getMousePos()[0]/48) == i and math.floor(ForeGround.getMousePos()[1]/48) == 0:
                        Inventory.selectedSlot = i
            elif Inventory.open == True:
                ySize = 240
                #checks for presses on the save button and saves the world if true
                if saveButton.collidepoint(ForeGround.getMousePos()[0],ForeGround.getMousePos()[1]):
                    for event in ev:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                                Block.Grid.saveWorld(World.openWorld)
                #checks for presses on the exit button
                if exitButton.collidepoint(ForeGround.getMousePos()[0],ForeGround.getMousePos()[1]):
                    for event in ev:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            #cleans up world
                            for y in range(worldHeight):
                                for x in range(worldLength):
                                    Block.BlockMatrix[y][x] = Block.Type.BlockType.dirt
                                    Block.bgBlockMatrix[y][x] = Block.Type.BlockType.air
                            Inventory.open = False
                            Inventory.craftingTableOpen == False
                            scene = mainMenu
                #handles interaction with the inventory
                for y in range(5):
                    for x in range(9):
                        for event in ev:
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                #calculates which box the player clicked
                                if math.floor(ForeGround.getMousePos()[0]/48) == x and math.floor(ForeGround.getMousePos()[1]/48) == y:   
                                    #what to do when the cursor is the same as the item in the slot    
                                    if Inventory.itemOnCursor == Inventory.grid[y][x]:
                                        for i in range(Inventory.itemCountOnCursor):
                                            if Inventory.stackAmount[y][x] < 100:
                                                Inventory.stackAmount[y][x] += 1
                                                Inventory.itemCountOnCursor -= 1
                                            else:
                                                break
                                        if Inventory.itemCountOnCursor <= 0:
                                            Inventory.itemOnCursor = Items.Id.empty
                                    #what to do when both the cursor and slot have something
                                    elif Inventory.itemOnCursor != Items.Id.empty and Inventory.grid[y][x] != Items.Id.empty:
                                        temporaryItem = Inventory.itemOnCursor
                                        temporaryItemCount = Inventory.itemCountOnCursor

                                        Inventory.itemOnCursor = Inventory.grid[y][x]
                                        Inventory.itemCountOnCursor = Inventory.stackAmount[y][x]

                                        Inventory.grid[y][x] = temporaryItem
                                        Inventory.stackAmount[y][x] = temporaryItemCount
                                    #what to do when the cursor is empty
                                    elif Inventory.itemOnCursor == Items.Id.empty:
                                        Inventory.itemOnCursor = Inventory.grid[y][x]
                                        Inventory.itemCountOnCursor = Inventory.stackAmount[y][x]

                                        Inventory.grid[y][x] = Items.Id.empty
                                        Inventory.stackAmount[y][x] =0
                                    #what to do when the cursor is not empty
                                    elif Inventory.itemOnCursor != Items.Id.empty:
                                        Inventory.grid[y][x] = Inventory.itemOnCursor
                                        Inventory.stackAmount[y][x] = Inventory.itemCountOnCursor

                                        Inventory.itemOnCursor = Items.Id.empty
                                        Inventory.itemCountOnCursor = 0

            if Inventory.selectedSlot != None and (ForeGround.getMousePos()[0] > 432 or ForeGround.getMousePos()[1] > ySize) and 1 <= Inventory.grid[0][Inventory.selectedSlot] <= 50:
                if Inventory.stackAmount[0][Inventory.selectedSlot] <= 0:
                    Inventory.grid[0][Inventory.selectedSlot] = Items.Id.empty
                    Inventory.stackAmount[0][Inventory.selectedSlot] = 0

            if Block.Grid.blockBreakingPos != Block.Grid.blockBreakingPosLast:
                blockBreakNumber = 1

            Block.Grid.SetBlockBreakCoord((ForeGround.getMousePos()[0]+Character.characterDrawLocation[0], (ForeGround.getMousePos()[1]+Character.characterDrawLocation[1])-600))

            blockBreakSpeed = Block.Type.determineBreakingSpeed(layer)
            if Block.Grid.getBlockAtLocation2(Block.Grid.blockBreakingPos,layer) == Block.Type.BlockType.air:
                    blockBreakNumber = 1

            if iterNum%blockBreakSpeed == 0:
                blockBreakNumber += 1
            if blockBreakNumber%6 == 0:
                entities += [Entity(Block.Grid.translateToBlockCoords(ForeGround.getMousePos()),(16,16),0,Block.Grid.getBlockAtLocation2(Block.Grid.blockBreakingPos,layer))]
                Block.Grid.breakBlock((ForeGround.getMousePos()[0],ForeGround.getMousePos()[1]),layer)
                blockBreakNumber = 1
        else:
                blockBreakNumber = 1


        #middle click
        if pg.mouse.get_pressed(3) == (False,True,False):
            if Inventory.open == True:
                for y in range(5):
                        for x in range(9):
                            for event in ev:
                                if event.type == pygame.MOUSEBUTTONDOWN:
                                    if math.floor(ForeGround.getMousePos()[0]/48) == x and math.floor(ForeGround.getMousePos()[1]/48) == y:
                                        if Inventory.itemOnCursor == Items.Id.empty:
                                            Inventory.stackAmount[y][x] -= 1
                                            Inventory.itemOnCursor = Inventory.grid[y][x]
                                            Inventory.itemCountOnCursor += 1
                                            if Inventory.stackAmount[y][x] <= 0:
                                                Inventory.grid[y][x] = Items.Id.empty

                                        elif Inventory.itemOnCursor == Inventory.grid[y][x]:
                                            Inventory.stackAmount[y][x] -= 1
                                            if Inventory.stackAmount[y][x] <= 0:
                                                Inventory.grid[y][x] = Items.Id.empty
                                            Inventory.itemCountOnCursor += 1        

        """
        visual screen logic(background, screen scrolling ect.)
        """

        #draws background image
        bgColor = skycolorGradient[int(World.time/1800)-1]
        pg.draw.rect(ForeGround.display,bgColor,pg.Rect(0,0,windowW,windowH))

        #sets light level according to time
        time24hr = int(World.time/1800) + 1
        if 1 <= time24hr <= 5:
            Block.Renderer.naturalLightLevel = 3
        elif time24hr == 6:
            Block.Renderer.naturalLightLevel = 5
        elif time24hr == 7:
            Block.Renderer.naturalLightLevel = 7
        elif time24hr == 8:
            Block.Renderer.naturalLightLevel = 9
        elif time24hr == 9:
            Block.Renderer.naturalLightLevel = 10
        elif time24hr == 10:
            Block.Renderer.naturalLightLevel = 12
        elif time24hr == 11:
            Block.Renderer.naturalLightLevel = 14
        elif 12 <= time24hr <= 18:
            Block.Renderer.naturalLightLevel = 15
        elif time24hr == 19:
            Block.Renderer.naturalLightLevel = 12
        elif time24hr == 20:
            Block.Renderer.naturalLightLevel = 10
        elif time24hr == 21:
            Block.Renderer.naturalLightLevel = 7
        elif time24hr == 22:
            Block.Renderer.naturalLightLevel = 5
        elif time24hr == 23:
            Block.Renderer.naturalLightLevel = 3
        elif time24hr == 24:
            Block.Renderer.naturalLightLevel = 3


        """
        block placement and properties logic
        """

        #renders blocks and the breaking overlay

        Block.Renderer.drawBlocksOnScreen((windowW/32+1,windowH/32-18))
            
        Block.Renderer.drawBreakingOverlay(blockBreakNumber,layer)
                    
        """
        player logic
        """
        if Character.health <= 0:
            realYVel = 0
        Character.healthUpdate(entities)

        #physics stuff

        #adds y velocity to the player, effectively gravity
        yVelocity += 0.01*World.deltaTime
        realYVel += 0.01*World.deltaTime

        #terminal velocity
        if yVelocity > 1:
            yVelocity = 1

        #zeroes out velocity if the player is on the ground
        if Character.Pos.newCollisionCheck()[4] == 1 or Character.characterLocation[1] > 950:
            yVelocity = 0
            if realYVel > 2.5:
                Character.health-=realYVel*6
            realYVel = 0



        #keyboard input
        for event in ev:
            if event.type == pg.KEYDOWN:
                #opens inventory
                if keyboardInput[pg.K_TAB]:
                    Inventory.open = not Inventory.open
                #jump
                if keyboardInput[pg.K_SPACE]:
                    if Character.Pos.newCollisionCheck()[4] == 1:
                        yVelocity -= 0.15*World.deltaTime
                #block interaction
                if keyboardInput[K_e]:
                    if Inventory.craftingTableOpen == True:
                        Inventory.craftingTableOpen = False
                    elif Block.Grid.getBlockAtLocation((ForeGround.getMousePos()[0],ForeGround.getMousePos()[1])) == Block.Type.BlockType.craftingTable:
                        if Inventory.craftingTableOpen == False:
                            Inventory.craftingTableOpen = True
                            Inventory.activeCraftingTableCoords = [Character.characterLocation[0],Character.characterLocation[1]]
                    if Block.Grid.getBlockAtLocation((ForeGround.getMousePos()[0],ForeGround.getMousePos()[1])) == Block.Type.BlockType.chest:
                        if Inventory.chestOpen == True:
                                Inventory.chestOpen = False
                        else:
                            for i in Inventory.containers:
                                if i.position[0] == Block.Grid.translateToBlockCoords(ForeGround.getMousePos())[0] and i.position[1] == Block.Grid.translateToBlockCoords(ForeGround.getMousePos())[1]:
                                    activeContainer = i
                                    Inventory.chestOpen = True
                                    break
                    blockPressed = Block.Grid.getBlockAtLocation((ForeGround.getMousePos()[0],ForeGround.getMousePos()[1]))
                    if blockPressed == Block.Type.BlockType.doorBottom or blockPressed == Block.Type.BlockType.doorTop or blockPressed == Block.Type.BlockType.doorOpen:
                        InteractionHandler.doorHandler()
                        
                                
                    
        #head hitbox velocity cancelation
        if Character.Pos.newCollisionCheck()[5] == 1:
            if yVelocity < 0:
                yVelocity = 0

        #does input for player movement
        Character.Input.inputKey(keyboardInput,iterNum,entities)

        #updates coords for player
        Character.Pos.updateDrawCoords((windowW,windowH))
        Character.Pos.update()
        #draw character at the end AFTER(DO NOT FORGOR💀) setting game logic for position
        Character.Render.drawStillX(ForeGround.display,Character.characterImage)
        for i in range(10):
            if Character.Pos.newCollisionCheck()[4] == 1 and yVelocity > 0:
                break
            Character.characterLocation[1] += yVelocity*0.1

        """
        hud/inventory code
        """
        if Inventory.chestOpen == True:
            InteractionHandler.chestHandler(activeContainer,ev)

        #cragting table stuff
        if Inventory.craftingTableOpen == True:
            InteractionHandler.craftingHandler(ev)

        if (Character.characterLocation[0]-Inventory.activeCraftingTableCoords[0]) > 5 or (Character.characterLocation[0]-Inventory.activeCraftingTableCoords[0]) <-5 or (Character.characterLocation[1]-Inventory.activeCraftingTableCoords[1]) > 5 or (Character.characterLocation[1]-Inventory.activeCraftingTableCoords[1]) <-5:
            Inventory.craftingTableOpen = False


        if Inventory.selectedSlot != None and Inventory.stackAmount[0][Inventory.selectedSlot] <= 0:
            Inventory.grid[0][Inventory.selectedSlot] = Items.Id.empty
            Inventory.stackAmount[0][Inventory.selectedSlot] = 0

        #hud rendering code
        if Inventory.open == True:
            ForeGround.display.blit(Gui.saveButton,(725,725))
            ForeGround.display.blit(Gui.exitToMenuButton,(725,665))
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
        #draw health bar
        healthBgRect = pg.Rect(630,20,150,20)
        healthRect = pg.Rect(630,20,Character.health*1.5,20)

        pg.draw.rect(ForeGround.display,(255,0,0),healthBgRect)
        pg.draw.rect(ForeGround.display,(50,255,10),healthRect)
        

        """
        entity logic
        """
        #iterates through all entites to check for player collision with them
        for i in range(len(entities)):
            try:
                ForeGround.display.blit(Items.iconList[entities[i].id],(entities[i].drawCoordinates))
                entities[i].update()
                entities[i].gravityUpdate()

                if Character.characterBoundingBox.colliderect(entities[i].boundingBox):
                    for g in range(entities[i].stackSize):
                        Inventory.addItem(entities[i].id)
                    deleteEnt(i,entities)
            except Exception as e:
                pass

        #gives player 100 of every block(debug)
        for event in ev:
            if event.type == pg.KEYDOWN:
                if keyboardInput[pg.K_q]:
                    Inventory.dropItem(Inventory.selectedSlot,entities)
                if keyboardInput[pg.K_x]:
                    if placingMatrix == "foreground":
                        placingMatrix = "background"
                    else:
                        placingMatrix = "foreground"
                if keyboardInput[pg.K_k]:
                    for i in range(100):
                        Inventory.addItem(Items.Id.stone)
                        Inventory.addItem(Items.Id.dirt)
                        Inventory.addItem(Items.Id.grass)
                        Inventory.addItem(Items.Id.sand)
                        Inventory.addItem(Items.Id.wood)
                        Inventory.addItem(Items.Id.log)
                        Inventory.addItem(Items.Id.leaves)
                        Inventory.addItem(Items.Id.craftingTable)
                        Inventory.addItem(Items.Id.chest)
                        Inventory.addItem(Items.Id.glowBlock)
                        Inventory.addItem(Items.Id.glass)
                        Inventory.addItem(Items.Id.door)



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
        windowWlast, windowHlast = pygame.display.get_surface().get_size()
        pg.display.flip()

