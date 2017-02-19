from random import shuffle

class Graph(object):
    def __init__(self, g_dict=None):
        if g_dict == None:
            g_dict = {}
        self.g_dict = g_dict
        self.generate_nodes()
        self.generate_edges()

    def optimize(self,data,cards,rolls):
        self.verts = []
        self.tiles = []
        self.adjs = []
        edges = []

        shuffle(cards)
        shuffle(rolls)

        for node in self.nodes:
            if data[node][0] == "vert":
                this = Vert(node[1:], data[node])
                self.verts.append(this)
            elif data[node][0] == "tile":
                resource = cards.pop()
                this = Tile(node[1:], resource, data[node])
                if resource != "desert":
                    this.diceroll = rolls.pop()
                self.tiles.append(this)

        for edge in self.edges:
            source = edge.pop()
            target = edge.pop()

            if source[0] == "n" and target[0] == "n":
                vert1 = self.getVertByID(source[1:])
                vert2 = self.getVertByID(target[1:])
                this = Edge(vert1, vert2)
                edges.append(this)
            else:
                key = source[0]
                sid = source[1:]
                tid = target[1:]

                if key == "n":
                    vert = self.getVertByID(sid)
                    tile = self.getTileByID(tid)
                else:
                    tile = self.getTileByID(sid)
                    vert = self.getVertByID(tid)
                this = Adj(vert, tile)
                self.adjs.append(this)

        self.edges = edges

    def vertGetNeighbors(self, vert):
        neighbors = []

        for edge in self.edges:
            if vert in edge.verts():
                if vert == edge.v1:
                    neighbors.append(edge.v2)
                else:
                    neighbors.append(edge.v1)

        return neighbors

    def generate_nodes(self):
        self.nodes = []
        for key in self.g_dict.keys():
            self.nodes.append(key)

    def generate_edges(self):
        self.edges = []
        for source in self.g_dict.keys():
            if source[0] == "n":
                for target in self.g_dict[source]:
                    edge = {source,target}
                    if edge not in self.edges:
                        if target != None:
                            self.edges.append(edge)

    def getVertByID(self,id):
        for vert in self.verts:
            if vert.id == id:
                return vert
        return None

    def getTileByID(self,id):
        for tile in self.tiles:
            if tile.id == id:
                return tile

    def getDesert(self):
        for tile in self.tiles:
            if tile.resource == "desert":
                return tile

class Vert(object):
    def __init__(self, id, data):
        self.id = id
        self.x = data[1]
        self.y = data[2]
        self.harbor = data[3]
        self.isSettlable = True
        self.isCity = False
        self.owner = None

        self.obj = None

class Tile(object):
    def __init__(self, id, resource, data):
        self.id = id
        self.x = data[1]
        self.y = data[2]
        self.diceroll = 0
        self.resource = resource

        self.obj = None

class Edge(object):
    def __init__(self, source, target):
        self.v1 = source
        self.v2 = target
        self.owner = None

        self.obj = None

    def verts(self):
        return {self.v1, self.v2}

class Adj(object):
    def __init__(self, vert, tile):
        self.vert = vert
        self.tile = tile
