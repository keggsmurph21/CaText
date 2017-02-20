from graphics import color_rgb
from random import choice, randint

class Player(object):
    def __init__(self, id):
        self.id = id
        self.settlements = []
        self.roads = []
        self.resources = []
        self.color = PLAYER_COLORS_LOOKUP[id]
        self.vpts = 0
        self.type = ""

    def countLongestRoad(self, graph):
        longest = 0

        roads = list(self.roads)
        roadsets = []
        mark = set()
        counted = set()

        while len(roads): # Separate roads into connected groups
            roadset = set()
            road = roads.pop()
            for r in roads:
                if graph.checkConnected(road,r) and r not in mark:
                        roadset.add(r)
                        mark.add(r)

            if len(roadset) or road not in counted:
                roadset.add(road)
                for r in roadset:
                    counted.add(r)
                roadsets.append(roadset)

        for rs in roadsets: # For each group, calculate Longest Road
            localmax = 0    #  = LR for this subgroup

            mark = set()
            rand = choice(list(rs)) # Choose a random starting road
                                    # and make sure it's at the end of a segment
            while len(graph.edgeGetEdges(rand,self)) > 1:
                mark.add(rand)
                if mark == rs: # Avoid infinite loops
                    break
                rand = choice(list(rs))

            queue = []   # Then DFS to find farthest
            mark = set()
            dist = {}

            queue.append(rand)
            mark.add(rand)
            dist[rand] = 0

            while len(queue):
                c = queue.pop(0)
                d = dist[c]

                for e in graph.edgeGetEdges(c,self):
                    vertOwner = c.verts().intersection(e.verts()).pop().owner
                    if vertOwner == self or vertOwner == None:
                        if e not in mark:
                            queue.append(e)
                            mark.add(e)
                            dist[e] = d+1
                        else:
                            if dist[e] < d+1:
                                dist[e] = d+1

            localmax = max(dist.values())

            if longest < localmax:
                longest = localmax

        return longest

    def rollDice(self):
        return randint(1,6), randint(1,6)

    def collectResources(self, graph, num):
        for tile in graph.tiles:
            if tile.diceroll == num:
                for vert in tile.verts:
                    if vert.owner == self and tile.resource != "desert":
                        self.resources.append(tile.resource)
                        if vert.isCity:
                            self.resources.append(tile.resource)

    def settle(self, graph, gui, df, dist=0):
        if self.type == "cpu":
            vert = self.findBestSpot(graph, df, dist)
        else:
            vert = self.chooseSettleSpot(graph, gui)

        return vert

    def findRoad(self, graph, gui, df, settlement=None):
        if self.type == "cpu":
            goal = self.findBestSpot(graph, df, 3)
            road = self.findBestRoad(graph, goal, settlement)
        else:
            road = self.chooseRoadSpot(graph, gui, settlement)

        return road

class CPUPlayer(Player):
    def __init__(self, id):
        super(CPUPlayer, self).__init__(id)
        self.type = "cpu"

    def findBestSpot(self, graph, df, dist=0):
        this = None
        max = 0
        d = 0

        for v in graph.verts:
            if dist:
                d = min([len(graph.shortestPath(v,s,self)) for s in self.settlements])

            if (dist == 0 or d <= dist) and v.isSettlable:
                m = 0
                for a in graph.vertGetAdjs(v):
                    m += df[str(a.tile.diceroll)]
                if m > max:
                    this = v
                    max = m

        return this

    def findBestRoad(self, graph, goal, settlement=None):
        this = None
        dist = 100

        if settlement:
            this = settlement
        else:
            for s in self.settlements:
                d = len(graph.shortestPath(s,goal,self))
                if d < dist:
                    this = s
                    dist = d

        path = graph.shortestPath(this,goal,self)

        if len(path):
            return path[0]
        else:
            return choice(graph.vertGetEdges(this))

class HumanPlayer(Player):
    def __init__(self, id):
        super(HumanPlayer, self).__init__(id)
        self.type = "human"

    def chooseSettleSpot(self, graph, gui):
        click = gui.win.getMouse()
        vert = gui.clickObj(click,graph,"v")
        while not(vert.isSettlable):
            click = gui.win.getMouse()
            vert = gui.clickObj(click,graph,"v")

        return vert

    def chooseRoadSpot(self, graph, gui, settlement=None):
        click = gui.win.getMouse()
        edge = gui.clickObj(click,graph,"e")
        while not(validateRoadPlacement(edge,self,graph,settlement)):
            click = gui.win.getMouse()
            edge = gui.clickObj(click,graph,"e")

        return edge

def validateRoadPlacement(road,player,graph,settlement):
    if road.owner != None:
        return False

    nearby = set()

    if settlement: # For handling the initial placement
        nearby.add(settlement)
    else:
        for s in player.settlements:
            nearby.add(s)
        for r in player.roads:
            if r.v1.owner == None or r.v1.owner == player:
                nearby.add(r.v1)
            if r.v2.owner == None or r.v2.owner == player:
                nearby.add(r.v2)

    if nearby.intersection(road.verts()) == set([]):
        return False

    return True

PLAYER_COLORS_LOOKUP = {
    0 : color_rgb(255,20,0),    # Red
    1 : color_rgb(0,10,255),    # Blue
    2 : color_rgb(35,140,35),   # Green
    3 : color_rgb(170,100,40) } # Brown
