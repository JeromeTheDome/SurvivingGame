from enum import intEnum
import pygame as pg

class Items():
    #defines item ids
    class Id():
            PICKAXE = 0
            lastentry = 1

    #assigns icons to each item id
    Icon = [pg.image] * BlockType.lastentry
    List[BlockType.PICKAXE] = pg.image.load("./Images/Item Icons/pickaxe.png")