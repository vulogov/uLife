##
##
##

import random
import time
from tabulate import tabulate

MAXAGE   = 120 ## Maximum age of cell, reaching it, cell dies of old age
MAXEMPTY = 15  ## Maximum age of empty cell, reaching it cell may go to life

class Cell:
    def __init__(self, x, y, xsize, ysize):
        self.x       = x
        self.y       = y
        self.xsize   = xsize
        self.ysize   = ysize
        self.status  = 0
        self.step    = 0
        self.age     = 0
        self.changed = False
        self.eimmune = random.randint(1,10)
        self.cimmune = random.randint(1,10)
    def __repr__(self):
        s = "DEAD" if self.status == 0 else "LIVE"
        return "%s(%d:%d)[%d,%d]=%d"%(s, self.x, self.y, self.eimmune, self.cimmune, self.age)
    def ToLife(self):
        self.age     = 0
        self.status  = 1
        self.eimmune = random.randint(1,10)
        self.cimmune = random.randint(1,10)
        self.changed = True
    def CreateLife(self):
        if not self.Alive() and self.age > MAXEMPTY:
            dice = random.randint(0,1)
            if dice == 0:
                self.ToLife()
    def Death(self):
        self.age     = 0
        self.status  = 0
        self.eimmune = 0
        self.cimmune = 0
        self.changed = True
    def EmptyDeath(self):
        self.changed = False
        self.eimmune -= 1
        if self.eimmune == 0:
            self.Death()

    def CrowdDeath(self):
        self.changed = False
        self.cimmune -= 1
        if self.cimmune == 0:
            self.Death()

    def OldAgeDeath(self):
        self.changed = False
        if self.age > MAXAGE:
            self.Death()

    def Alive(self):
        return True if self.status == 1 else False

class World:
    def __init__(self, xsize, ysize):
        self.xsize   = xsize
        self.ysize   = ysize
        self.cells   = {}
        self.__initcells__()
    def __initcells__(self):
        for i in range(0,self.xsize):
            for j in range(0, self.ysize):
                self.cells[(i,j)] = Cell(i,j,self.xsize, self.ysize)
    def neighbors(self, x, y):
        c = self.cells[(x,y)]
        n = []
        if x == 0:
            x1 = self.xsize-1
            x2 = x + 1
        else:
            x1 = x - 1
            x2 = x + 1
            if x2 == self.xsize:
                x2 = 0
        if y == 0:
            y1 = self.ysize-1
            y2 = y + 1
        else:
            y1 = y - 1
            y2 = y + 1
            if y2 == self.ysize:
                y2 = 0
        n.append(self.cells[(x1,y)])
        n.append(self.cells[(x1,y1)])
        n.append(self.cells[(x,y1)])
        n.append(self.cells[(x2,y1)])
        n.append(self.cells[(x2,y)])
        n.append(self.cells[(x2,y2)])
        n.append(self.cells[(x,y2)])
        n.append(self.cells[(x1,y2)])
        return (c,n)
    def Step(self):
        for i in range(0,self.xsize):
            for j in range(0, self.ysize):
                c, n = self.neighbors(i,j)
                c.changed = False
                c.age += 1
                if c.Alive():
                    c.OldAgeDeath()
                if c.changed:
                    continue
                c.CreateLife()
                if c.changed:
                    continue
                alive_neighbors = 0
                for neighbor in n:
                    if neighbor.Alive():
                        alive_neighbors += 1
                if not c.Alive() and alive_neighbors == 3:
                    c.ToLife()
                    continue
                if c.Alive() and alive_neighbors < 2:
                    c.EmptyDeath()
                    continue
                if c.Alive() and alive_neighbors > 3:
                    c.CrowdDeath()
                    continue
    def __call__(self, x,y):
        return self.cells[(x,y)]
    def ToLife(self, *args):
        for c in args:
            cell = self(c[0], c[1])
            cell.ToLife()
    def __repr__(self):
        t = []
        for i in range(0,self.xsize):
            r = []
            for j in range(0, self.ysize):
                r.append(str(self(i,j)))
            t.append(r)
        return str(tabulate(t))

w = World(8,8)
w.ToLife((0,0), (0,1), (1,1), (1,2), (1,3), (0,2))
while True:
    print(w)
    w.Step()
    time.sleep(2)
