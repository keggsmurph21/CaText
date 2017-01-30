from graphics import *

import random
import sys
import math

BACKGROUND_COLOR = color_rgb(60, 130, 230)
EDGE_SIZE = 30

class Catan(object):
    def __init__(self, filename):
        self.window = GraphWin("Catan", 640, 480)
        self.window.setBackground(BACKGROUND_COLOR)
        self.board = Board(self.window)
        self.filename = filename
        self.resources = []
        
        self.buildBoard() # eventually add error handling here

    def play(self):
        self.window.getMouse()
        self.window.close()

    def buildBoard(self):
        with open(self.filename) as f:
            content = f.readlines()

        content = [x.strip() for x in content]

        boardSetupID = content.index("BOARD SETUP")
        resourcesID = content.index("RESOURCES")
        dicerollsID = content.index("DICE ROLLS")

        textBoardSetup = content[boardSetupID + 1:resourcesID]
        print textBoardSetup

        textResources = content[resourcesID + 1:dicerollsID]
        for r in textResources:
            frequency = int(r.split(" ")[0])
            r = r.split(" ")[1]

            if (r == "desert"):
                res = Resource(self.window, color_rgb(250,230,60),"Desert")
            elif (r == "ore"):
                res = Resource(self.window, color_rgb(50,50,60),"Ore")
            elif (r == "brick"):
                res = Resource(self.window, color_rgb(220,120,60),"Brick")
            elif (r == "wool"):
                res = Resource(self.window, color_rgb(140,210,40),"Wool")
            elif (r == "grain"):
                res = Resource(self.window, color_rgb(210,210,30),"Grain")
            elif (r == "lumber"):
                res = Resource(self.window, color_rgb(40,120,30),"Lumber")

            for f in range(frequency):
                self.resources.append(res)

        random.shuffle(self.resources)

        dicerolls = content[dicerollsID + 1].split(",")
        i = random.randint(0,11)

        for r in self.resources:
            if (r.label != "Desert"):
                r.diceroll = dicerolls[i]
                i += 1
                i = i%len(dicerolls)

        print self.resources[6].label
        self.resources[6].placeOnBoard()

class Resource(object):
    def __init__(self, window, color, label, x=100, y=100, visible=True):
        self.window = window
        self.color = color
        self.label = label
        self.visible = visible # for future compatibility with expansion packs
        self.image = None
        self.diceroll = 0
        self.x = x
        self.y = y

        self.hex = None # the Graphics object

        self.W  = None # neighbors of the hex
        self.NW = None
        self.NE = None
        self.E  = None
        self.SE = None
        self.SW = None

    def placeOnBoard(self):
        x = self.x
        y = self.y

        self.hex = Polygon(
            Point(x, y),
            Point(x, y + EDGE_SIZE),
            Point(x + math.sqrt(3)/2 * EDGE_SIZE, y + 3.0/2 * EDGE_SIZE),
            Point(x + math.sqrt(3) * EDGE_SIZE, y + EDGE_SIZE),
            Point(x + math.sqrt(3) * EDGE_SIZE, y),
            Point(x + math.sqrt(3)/2 * EDGE_SIZE, y - 1.0/2 * EDGE_SIZE))

        self.hex.setFill(self.color)
        self.hex.setWidth(3)
        self.hex.draw(self.window)

class Player(object):
    def __init__(self):
        pass

class Board(object):
    def __init__(self, window):
        self.window = window
        self.Nodes = [Node(self.window) for i in range(55)]
        self.Edges = [Edge(self.window) for i in range(4)]

class Node(object):
    def __init__(self, window):
        self.owner = None
        self.isCity = False
        self.color = None
        #self.button = Tk.Button()

    def settle(self, owner):
        self.owner = owner
        self.color = owner.getColor()

class Tile(object):
    def __init__(self, window):
        self.window = window

class Edge(object):
    def __init__(self, window):
        self.window = window

def main():
    if (sys.argv != None):
        filename = sys.argv[1]

    catan = Catan(filename)
    catan.play()

    return 0

if __name__ == "__main__":
    main()
