from enum import IntEnum
import pygame as pg

class Items():
    #defines item ids
    class Id(IntEnum):
            empty = 0
            pickaxe = 1
            lastentry = 2

    #assigns icons to each item id
    iconList = [pg.image] * Id.lastentry
    iconList[Id.pickaxe] = pg.image.load("./Images/Item Icons/pickaxe.png")