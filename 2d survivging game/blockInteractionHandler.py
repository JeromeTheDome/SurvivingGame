from gameWindow import Block,ForeGround
from inventory import Inventory
from CharacterFile import Character
from itemIds import Items
import craftingRecipies
import pygame as pg

myfont = pg.font.SysFont('Comic Sans MS', 18)

class InteractionHandler():
    def chestHandler(activeContainer,frameEvents):
        #logic for if a chest is opened
        if activeContainer.position[0]-Character.characterLocation[0] < 5 or activeContainer.position[0]-Character.characterLocation[0] > 20: #or activeContainer.position[1]-Character.characterLocation[1] < 10 or activeContainer.position[1]-Character.characterLocation[1] > 20:
            Inventory.chestOpen = False
        #checks for interaction with chest grid
        for y in range(len(activeContainer.grid)):
            for x in range(len(activeContainer.grid[0])):
                chestBoxRect = pg.Rect(((x*48),(y*48+288)),(48,48))
                Inventory.Render.renderBox(((x*48),(y*48+288)),activeContainer.grid[y][x])
                ForeGround.display.blit(myfont.render(str(activeContainer.stackGrid[y][x]), False, (150, 150, 150)),((x*48)+30,(y*48+288)+24))
                for event in frameEvents:
                    #mouse input
                    if event.type == pg.MOUSEBUTTONDOWN:
                        if pg.mouse.get_pressed(3) == (True,False,False) and chestBoxRect.collidepoint(ForeGround.getMousePos()[0],ForeGround.getMousePos()[1]):
                            if activeContainer.grid[y][x] != Inventory.itemOnCursor:
                                temporaryItem = Inventory.itemOnCursor
                                temporaryItemCount = Inventory.itemCountOnCursor

                                Inventory.itemCountOnCursor = activeContainer.stackGrid[y][x]
                                Inventory.itemOnCursor = activeContainer.grid[y][x]

                                activeContainer.stackGrid[y][x] = temporaryItemCount
                                activeContainer.grid[y][x] = temporaryItem
                            elif Inventory.itemOnCursor == activeContainer.grid[y][x]:
                                    for i in range(Inventory.itemCountOnCursor):
                                        if activeContainer.stackGrid[y][x] < 100:
                                            activeContainer.stackGrid[y][x] += 1
                                            Inventory.itemCountOnCursor -= 1
                                        else:
                                            break
                                    if Inventory.itemCountOnCursor <= 0:
                                        Inventory.itemOnCursor = Items.Id.empty

                        if pg.mouse.get_pressed(3) == (False,True,False) and chestBoxRect.collidepoint(ForeGround.getMousePos()[0],ForeGround.getMousePos()[1]):
                            if Inventory.itemOnCursor == Items.Id.empty:
                                activeContainer.stackGrid[y][x] -= 1
                                Inventory.itemOnCursor = activeContainer.grid[y][x]
                                Inventory.itemCountOnCursor += 1
                                if activeContainer.stackGrid[y][x] <= 0:
                                    activeContainer.grid[y][x] = Items.Id.empty

                            elif Inventory.itemOnCursor == activeContainer.grid[y][x]:
                                activeContainer.stackGrid[y][x] -= 1
                                if activeContainer.stackGrid[y][x] <= 0:
                                    activeContainer.grid[y][x] = Items.Id.empty
                                Inventory.itemCountOnCursor += 1 
                            elif Inventory.itemOnCursor != Items.Id.empty and activeContainer.grid[y][x] == Items.Id.empty:
                                activeContainer.grid[y][x] = Inventory.itemOnCursor
                                activeContainer.stackGrid[y][x] += 1
                                Inventory.itemCountOnCursor -= 1
                                if Inventory.itemCountOnCursor <= 0:
                                    Inventory.itemOnCursor = Items.Id.empty
    def craftingHandler(frameEvents):
        #draws crafting interface and handles containers for it
            for y in range(3):
                for x in range(3):
                    craftingBoxRect = pg.Rect((x*48+500,y*48+500),(48,48))
                    Inventory.Render.renderBox(((x*48+500),(y*48+500)),Inventory.craftingTableGrid[y][x])
                    ForeGround.display.blit(myfont.render(str(Inventory.craftingTableStackAmount[y][x]), False, (150, 150, 150)),((x*48+500)+30,(y*48+500)+24))
                    for event in frameEvents:
                        if event.type == pg.MOUSEBUTTONDOWN:
                            if pg.mouse.get_pressed(3) == (True,False,False) and craftingBoxRect.collidepoint(ForeGround.getMousePos()[0],ForeGround.getMousePos()[1]):
                                temporaryItem = Inventory.itemOnCursor
                                temporaryItemCount = Inventory.itemCountOnCursor

                                Inventory.itemCountOnCursor = Inventory.craftingTableStackAmount[y][x]
                                Inventory.itemOnCursor = Inventory.craftingTableGrid[y][x]

                                Inventory.craftingTableStackAmount[y][x] = temporaryItemCount
                                Inventory.craftingTableGrid[y][x] = temporaryItem
                            if pg.mouse.get_pressed(3) == (False,True,False) and craftingBoxRect.collidepoint(ForeGround.getMousePos()[0],ForeGround.getMousePos()[1]):
                                if Inventory.itemOnCursor == Items.Id.empty:
                                    Inventory.craftingTableStackAmount[y][x] -= 1
                                    Inventory.itemOnCursor = Inventory.craftingTableGrid[y][x]
                                    Inventory.itemCountOnCursor += 1
                                    if Inventory.craftingTableStackAmount[y][x] <= 0:
                                        Inventory.craftingTableGrid[y][x] = Items.Id.empty

                                elif Inventory.itemOnCursor == Inventory.craftingTableGrid[y][x]:
                                    Inventory.craftingTableStackAmount[y][x] -= 1
                                    if Inventory.craftingTableStackAmount[y][x] <= 0:
                                        Inventory.craftingTableGrid[y][x] = Items.Id.empty
                                    Inventory.itemCountOnCursor += 1 
                                elif Inventory.itemOnCursor != Items.Id.empty and Inventory.craftingTableGrid[y][x] == Items.Id.empty:
                                    Inventory.craftingTableGrid[y][x] = Inventory.itemOnCursor
                                    Inventory.craftingTableStackAmount[y][x] += 1
                                    Inventory.itemCountOnCursor -= 1
                                    if Inventory.itemCountOnCursor <= 0:
                                        Inventory.itemOnCursor = Items.Id.empty

            #checks crafting table container against a bunch of recipies
            Inventory.craftingTableOutputBox = 0
            Inventory.craftingTableOutputAmount = 0
            for i in craftingRecipies.craftingTableRecipies:
                if Inventory.craftingTableGrid[0][0] == i[0][0] and Inventory.craftingTableGrid[0][1] == i[0][1] and Inventory.craftingTableGrid[0][2] == i[0][2]:
                    if Inventory.craftingTableGrid[1][0] == i[1][0] and Inventory.craftingTableGrid[1][1] == i[1][1] and Inventory.craftingTableGrid[1][2] == i[1][2]:
                        if Inventory.craftingTableGrid[2][0] == i[2][0] and Inventory.craftingTableGrid[2][1] == i[2][1] and Inventory.craftingTableGrid[2][2] == i[2][2]:
                            Inventory.craftingTableOutputBox = i[3][0]
                            Inventory.craftingTableOutputAmount = i[3][1]
                            break
            #does the same thing for the output box
            craftingBoxRect = pg.Rect((548,695),(48,48))
            ForeGround.display.blit(Inventory.Render.arrowDown,(554,647))
            Inventory.Render.renderBox((548,695),Inventory.craftingTableOutputBox)
            ForeGround.display.blit(myfont.render(str(Inventory.craftingTableOutputAmount), False, (150, 150, 150)),(584,719))
            for event in frameEvents:
                if event.type == pg.MOUSEBUTTONDOWN:
                    if pg.mouse.get_pressed(3) == (True,False,False) and craftingBoxRect.collidepoint(ForeGround.getMousePos()[0],ForeGround.getMousePos()[1]):
                        if Inventory.itemOnCursor == Items.Id.empty:
                            Inventory.itemCountOnCursor = Inventory.craftingTableOutputAmount
                            Inventory.itemOnCursor = Inventory.craftingTableOutputBox

                            Inventory.craftingTableOutputAmount = 0
                            Inventory.craftingTableOutputBox = 0

                        elif Inventory.itemOnCursor == Inventory.craftingTableOutputBox:
                            Inventory.itemCountOnCursor += Inventory.craftingTableOutputAmount

                            Inventory.craftingTableOutputAmount = 0
                            Inventory.craftingTableOutputBox = 0

                        for y in range(3):
                            for x in range(3):
                                if Inventory.craftingTableGrid[y][x] != Items.Id.empty:
                                    Inventory.craftingTableStackAmount[y][x] -= 1
                                    if Inventory.craftingTableStackAmount[y][x] <= 0:
                                        Inventory.craftingTableGrid[y][x] = Items.Id.empty
    def doorHandler():
        blockPressed = Block.Grid.getBlockAtLocation((ForeGround.getMousePos()[0],ForeGround.getMousePos()[1]))

        if blockPressed == Block.Type.BlockType.doorTop:
            blockBelow = Block.Grid.getBlockAtLocation((ForeGround.getMousePos()[0],ForeGround.getMousePos()[1]),1,(0,1))
            if blockBelow == Block.Type.BlockType.doorBottom:
                clickPos = Block.Grid.translateToBlockCoords((ForeGround.getMousePos()[0],ForeGround.getMousePos()[1]))
                Block.BlockMatrix[clickPos[1]][clickPos[0]] = Block.Type.BlockType.doorOpen
                Block.BlockMatrix[clickPos[1]+1][clickPos[0]] = Block.Type.BlockType.doorOpen
                
        elif blockPressed == Block.Type.BlockType.doorBottom:
            blockAbove = Block.Grid.getBlockAtLocation((ForeGround.getMousePos()[0],ForeGround.getMousePos()[1]),1,(0,-1))
            if blockAbove == Block.Type.BlockType.doorTop:
                clickPos = Block.Grid.translateToBlockCoords((ForeGround.getMousePos()[0],ForeGround.getMousePos()[1]))
                Block.BlockMatrix[clickPos[1]][clickPos[0]] = Block.Type.BlockType.doorOpen
                Block.BlockMatrix[clickPos[1]-1][clickPos[0]] = Block.Type.BlockType.doorOpen

        elif blockPressed == Block.Type.BlockType.doorOpen:
            blockBelow = Block.Grid.getBlockAtLocation((ForeGround.getMousePos()[0],ForeGround.getMousePos()[1]),1,(0,1))
            blockAbove = Block.Grid.getBlockAtLocation((ForeGround.getMousePos()[0],ForeGround.getMousePos()[1]),1,(0,-1))
            if blockBelow == Block.Type.BlockType.doorOpen:
                clickPos = Block.Grid.translateToBlockCoords((ForeGround.getMousePos()[0],ForeGround.getMousePos()[1]))
                Block.BlockMatrix[clickPos[1]][clickPos[0]] = Block.Type.BlockType.doorTop
                Block.BlockMatrix[clickPos[1]+1][clickPos[0]] = Block.Type.BlockType.doorBottom
            elif blockAbove == Block.Type.BlockType.doorOpen:
                clickPos = Block.Grid.translateToBlockCoords((ForeGround.getMousePos()[0],ForeGround.getMousePos()[1]))
                Block.BlockMatrix[clickPos[1]][clickPos[0]] = Block.Type.BlockType.doorBottom
                Block.BlockMatrix[clickPos[1]-1][clickPos[0]] = Block.Type.BlockType.doorTop
    def glowBlockHandler():
        x,y = Block.Grid.translateToBlockCoords((ForeGround.getMousePos()[0],ForeGround.getMousePos()[1]))
        Block.Renderer.emmisiveOveride.append([(x,y),(255,255,255),15])
        