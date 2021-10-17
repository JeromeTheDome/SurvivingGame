from enum import IntEnum
import pygame as pg

class Items():
    #defines item ids
    class Id(IntEnum):
            empty = 0
            #item ids 1 to 50 are reserved for blocks. blocks item ids are identical to block ids
            stone = 1
            dirt = 2
            grass = 3
            sand = 4
            wood = 5
            #51 to 100 reserved for tools

            #101 and up is for other items
            lastentry = 6

    #assigns icons to each item id
    iconList = [pg.image] * Id.lastentry
    iconList[Id.stone] = pg.image.load("./Images/Item Icons/stoneIcon.png")
    iconList[Id.dirt] = pg.image.load("./Images/Item Icons/dirtIcon.png")
    iconList[Id.grass] = pg.image.load("./Images/Item Icons/grassIcon.png")
    iconList[Id.sand] = pg.image.load("./Images/Item Icons/sandIcon.png")
    iconList[Id.wood] = pg.image.load("./Images/Item Icons/woodIcon.png")