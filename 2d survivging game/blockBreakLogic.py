import pygame as pg
from gameWindow import Block,ForeGround
from entity import Entity

class BreakLogic():
    def default(entities,layer):
        entities += [Entity(Block.Grid.translateToBlockCoords(ForeGround.getMousePos()),(16,16),0,Block.Grid.getBlockAtLocation2(Block.Grid.blockBreakingPos,layer))]
        Block.Grid.breakBlock((ForeGround.getMousePos()[0],ForeGround.getMousePos()[1]),layer)
    def glowBlock(entities,layer):
        entities += [Entity(Block.Grid.translateToBlockCoords(ForeGround.getMousePos()),(16,16),0,Block.Grid.getBlockAtLocation2(Block.Grid.blockBreakingPos,layer))]
        Block.Grid.breakBlock((ForeGround.getMousePos()[0],ForeGround.getMousePos()[1]),layer)
        mousePos = Block.Grid.translateToBlockCoords((ForeGround.getMousePos()[0],ForeGround.getMousePos()[1]))
        for i in Block.Renderer.emmisiveOveride:
            if i[0][0] == mousePos[0] and i[0][1] == mousePos[1]:
                del(i)


breakLogicLookup = {
    'default':BreakLogic.default,
    Block.Type.BlockType.glowBlock:BreakLogic.glowBlock,
}