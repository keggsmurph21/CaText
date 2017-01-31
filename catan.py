from graphics import *

import random
import sys
import math
import itertools

BACKGROUND_COLOR = color_rgb(60, 130, 230)
EDGE_SIZE = 35
RESOURCE_COLOR_LOOKUP = {
    "desert" : color_rgb(230,230,230),
    "ore"    : color_rgb(50,50,60),
    "brick"  : color_rgb(220,120,60),
    "wool"   : color_rgb(140,210,40),
    "grain"  : color_rgb(255,210,0),
    "lumber" : color_rgb(40,120,30),
    "mystery": color_rgb(255,255,255) }
ADJACENT_NODES = [
    ("E","SE"),
    ("SE","E"),
    ("SE","SW"),
    ("SW","SE"),
    ("SW","W"),
    ("W","SW"),
    ("W","NW"),
    ("NW","W"),
    ("NW","NE"),
    ("NE","NW"),
    ("NE","E"),
    ("E","NE") ]
PLAYER_COLORS_LOOKUP = {
    0 : color_rgb(255,20,0),
    1 : color_rgb(0,10,255),
    2 : color_rgb(220,70,70),
    3 : color_rgb(170,100,40) }

class Catan(object):
    def __init__(self, filename, humanplayers, cpuplayers):
        self.window = GraphWin("Catan", 640, 480)
        self.window.setBackground(BACKGROUND_COLOR)
        self.center = Point(320,240)

        self.board = None
        self.filename = filename

        self.players = Players(self.window, humanplayers, cpuplayers)

        self.buildBoard() # eventually add error handling here

    def getNearby(self, click):
        tileDistances = []

        for t in self.board.tiles:
            tileDistances.append(distance(click, t.getCenter()))
        tileID = tileDistances.index(min(tileDistances))
        tile = self.getTile(tileID)

        dist = 640

        for n in self.board.nodes:
            if distance(click, n.getCenter()) < dist:
                node = n
                dist = distance(click, n.getCenter())

        dist = 640

        for e in self.board.edges:
            if distance(click, e.getCenter()) < dist:
                edge = e
                dist = distance(click, e.getCenter())

        return (tile, node, edge)

    def getAdjNodesFromTile(self, tile):
        nodes = set()
        for node in self.board.nodes:
            if distance(node.getCenter(), tile.getCenter()) < EDGE_SIZE * 1.1:
                nodes.add(node)

        return nodes

    def getAdjEdgesFromTile(self, tile):
        edges = set()
        for edge in self.board.edges:
            if distance(edge.getCenter(), tile.getCenter()) < EDGE_SIZE:
                edges.add(edge)

        return edges

    def getAdjEdgesFromNode(self, node):
        edges = set()
        for edge in self.board.edges:
            if distance(edge.getCenter(), node.getCenter()) < EDGE_SIZE * 0.9:
                edges.add(edge)

        return edges

    def play(self):
        while 1:
            click = self.window.getMouse()
            print click.getX(), click.getY()
        self.window.close()

    def getDesert(self):
        for t in self.board.tiles:
            if type(t) == Resource:
                if t.label == "desert":
                    return t

    def moveRobber(self, tile):
        self.board.robber.move(tile)

    def getRobber(self):
        return self.board.robber.id

    def collectResource(self, id):
        if self.getRobber != id:
            pass

    def getTile(self, id):
        for tile in self.board.tiles:
            if tile.id == id:
                return tile

    def getNode(self, a, b, c):
        indices = [a,b,c]
        indices.sort()
        check = [self.getTile(x) for x in indices]

        for node in self.board.nodes:
            neighbors = node.getNeighbors().values()
            neighbors.sort()
            if neighbors == check:
                return node

    def buildBoard(self):
        with open(self.filename) as f:
            content = f.readlines()

        content = [x.strip() for x in content]
        boardSetupID = content.index("BOARD SETUP")
        resourcesID = content.index("RESOURCES")
        dicerollsID = content.index("DICE ROLLS")
        numberOfTiles = resourcesID - boardSetupID - 1
        self.board = Board(self.window)
        self.board.tiles = [None for t in range(numberOfTiles)]

        for r in content[boardSetupID + 1 : resourcesID]:
            row = r.split(" ")
            t = int(row[0])
            tiletype = row[9]
            x = self.center.getX() + math.sqrt(3) * EDGE_SIZE * float(row[7])
            y = self.center.getY() + 1.5 * EDGE_SIZE * float(row[8])

            if tiletype == "harbor":
                self.board.tiles[t] = Harbor(self.window, x, y, int(row[10]), row[11])
            elif tiletype == "water":
                self.board.tiles[t] = Water(self.window, x, y)
            elif tiletype == "resource":
                self.board.tiles[t] = Resource(self.window, x, y, color_rgb(255,255,255), 0)

            self.board.tiles[t].id = t

            self.board.tiles[t].W  = row[1]
            self.board.tiles[t].NW = row[2]
            self.board.tiles[t].NE = row[3]
            self.board.tiles[t].E  = row[4]
            self.board.tiles[t].SE = row[5]
            self.board.tiles[t].SW = row[6]

        resources = []

        for r in content[resourcesID + 1 : dicerollsID]:
            frequency = int(r.split(" ")[0])
            r = r.split(" ")[1]

            for f in range(frequency):
                resources.append(r)

        random.shuffle(resources)
        i = random.randint(0,11)

        dicerolls = content[dicerollsID + 1].split(",")
        dicerolls = dicerolls[i:] + dicerolls[:i]
        dicerolls = [int(x) for x in dicerolls]
        dicerollMatches = content[dicerollsID + 2].split(",")
        dicerollMatches = [int(x) for x in dicerollMatches]

        for t in self.board.tiles:
            if type(t) == Resource:
                resource = resources.pop(0)
                t.label = resource
                t.color = RESOURCE_COLOR_LOOKUP[resource]
            elif type(t) == Harbor:
                t.harborTile = self.getTile(t.harborTile)

        for d in dicerollMatches:
            if self.board.tiles[d].label != "desert":
                self.board.tiles[d].diceroll = dicerolls.pop(0)

        for t in self.board.tiles:
            t.placeOnBoard()

        # Build edges
        for t in self.board.tiles:
            neighbors = t.getNeighbors()
            for n in neighbors:
                if neighbors[n] == "x":
                    pass
                else:
                    neighbor = self.getTile(int(neighbors[n]))
                    if type(neighbor) == Resource or type(t) == Resource:
                        if t.id < neighbor.id:
                            edge = Edge(self.window, t, neighbor)
                        else:
                            edge = Edge(self.window, neighbor, t)
                        self.board.edges.add(edge)

        # Build nodes
        for t in self.board.tiles:
            neighbors = t.getNeighbors()
            combos = set(itertools.combinations(neighbors,2))

            for combo in combos:
                count = 0
                for n in combo:
                    if neighbors[n] == "x":
                        count += 1
                if count == 0 and combo in ADJACENT_NODES:
                    indices = [int(neighbors[n]) for n in combo]
                    indices.append(t.id)
                    indices.sort()

                    north = sum([i%2 for i in indices])%2 + 1

                    a = self.getTile(indices[0])
                    b = self.getTile(indices[1])
                    c = self.getTile(indices[2])

                    node = Node(self.window, north, a, b, c)

                    self.board.nodes.add(node)

        desert = self.getDesert()
        self.moveRobber(desert)

        while 1:
            click = self.window.getMouse()
            tile = self.getNearby(click)[0]
            nodes = self.getAdjNodesFromTile(tile)
            for n in nodes:
                n.node.draw(self.window)
                edges = self.getAdjEdgesFromNode(n)
                for e in edges:
                    print len(edges), "edge"
                    e.line.setFill(randomColor())
class Robber(object):
    def __init__(self, window, x, y):
        self.window = window
        self.robber = Circle(Point(x,y), 12)
        self.robber.setOutline(color_rgb(0,0,0))
        self.robber.setWidth(5)
        self.id = 0

    def move(self, tile):
        if type(tile) == Resource:
            self.robber.undraw()
            self.robber = Circle(Point(tile.x, tile.y), 12)
            self.robber.setWidth(5)
            self.robber.draw(self.window)
            self.id = tile.id
        else:
            print "Unable to move Robber here."

class DevCards(object):
    def __init__(self):
        self.deck = []
        for i in range(14):
            self.deck.append(DevCard("knight"))
        for i in range(5):
            self.deck.append(DevCard("victory point"))
        for i in range(2):
            self.deck.append(DevCard("road building"))
        for i in range(2):
            self.deck.append(DevCard("year of plenty"))
        for i in range(2):
            self.deck.append(DevCard("monopoly"))

class DevCard(object):
    def __init__(self, type):
        self.type = type

class Dice(object):
    def __init__(self, window):
        self.one = Die(window, 630,20,590,60)
        self.two = Die(window, 580,20,540,60)

    def roll(self):
        self.one.roll()
        self.two.roll()
        return self.one.value + self.two.value

class Die(object):
    def __init__(self, window, x1, y1, x2, y2):
        self.window = window
        self.value = 0
        self.die = Rectangle(Point(x1,y1), Point(x2,y2))
        self.die.setFill(color_rgb(200,69,69))
        self.die.setOutline(color_rgb(0,0,0))
        self.die.setWidth(2)
        self.die.draw(self.window)

        self.text = Text(self.die.getCenter(), "")
        self.text.setSize(20)
        self.text.draw(self.window)

    def roll(self):
        self.value = random.randint(1,6)
        self.text.setText(str(self.value))

class Tile(object):
    def base(self, color=BACKGROUND_COLOR, outline="black", outlineWidth=0):
        self.color = color
        self.outline = outline
        self.outlineWidth = outlineWidth
        self.diceroll = 0
        self.id = None

        self.W  = None # neighbors of the hex
        self.NW = None
        self.NE = None
        self.E  = None
        self.SE = None
        self.SW = None

        self.hex = None

    def getCenter(self):
        xTotal = 0.0
        yTotal = 0.0
        numPoints = 0

        for point in self.hex.getPoints():
            xTotal += point.getX()
            yTotal += point.getY()
            numPoints += 1

        return Point(xTotal/numPoints, yTotal/numPoints)

    def getNeighbors(self):
        neighbors = {}
        neighbors["W"]  = self.W
        neighbors["NW"] = self.NW
        neighbors["NE"] = self.NE
        neighbors["E"]  = self.E
        neighbors["SE"] = self.SE
        neighbors["SW"] = self.SW
        return neighbors

    def placeOnBoard(self):
        x = self.x
        y = self.y

        self.hex = Polygon(
            Point(x - math.sqrt(3)/2 * EDGE_SIZE, y - 1.0/2 * EDGE_SIZE),
            Point(x - math.sqrt(3)/2 * EDGE_SIZE, y + 1.0/2 * EDGE_SIZE),
            Point(x, y + EDGE_SIZE),
            Point(x + math.sqrt(3)/2 * EDGE_SIZE, y + 1.0/2 * EDGE_SIZE),
            Point(x + math.sqrt(3)/2 * EDGE_SIZE, y - 1.0/2 * EDGE_SIZE),
            Point(x, y - EDGE_SIZE))

        self.hex.setFill(self.color)
        self.hex.setWidth(2)
        self.hex.setOutline(self.outline)
        self.hex.draw(self.window)

        if self.diceroll != 0:
            self.text = Text(Point(x,y), self.diceroll)
            self.text.draw(self.window)

        if type(self) == Harbor:
            self.placeHarbor()

class Harbor(Tile):
    def __init__(self, window, x, y, harborTile, harborType):
        self.base(BACKGROUND_COLOR)
        self.window = window
        self.harborTile = harborTile
        self.harborType = harborType
        self.x = x
        self.y = y
        self.harbor = None

    def placeHarbor(self):
        self.harborTile.harbor = self.harborType

        p1 = Point(self.x, self.y)
        bisect = Line(p1, Point(self.harborTile.x, self.harborTile.y))
        pb = bisect.getCenter()

        if p1.getY() == pb.getY():
            p2 = Point(pb.getX(), pb.getY() + EDGE_SIZE * 1.0/2)
            p3 = Point(pb.getX(), pb.getY() - EDGE_SIZE * 1.0/2)
        elif p1.getY() < pb.getY():
            p2 = Point(p1.getX(), p1.getY() + EDGE_SIZE)
            p3 = Point(self.harborTile.x, self.harborTile.y - EDGE_SIZE)
        else:
            p2 = Point(self.harborTile.x, self.harborTile.y + EDGE_SIZE)
            p3 = Point(p1.getX(), p1.getY() - EDGE_SIZE)

        bisect = Line(p1,pb)
        p1 = bisect.getCenter()

        self.harbor = Polygon(p1,p2,p3)
        self.harbor.setOutline(BACKGROUND_COLOR)
        self.harbor.setFill(RESOURCE_COLOR_LOOKUP[self.harborType])
        self.harbor.draw(self.window)

class Water(Tile):
    def __init__(self, window, x, y):
        self.base()
        self.window = window
        self.x = x
        self.y = y

class Resource(Tile):
    def __init__(self, window, x, y, color, label, visible=True):
        self.base("white")
        self.window = window
        self.x = x
        self.y = y
        self.harbor = None

        self.color = color
        self.label = label
        self.visible = visible # for future compatibility with expansion packs
        self.image = None
        self.diceroll = 0
        self.outline = BACKGROUND_COLOR
        self.outlineWidth = 1

        self.text = None # also a Graphics object, holds the dice roll

class Players(object):
    def __init__(self, window, humans, cpus):
        self.window = window
        self.players = set()
        for i in range(humans):
            self.players.add(HumanPlayer(len(self.players)))
        for i in range(cpus):
            self.players.add(CPUPlayer(len(self.players)))

    def adjustOrder(self,a,b,c,d):
        temp = [self.players[a], self.players[b], self.players[c], self.players[d]]
        self.players = temp
        for p in self.players:
            p.textbox.undraw()
            p.textbox.draw(self.window)

class Player(object):
    def super_init(self, id):
        self.id = id
        self.color = PLAYER_COLORS_LOOKUP[id]
        self.name = ""

        self.resources = set()
        self.devcards = set()
        self.settlements = set()
        self.roads = set()

        self.next = None

class HumanPlayer(Player):
    def __init__(self, id):
        self.super_init(id)
        self.name = "Player " + str(id+1)

class CPUPlayer(Player):
    def __init__(self, id):
        self.super_init(id)
        self.name = "Player " + str(id+1) + " (CPU)"

class Board(object):
    def __init__(self, window):
        self.window = window
        self.tiles = []
        self.nodes = set()
        self.edges = set()
        self.dice = Dice(window)
        self.devcards = DevCards()
        self.robber = Robber(window, 0, 0)

class Node(object):
    def __init__(self, window, north, a, b, c):
        self.window = window
        self.owner = None
        self.isCity = False
        self.color = None
        self.north = north
        self.settlable = True

        if north:
            self.N  = a
            self.SE = b
            self.SW = c
        else:
            self.NW = a
            self.NE = b
            self.S  + c

        aPoints = a.hex.getPoints()
        aCenter = Line(aPoints[0],aPoints[3]).getCenter()
        bPoints = b.hex.getPoints()
        bCenter = Line(bPoints[0],bPoints[3]).getCenter()
        cPoints = c.hex.getPoints()
        cCenter = Line(cPoints[0],cPoints[3]).getCenter()

        self.x = (aCenter.getX() + bCenter.getX() + cCenter.getX())/3.0
        self.y = (aCenter.getY() + bCenter.getY() + cCenter.getY())/3.0
        self.node = Circle(Point(self.x, self.y), EDGE_SIZE * 1.0/4)
        self.node.setFill("white")

    def getCenter(self):
        return self.node.getCenter()

    def getNeighbors(self):
        neighbors = {}
        if self.north:
            neighbors["N"]  = self.N
            neighbors["SE"] = self.SE
            neighbors["SW"] = self.SW
        else:
            neighbors["NW"] = self.NW
            neighbors["NE"] = self.NE
            neighbors["S"]  = self.S
        return neighbors

    def show(self):
        self.node.draw(self.window)

    def hide(self):
        self.node.undraw()

    def settle(self, owner):
        self.owner = owner
        self.color = owner.getColor()

class Edge(object):
    def __init__(self, window, source, target):
        self.window = window
        self.source = source
        self.target = target
        self.owner = None

        if source.y == target.y:
            self.y1 = source.y - EDGE_SIZE * 1.0/2
            self.y2 = target.y + EDGE_SIZE * 1.0/2

            if source.x < target.x:
                self.x1 = source.x + EDGE_SIZE * math.sqrt(3)/2
                self.x2 = target.x - EDGE_SIZE * math.sqrt(3)/2
            else:
                self.x1 = source.x - EDGE_SIZE * math.sqrt(3)/2
                self.x2 = target.x + EDGE_SIZE * math.sqrt(3)/2

        else:
            self.x1 = source.x
            self.x2 = target.x

            if source.y < target.y:
                self.y1 = source.y + EDGE_SIZE
                self.y2 = target.y - EDGE_SIZE
            else:
                self.y1 = source.y - EDGE_SIZE
                self.y2 = target.y + EDGE_SIZE

        self.line = Line(Point(self.x1,self.y1), Point(self.x2,self.y2))
        self.line.setWidth(3)
        self.line.setFill("white")
        self.line.draw(self.window)

    def getCenter(self):
        xTotal = self.line.getP1().getX() + self.line.getP2().getX()
        yTotal = self.line.getP1().getY() + self.line.getP2().getY()

        return Point(xTotal/2.0, yTotal/2.0)

def distance(p1, p2):
    return math.sqrt((p1.getX() - p2.getX())**2 + (p1.getY() - p2.getY())**2)

def randomColor():
    return color_rgb(random.randint(0,255),random.randint(0,255),random.randint(0,255))

def main():
    if (sys.argv != None):
        filename = sys.argv[1]
        humanplayers = int(sys.argv[2])
        cpuplayers = int(sys.argv[3])
    else:
        print "Please provide a map and the number of humans/CPUs."

    catan = Catan(filename, humanplayers, cpuplayers)
    catan.play()

if __name__ == "__main__":
    main()
