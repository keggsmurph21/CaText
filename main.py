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

        self.players = [player.HumanPlayer(0), player.CPUPlayer(1),
            player.CPUPlayer(2), player.CPUPlayer(3)]

            ### Temp for implementing longest road counter
        p = self.players[0]
        vert = p.settle(self.graph, self.gui, self.dicefreq, 0)
        self.graph.buildSettlement(vert,p)
        self.gui.buildSettlement(vert,p)
        vert = p.settle(self.graph, self.gui, self.dicefreq, 0)
        self.graph.buildSettlement(vert,p)
        self.gui.buildSettlement(vert,p)
        for f in range(6):
            road = p.findRoad(self.graph, self.gui, self.dicefreq, None)
            self.graph.buildRoad(road,p)
            self.gui.buildRoad(road,p)

        print p.countLongestRoad(self.graph)
            ### End temp

        random.shuffle(self.players)

        firstTurnOrder = [] # eventually should roll to see who goes first
        for p in self.players:
            firstTurnOrder.append(p)
        self.players.reverse()
        for p in self.players:
            firstTurnOrder.append(p)
        self.players.reverse()

        for p in firstTurnOrder:
            vert = p.settle(self.graph, self.gui, self.dicefreq, 0)
            self.graph.buildSettlement(vert, p)
            self.gui.buildSettlement(vert, p)

            road = p.findRoad(self.graph, self.gui, self.dicefreq, vert)
            self.graph.buildRoad(road, p)
            self.gui.buildRoad(road, p)

            if len(p.settlements) == 2:
                for adj in self.graph.vertGetAdjs(vert):
                    p.resources.append(adj.tile.resource)

        while 1:
            for p in self.players:
                roll = p.rollDice()
                self.gui.updateDice(roll)

                for q in self.players:
                    q.collectResources(self.graph,sum(roll))
                    print q.id, q.resources

                print p.countLongestRoad(self.graph)

                victor = self.checkVictory()
                if victor != None:
                    return

                self.gui.win.getMouse()

    def checkVictory(self):
        for p in self.players:
            if p.vpts >= 10:
                return p

        return None



def main():
    catan = Catan()

    return 0

if __name__ == "__main__":
    main()
