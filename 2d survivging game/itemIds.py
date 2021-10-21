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
            log = 6
            leaves = 7
            #51 to 100 reserved for tools
            defaultPick = 51
            defaultAxe = 52
            defaultShovel = 53
            #101 and up is for other items
            lastentry = 101

    #assigns icons to each item id
    #blocks
    iconList = [pg.image] * Id.lastentry
    iconList[Id.empty] = pg.image.load("./Images/Item Icons/empty.png").convert_alpha()
    iconList[Id.stone] = pg.image.load("./Images/Item Icons/stoneIcon.png").convert_alpha()
    iconList[Id.dirt] = pg.image.load("./Images/Item Icons/dirtIcon.png").convert_alpha()
    iconList[Id.grass] = pg.image.load("./Images/Item Icons/grassIcon.png").convert_alpha()
    iconList[Id.sand] = pg.image.load("./Images/Item Icons/sandIcon.png").convert_alpha()
    iconList[Id.wood] = pg.image.load("./Images/Item Icons/woodIcon.png").convert_alpha()
    iconList[Id.log] = pg.image.load("./Images/Item Icons/logIcon.png").convert_alpha()
    iconList[Id.leaves] = pg.image.load("./Images/Item Icons/leavesIcon.png").convert_alpha()
    #tools/weapons
    iconList[Id.defaultPick] = pg.image.load("./Images/Item Icons/pickaxe.png").convert_alpha()
    iconList[Id.defaultAxe] = pg.image.load("./Images/Item Icons/axe.png").convert_alpha()
    iconList[Id.defaultShovel] = pg.image.load("./Images/Item Icons/shovel.png").convert_alpha()