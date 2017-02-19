import boards, graph, gui, pickle, random

class Catan(object):
    def __init__(self):
        g_dict = boards.standard("tiles")
        data = boards.standard("data")
        cards = boards.standard("cards")
        rolls = boards.standard("rolls")
        harbors = boards.standard("harbors")

        self.graph = graph.Graph(g_dict)
        self.graph.optimize(data,cards,rolls)

        self.gui = gui.GUI(self.graph, harbors)
        self.gui.moveRobber(self.graph.getDesert())

        self.gui.pause()



def main():
    catan = Catan()

    return 0

if __name__ == "__main__":
    main()
