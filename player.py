from graphics import color_rgb
from random import randint

class Player(object):
    def __init__(self, id):
        self.id = id
        self.settlements = []
        self.roads = []
        self.resources = []
        self.color = PLAYER_COLORS_LOOKUP[id]
        self.vpts = 0

    def rollDice(self):
        return randint(1,6), randint(1,6)

class CPUPlayer(Player):
    def __init__(self, id):
        super(CPUPlayer, self).__init__(id)

    def findBestSpot(self, graph, df, dist=0):
        this = None # the spot to be settled
        max = 0
        d = 0

        for v in graph.verts:
            for s in self.settlements:
                d = len(graph.shortestPath(v,s,self))
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

        return path[0]

class HumanPlayer(Player):
    def __init__(self, id):
        super(HumanPlayer, self).__init__(id)

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

    if nearby.intersection({road.v1,road.v2}) == set([]):
        return False

    return True

PLAYER_COLORS_LOOKUP = {
    0 : color_rgb(255,20,0),    # Red
    1 : color_rgb(0,10,255),    # Blue
    2 : color_rgb(35,140,35),   # Green
    3 : color_rgb(170,100,40) } # Brown
