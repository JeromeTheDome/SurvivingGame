import pygame as pg
from itemIds import Items

craftingTableRecipies = [
    #wood planks
    [[0,0,0],
     [0,Items.Id.log,0],
     [0,0,0],
     #output data
     [Items.Id.wood,4]],
     #crafting table
    [[Items.Id.wood,Items.Id.wood,0],
     [Items.Id.wood,Items.Id.wood,0],
     [0,0,0],
     #output data
     [Items.Id.craftingTable,1]],
     #tool handle
     [[0,0,Items.Id.wood],
     [Items.Id.wood,0,0],
     [Items.Id.wood,Items.Id.wood,0],
     #output data
     [Items.Id.toolHandle,1]],
     #chest
     [[0,0,0],
     [Items.Id.wood,0,Items.Id.wood],
     [Items.Id.wood,Items.Id.wood,Items.Id.wood],
     #output data
     [Items.Id.chest,1]]
]