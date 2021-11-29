import pygame as pg
from gameWindow import ForeGround, Block
from inventory import Inventory
from container import Container

class PlaceLogic():
    def default(layer): #default logic for placing a door
        if layer == "foreground":
            Block.Grid.placeBlock((ForeGround.getMousePos()[0],ForeGround.getMousePos()[1]),Inventory.grid[0][Inventory.selectedSlot])
        elif layer == "background":
            Block.Grid.placeBlockBg((ForeGround.getMousePos()[0],ForeGround.getMousePos()[1]),Inventory.grid[0][Inventory.selectedSlot])
        return True
    
    def door(layer):
        if layer == "foreground":
            if Block.Grid.getBlockAtLocation((ForeGround.getMousePos()[0],ForeGround.getMousePos()[1]),1,(0,-1)) == Block.Type.BlockType.air:
                Block.Grid.placeBlock((ForeGround.getMousePos()[0],ForeGround.getMousePos()[1]),Inventory.grid[0][Inventory.selectedSlot])
                Block.Grid.placeBlock((ForeGround.getMousePos()[0],ForeGround.getMousePos()[1]),(Inventory.grid[0][Inventory.selectedSlot])-1,False,(0,-1))
                return True
            else:
                return False
        elif layer == "background":
            if Block.Grid.getBlockAtLocation((ForeGround.getMousePos()[0],ForeGround.getMousePos()[1]),2,(0,-1)) == Block.Type.BlockType.air:
                Block.Grid.placeBlockBg((ForeGround.getMousePos()[0],ForeGround.getMousePos()[1]),Inventory.grid[0][Inventory.selectedSlot])
                Block.Grid.placeBlockBg((ForeGround.getMousePos()[0],ForeGround.getMousePos()[1]),(Inventory.grid[0][Inventory.selectedSlot])-1,False,(0,-1))
                return True
            else:
                return False
    def chest(layer):
        if layer == "foreground":
            Inventory.containers += [Container((Block.Grid.translateToBlockCoords(ForeGround.getMousePos())[0],Block.Grid.translateToBlockCoords(ForeGround.getMousePos())[1]),1)]
            Block.Grid.placeBlock((ForeGround.getMousePos()[0],ForeGround.getMousePos()[1]),Inventory.grid[0][Inventory.selectedSlot])
        elif layer == "background":
            Inventory.containers += [Container((Block.Grid.translateToBlockCoords(ForeGround.getMousePos())[0],Block.Grid.translateToBlockCoords(ForeGround.getMousePos())[1]),1)]
            Block.Grid.placeBlockBg((ForeGround.getMousePos()[0],ForeGround.getMousePos()[1]),Inventory.grid[0][Inventory.selectedSlot])
        return True

blockPlaceLogicTable = {
    Block.Type.BlockType.doorBottom:PlaceLogic.door,
    Block.Type.BlockType.chest:PlaceLogic.chest,
    "default":PlaceLogic.default,
}