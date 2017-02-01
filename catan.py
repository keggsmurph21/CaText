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
    0 : color_rgb(255,20,0),    # Red
    1 : color_rgb(0,10,255),    # Blue
    2 : color_rgb(35,140,35),   # Green
    3 : color_rgb(170,100,40) } # Brown
AI_TYPES = ["random","maximize"]
DICE_ROLL_FREQUENCIES = {
    '0' : 0,
    '2' : 1,
    '3' : 2,
    '4' : 3,
    '5' : 4,
    '6' : 5,
    '8' : 5,
    '9' : 4,
    '10': 3,
    '11': 2,
    '12': 1 }

class Catan(object):
    def __init__(self, filename, humanplayers, cpuplayers):
        self.window = GraphWin("Catan", 640, 480)
        self.window.setBackground(BACKGROUND_COLOR)
        self.center = Point(320,240)

        self.board = None
        self.buttons = []
        self.filename = filename

        self.players = Players(self.window, humanplayers, cpuplayers)
        self.turnNumber = 0

        self.buildBoard() # eventually add error handling here
        self.firstTurn()
        self.play()
        self.window.getMouse()
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
    def getEdgeBetweenNodes(self, node1, node2):
        nodes1 = self.getAdjEdgesFromNode(node1)
        nodes2 = self.getAdjEdgesFromNode(node2)

        return (nodes1 & nodes2).pop()
    def getAdjNodesFromTile(self, tile):
        nodes = []
        for node in self.board.nodes:
            if distance(node.getCenter(), tile.getCenter()) < EDGE_SIZE * 1.1:
                nodes.append(node)

        return nodes
    def getAdjNodesFromNode(self, ref):
        nodes = set()
        for node in self.board.nodes:
            if distance(node.getCenter(), ref.getCenter()) < EDGE_SIZE * 1.1:
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
    def getAdjTilesFromNode(self, node):
        tiles = set()
        for tile in self.board.tiles:
            if distance(tile.getCenter(), node.getCenter()) < EDGE_SIZE * 1.1:
                tiles.add(tile)

        return tiles
    def validateRoadPlacement(self, edge, i):
        if edge.owner == None:
            for node in self.getPlayer(i).settlements:
                if distance(node.getCenter(), edge.getCenter()) < EDGE_SIZE:
                    return True
            for road in self.getPlayer(i).roads:
                if distance(road.getCenter(), edge.getCenter()) < EDGE_SIZE:
                    return True

        return False
    def checkButtons(self):
        click = self.window.getMouse()
        distances = [b.distance(click) for b in self.buttons]
        minDist = min(distances)
        while minDist > 100:
            print ">> Please click one of the buttons to the right."
            click = self.window.getMouse()
            distances = [b.distance(click) for b in self.buttons]
            minDist = min(distances)
        b = distances.index(minDist)
        return self.buttons[b].text
    def roll(self):
        roll = self.board.dice.roll()
        if roll == 7:
            for player in self.players.players:
                if len(player.resources) > 7:
                    discard = len(player.resources)/2
                    print "%s had %d cards and needs to discard %d of them." % (player.name, len(player.resources), discard)
                    self.chooseCardsToDiscard(player, discard)
        else:
            tiles = set()
            nodes = []
            for tile in self.board.tiles:
                if tile.diceroll == roll:
                    nodes = self.getAdjNodesFromTile(tile)
                    for node in nodes:
                        if node.owner != None:
                            self.collectResource(tile, node.owner.id, node.isCity)
    def play(self):
        while 1:
            self.turnNumber += 1
            for i in range(self.players.numPlayers):
                self.roll()

                if self.getPlayer(i).style == "human":
                    action = None
                    while action != "end turn":
                        self.getPlayer(i).check(self.turnNumber)
                        action = self.checkButtons()
                        if action == "trade":
                            self.trade()
                        elif action == "dev card":
                            self.playDevCard()
                        elif action == "build":
                            self.build()

                else:
                    pass

                victor = self.checkVictory() # Check if anyone has 10 VPs
                if victor != None:
                    self.announceVictory(victor)
                    self.window.close()
                    quit()
    def getPlayer(self, id):
        for player in self.players.players:
            if player.id == id:
                return player
    def getDesert(self):
        for t in self.board.tiles:
            if type(t) == Resource:
                if t.label == "desert":
                    return t
    def chooseCardsToDiscard(self, player, n):
        if player.style == "human":
            pass
        elif player.style == "random":
            print player.resources
            for i in range(n):
                total = len(player.resources)
                player.resources.pop(random.randint(0,total-1))
            print player.resources
        elif player.style == "maximize":
            pass
    def playerMoveRobber(self, i):
        if self.getPlayer(i).style == "human":
            pass
        elif self.getPlayer(i).style == "random":
            pass
        elif self.getPlayer(i).style == "maximize":
            pass
    def moveRobber(self, tile):
        self.board.robber.move(tile)
    def getRobber(self):
        return self.board.robber.id
    def collectResource(self, tile, i, isCity):
        if type(tile) == Resource:
            resource = tile.label
            if tile.id != self.getRobber():
                self.getPlayer(i).resources.append(resource)
                number = 1
                if isCity:
                    self.getPlayer(i).resources.append(resource)
                    number = 2
                    print "You collect one extra from your city."
                if self.getPlayer(i).style == "human":
                    print "%s collected %d %s." % (self.getPlayer(i).name, number, resource)
                return resource

        return None
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
        centers = set()

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

                        # Check for duplicates
                        centers.add(edge.getCenter())
                        near = 0
                        for c in centers:
                            dist = distance(c, edge.getCenter())
                            if dist < EDGE_SIZE * 0.5:
                                near += 1
                        if near < 2: # Non-duplicates should only show up once
                            self.board.edges.add(edge)
                        else:        # Remove duplicates from the graphic
                            edge.line.undraw()

        # Build nodes
        centers = set()

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

                    # Check for duplicates
                    centers.add(node.getCenter())
                    near = 0
                    for c in centers:
                        dist = distance(c, node.getCenter())
                        if dist < EDGE_SIZE * 0.5:
                            near += 1
                    if near < 2: # Non-duplicates should only show up once
                        self.board.nodes.add(node)
                    else:        # Remove duplicates from the graphic
                        node.node.undraw()

        # Build graph with edges
        for source in self.board.edges:
            for target in self.board.edges:
                dist = distance(source.getCenter(), target.getCenter())
                if EDGE_SIZE * 0.1 < dist and dist < EDGE_SIZE * 1.1:
                    source.neighbors.add(target)

        # Build graph with nodes
        for source in self.board.nodes:
            for target in self.board.nodes:
                dist = distance(source.getCenter(), target.getCenter())
                if EDGE_SIZE * 0.1 < dist and dist < EDGE_SIZE * 1.1:
                    if source != target:
                        source.neighbors.add(target)

        # Put robber onto desert to start game
        desert = self.getDesert()
        self.moveRobber(desert)

        # Build buttons
        trade = Button(self.window, "trade", 70, randomColor())
        dev = Button(self.window, "dev card", 120, randomColor())
        build = Button(self.window, "build", 170, randomColor())
        end = Button(self.window, "end turn", 220, randomColor())
        self.buttons = [trade, dev, build, end]
    def trade(self):
        print "trade"
    def playDevCard(self):
        print "dev card"
    def build(self):
        print "build"
    def checkVictory(self):
        for player in self.players.players:
            if player.vPoints >= 10:
                return player

        return None
    def announceVictory(self, player):
        print "Player %d wins!" % player.id
    def placeSettlement(self, i, firstTurn):
        if self.getPlayer(i).style == "human":
            print ">> Please place a settlement on the map."

            click = self.window.getMouse()
            node = self.getNearby(click)[1]

            while node.settlable == False: # also check to see if user has built a road to the spot
                print ">> You cannot settle here."
                click = self.window.getMouse()
                node = self.getNearby(click)[1]
        elif self.getPlayer(i).style == "random":
            nodeChoices = set()

            for node in self.board.nodes:
                if node.settlable:
                    nodeChoices.add(node)

            node = nodeChoices.pop()
        elif self.getPlayer(i).style == "maximize":
            nodeChoices = []
            rollTotals = []
            for node in self.board.nodes:
                if node.settlable:
                    rollTotal = 0
                    tiles = self.getAdjTilesFromNode(node)
                    for tile in tiles:
                        roll = str(tile.diceroll)
                        rollTotal += DICE_ROLL_FREQUENCIES[roll]
                    rollTotals.append(rollTotal)
                    nodeChoices.append(node)
            maxIndex = rollTotals.index(max(rollTotals))
            node = nodeChoices[maxIndex]

        for n in self.getAdjNodesFromNode(node):
            n.settlable = False

        node.owner = self.getPlayer(i)
        node.owner.settlements.add(node)
        node.owner.vPoints += 1
        node.node.setFill(node.owner.color)
        node.settlable = False
        node.node.draw(self.window)

        return node
    def placeRoad(self, i):
        if self.getPlayer(i).style == "human":
            print ">> Please place a road on the map."

            click = self.window.getMouse()
            edge = self.getNearby(click)[2]
            valid = self.validateRoadPlacement(edge, i)

            while valid == False:
                print ">> You cannot build a road here."
                click = self.window.getMouse()
                edge = self.getNearby(click)[2]
                valid = self.validateRoadPlacement(edge,i)
        elif self.getPlayer(i).style == "maximize":
            nodeChoices = []
            rollTotals = []
            for node in self.board.nodes:
                if node.settlable:
                    rollTotal = 0
                    tiles = self.getAdjTilesFromNode(node)
                    for tile in tiles:
                        roll = str(tile.diceroll)
                        rollTotal += DICE_ROLL_FREQUENCIES[roll]
                    rollTotals.append(rollTotal)
                    nodeChoices.append(node)
            maxIndex = rollTotals.index(max(rollTotals))
            node = nodeChoices[maxIndex]

            nodeChoices = []
            distChoices = []
            for n in self.getPlayer(i).settlements:
                distChoices.append(distance(node.getCenter(),n.getCenter()))
                nodeChoices.append(n)
            minIndex = distChoices.index(min(distChoices))
            start = nodeChoices[minIndex]

            path = self.shortestPath(start, node)
            edge = self.getEdgeBetweenNodes(start, path[1])
        elif self.getPlayer(i).style == "random":
            edgeChoices = set()

            for edge in self.board.edges:
                if self.validateRoadPlacement(edge, i):
                    edgeChoices.add(edge)

            edge = edgeChoices.pop()

        self.getPlayer(i).roads.add(edge)
        edge.owner = self.getPlayer(i)
        edge.line.setFill(self.getPlayer(i).color)

        #need to update each player's longest road
        #and then compare to see if anyone is in the lead

        return edge
    def shortestPath(self, source, target):
        path = [target]
        visited = [source]
        queue = [source]
        previous = [None]

        while len(queue) > 0:
            current = queue.pop(0)

            cEdges = self.getAdjEdgesFromNode(current)
            for neighbor in current.neighbors:
                if neighbor.owner == None and neighbor not in visited:
                    nEdges = self.getAdjEdgesFromNode(current)
                    for edge in nEdges:
                        if edge in cEdges and edge.owner == None:
                            visited.append(neighbor)
                            queue.append(neighbor)
                            previous.append(current)

            if distance(current.getCenter(), target.getCenter()) < EDGE_SIZE:
                break

        while distance(visited[-1].getCenter(), target.getCenter()) > EDGE_SIZE:
            previous.pop()
            visited.pop()

        while len(previous):
            source = visited.pop()
            target = previous.pop()
            while source != target:
                source = visited.pop()
                previous.pop()
            path.append(target)

        path.reverse()

        return path
    def firstTurn(self):
        rolls = []
        order = []
        newPlayers = []

        for i in range(self.players.numPlayers):
            roll = self.board.dice.roll()
            self.getPlayer(i).roll = roll
            rolls.append(roll)

            print "%s's Turn #%d" % (self.getPlayer(i).name, self.turnNumber)
            if self.getPlayer(i).style == "human":
                alias = raw_input("Please enter your name: ")
                self.getPlayer(i).name = alias
            else:
                print "Play style: %s" % self.getPlayer(i).style
            print "Rolled a %d.\n" % roll

        for i in range(self.players.numPlayers):
            order.append(rolls.index(max(rolls)))
            rolls[order[-1]] = 0

        for i in order:
            newPlayers.append(self.getPlayer(i))

        self.players.players = newPlayers
        self.board.dice.clear()
        print "\n\n** NEW ORDER:", [player.name for player in newPlayers], "**\n\n"

        for i in range(self.players.numPlayers):
            self.getPlayer(i).check(self.turnNumber)
            self.placeSettlement(i, True)
            self.placeRoad(i)

        for i in range(self.players.numPlayers):
            j = self.players.numPlayers - i - 1
            self.getPlayer(j).check(self.turnNumber)
            secondSettlement = self.placeSettlement(j, True)
            tiles = self.getAdjTilesFromNode(secondSettlement)
            for tile in tiles:
                self.collectResource(tile, j, False)
            self.placeRoad(j)
class Button(object):
    def __init__(self, window, text, yStart, color):
        self.text = text
        self.object = Rectangle(Point(545,yStart),Point(625,yStart+40))

        self.object.setFill(color)
        self.object.setOutline(color_rgb(0,0,0))
        self.object.setWidth(3)
        self.object.draw(window)

        self.textObject = Text(Point(585, yStart+20), text)
        self.textObject.setSize(18)
        self.textObject.draw(window)

    def distance(self, click):
        distance = math.sqrt((click.getX() - 585)**2
                           + (click.getY() - self.object.getP1().getY() - 20)**2)
        return distance
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
        print "Roll: %d" % (self.one.value + self.two.value)
        return self.one.value + self.two.value

    def clear(self):
        self.one.clear()
        self.two.clear()
class Die(object):
    def __init__(self, window, x1, y1, x2, y2):
        self.window = window
        self.value = 0
        self.die = Rectangle(Point(x1,y1), Point(x2,y2))
        self.die.setFill(color_rgb(200,69,69))
        self.die.setOutline(color_rgb(0,0,0))
        self.die.setWidth(3)
        self.die.draw(self.window)

        self.text = Text(self.die.getCenter(), "")
        self.text.setSize(20)
        self.text.draw(self.window)

    def roll(self):
        self.value = random.randint(1,6)
        self.text.setText(str(self.value))

    def clear(self):
        self.text.setText("")
class Tile(object):
    def base(self, color=BACKGROUND_COLOR, outline=BACKGROUND_COLOR, outlineWidth=0):
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
        self.players = []
        self.numPlayers = humans + cpus
        for i in range(humans):
            self.players.append(HumanPlayer(len(self.players)))
        for i in range(cpus):
            self.players.append(CPUPlayer(len(self.players)))
class Player(object):
    def super_init(self, id):
        self.id = id
        try:
            self.color = PLAYER_COLORS_LOOKUP[id]
        except KeyError:
            self.color = randomColor()
        self.name = ""
        self.style = ""

        self.resources = []
        self.devcards = []
        self.settlements = set()
        self.roads = set()
        self.roll = 0

        self.next = None
        self.vPoints = 0
        self.LAtotal = 0
        self.LRtotal = 0
        self.largestArmy = False
        self.longestRoad = False

    def numCities(self):
        cities = [s.isCity for s in self.settlements]
        return sum(cities)

    def numSettlements(self):
        settlements = [not(s.isCity) for s in self.settlements]
        return sum(settlements)

    def numRoads(self):
        return len(self.roads)

    def optimize(self, item):
        tempDict = {}
        tempList = []
        for i in item:
            tempDict[i] = item.count(i)
        for i in tempDict:
            data = "x" + str(tempDict[i]) + " " + i
            tempList.append(data)

        return tempList
    def check(self, turn): # before you wreck(self)
        print "%s's Turn #%d:" % (self.name, turn)
        print "\tYou have used %d out of %d cities." % (self.numCities(), 4)
        print "\tYou have used %d out of %d settlements." % (self.numSettlements(), 5)
        print "\tYou have used %d out of %d roads." % (self.numRoads(), 15)
        print "\tYou currently have %d development cards:" % len(self.devcards)
        for devcard in self.optimize(self.devcards):
            print "\t  %s" % devcard
        print "\tYou currently have %d resource cards:" % len(self.resources)
        for resource in self.optimize(self.resources):
            print "\t  %s" % resource
        print "\tYou have played %d Knights..." % self.LAtotal
        if self.largestArmy:
            print "\t... and currently have the Largest Army."
        print "\tYour longest road is %d roads..." % self.LRtotal
        if self.longestRoad:
            print "\t... is currently the Longest Road."
        print "\tTherefore, you have %d victory points.\n" % self.vPoints
class HumanPlayer(Player):
    def __init__(self, id):
        self.super_init(id)
        self.style = "human"
        self.name = "Player " + str(id+1)
class CPUPlayer(Player):
    def __init__(self, id):
        self.super_init(id)
        self.style = random.choice(AI_TYPES)
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
        self.north = north
        self.settlable = True

        self.neighbors = set()

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

    def show(self):
        self.node.draw(self.window)

    def hide(self):
        self.node.undraw()
class Edge(object):
    def __init__(self, window, source, target):
        self.window = window
        self.source = source
        self.target = target
        self.owner = None

        self.neighbors = set()

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

if __name__ == "__main__":
    main()
