from enum import IntEnum
import pygame as pg

class Items():
    #defines item ids
    class Id(IntEnum):
            #blocks reserved for any given purpose
           # reserved = []


            empty = 0
            #item ids 1 to 50 are reserved for blocks. blocks item ids are identical to block ids
            stone = 1
            dirt = 2
            grass = 3
            sand = 4
            wood = 5
            log = 6
            leaves = 7
            craftingTable = 8
            chest = 9
            glowBlock = 10
            glass = 11
            reserved = 12
            door = 13
            #51 to 100 reserved for tools
            defaultPick = 51
            defaultAxe = 52
            defaultShovel = 53
            #101 and up is for other items
            toolHandle = 101
            lastentry = 102

    #assigns icons to each item id
    #blocks
    iconList = [pg.image] * Id.lastentry
    iconList[Id.empty] = pg.image.load("./Images/Item Icons/empty.png").convert_alpha()
    iconList[Id.stone] = pg.image.load("./Images/Item Icons/stoneIcon.png").convert()
    iconList[Id.dirt] = pg.image.load("./Images/Item Icons/dirtIcon.png").convert()
    iconList[Id.grass] = pg.image.load("./Images/Item Icons/grassIcon.png").convert()
    iconList[Id.sand] = pg.image.load("./Images/Item Icons/sandIcon.png").convert()
    iconList[Id.wood] = pg.image.load("./Images/Item Icons/woodIcon.png").convert()
    iconList[Id.log] = pg.image.load("./Images/Item Icons/logIcon.png").convert()
    iconList[Id.leaves] = pg.image.load("./Images/Item Icons/leavesIcon.png").convert_alpha()
    iconList[Id.craftingTable] = pg.image.load("./Images/Item Icons/craftingTableIcon.png").convert()
    iconList[Id.chest] = pg.image.load("./Images/Item Icons/chestIcon.png").convert()
    iconList[Id.glowBlock] = pg.image.load("./Images/Item Icons/glowBlockIcon.png").convert()
    iconList[Id.glass] = pg.image.load("./Images/Item Icons/glassIcon.png").convert()
    iconList[Id.door] = pg.image.load("./Images/Item Icons/doorIcon.png").convert()
    #tools/weapons
    iconList[Id.defaultPick] = pg.image.load("./Images/Item Icons/pickaxe.png").convert_alpha()
    iconList[Id.defaultAxe] = pg.image.load("./Images/Item Icons/axe.png").convert_alpha()
    iconList[Id.defaultShovel] = pg.image.load("./Images/Item Icons/shovel.png").convert_alpha()
    #other items
    iconList[Id.toolHandle] = pg.image.load("./Images/Item Icons/toolHandle.png").convert_alpha()
    
    #set colorkeys
    iconList[Id.glass].set_colorkey((255,0,255))
    iconList[Id.door].set_colorkey((255,0,255))