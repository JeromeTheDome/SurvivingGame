import pygame as pg
from gameWindow import ForeGround, Block
from inventory import Inventory

class PlaceLogic():
    def default(): #default logic for placing a door
        Block.Grid.placeBlock((ForeGround.getMousePos()[0],ForeGround.getMousePos()[1]),Inventory.grid[0][Inventory.selectedSlot])
    
    def door():
        if Block.Grid.getBlockAtLocation((ForeGround.getMousePos()[0],ForeGround.getMousePos()[1]),1,(0,-1)) == Block.Type.BlockType.air:
            Block.Grid.placeBlock((ForeGround.getMousePos()[0],ForeGround.getMousePos()[1]),Inventory.grid[0][Inventory.selectedSlot])
            Block.Grid.placeBlock((ForeGround.getMousePos()[0],ForeGround.getMousePos()[1]),(Inventory.grid[0][Inventory.selectedSlot])-1,False,(0,-1))

blockPlaceLogicTable = {
    Block.Type.BlockType.doorBottom:PlaceLogic.door,
    "default":PlaceLogic.default,
}