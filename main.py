import boards, graph, gui, player, random

class Catan(object):
    def __init__(self):
        g_dict = boards.standard("tiles")
        data = boards.standard("data")
        cards = boards.standard("cards")
        rolls = boards.standard("rolls")
        harbors = boards.standard("harbors")
        self.dicefreq = boards.standard("dicefreq")

        self.graph = graph.Graph(g_dict,data,cards,rolls)
        self.gui = gui.GUI(self.graph, harbors)

        self.longestRoad = 4
        self.largestArmy = 2

        self.players = [
            player.HumanPlayer(0),
            player.HumanPlayer(1),
            player.CPUPlayer(2),
            player.CPUPlayer(3) ]

        random.shuffle(self.players)

        firstTurnOrder = [] # eventually should roll to see who goes first
        for p in self.players:
            firstTurnOrder.append(p)
        self.players.reverse()
        for p in self.players:
            firstTurnOrder.append(p)
        self.players.reverse()

        for p in firstTurnOrder:
            vert = self.buildSettlement(p,0)
            self.buildRoad(p,vert)

            if len(p.settlements) == 2:
                for adj in self.graph.vertGetAdjs(vert):
                    p.resources.append(adj.tile.resource)

        while 1:
            for p in self.players:
                roll = p.rollDice()
                self.gui.updateDice(roll)

                for q in self.players:
                    q.collectResources(self.graph,sum(roll))
                    #print q.id, q.resources

                # Keep adding roads every turn
                self.buildRoad(p)

                #print p.id, p.countLongestRoad(self.graph)

                victor = self.checkVictory()
                if victor != None:
                    return

                #self.gui.win.getMouse()

    def buildRoad(self, player, settlement=None):
        road = player.findRoad(self.graph, self.gui, self.dicefreq, settlement)
        self.graph.buildRoad(road, player)
        self.gui.buildRoad(road, player)

        return road

    def buildSettlement(self, player, dist):
        vert = player.settle(self.graph, self.gui, self.dicefreq, dist)
        self.graph.buildSettlement(vert, player)
        self.gui.buildSettlement(vert, player)

        return vert

    def checkLongestRoad(self, player):
        roads = player.countLongestRoad(self.graph)
        if roads > self.longestRoad:
            for p in self.players:
                if p.hasLongestRoad:
                    p.hasLongestRoad = False
                    p.vpts -= 2
            player.hasLongestRoad = True
            player.vpts += 2
            self.longestRoad = roads

            return player

        return None

    def checkLargestArmy(self, player):
        army = player.countLargestArmy()
        if army > self.largestArmy:
            for p in self.players:
                if p.hasLargestArmy:
                    p.hasLargestArmy = False
                    p.vpts -= 2
            player.hasLargestArmy = True
            player.vpts += 2
            self.largestArmy = army

            return player

        return None

    def checkVictory(self):
        for p in self.players:
            plr = self.checkLongestRoad(p)
            pla = self.checkLargestArmy(p)

            if plr != None:
                print "Longest road:", plr.id
            if pla != None:
                print "Largest army:", pla.id

            if p.vpts >= 10:
                return p

        return None



def main():
    catan = Catan()

    return 0

if __name__ == "__main__":
    main()
