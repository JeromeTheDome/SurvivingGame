
class Container():
    def __init__(self,pos,containerType,grid = None,stackGrid = None):
        self.position = [pos[0],pos[1]]
        self.type = containerType
        if grid != None and stackGrid != None:
            self.grid = grid
            self.stackGrid = stackGrid
        elif self.type == 1:
            self.grid = [[0 for i in range(9)]for i in range(5)]
            self.stackGrid = [[0 for i in range(9)]for i in range(5)]