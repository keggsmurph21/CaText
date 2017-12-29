import os, random

COLORS = {
    'reset':    u"\u001b[0m",
    'black':    u"\u001b[30m",
    'desert':   u"\u001b[38;5;223m",
    'wheat':    u"\u001b[38;5;226m",
    'sheep':    u"\u001b[38;5;155m",
    'brick':    u"\u001b[38;5;208m",
    'wood':     u"\u001b[38;5;22m",
    'ore':      u"\u001b[38;5;240m",
    '0':        u"\u001b[38;5;1m",
    '1':        u"\u001b[38;5;26m",
    '2':        u"\u001b[38;5;202m",
    '3':        u"\u001b[38;5;14m",
    'b_white':  u"\u001b[47m"
}

class Catan(object):
    def __init__(self):
        self.hexes = []
        self.nodes = []
        self.roads = []
        self.conns = []

        self.players = []

        self.generate_board()

        self.h_index = {
            'd11':  5,
            'd12':  5,
            'd19':  6,
            'd20':  6,
            'd27':  7,
            'd28':  7,
            'h7':   10,
            'h07':  10,
            'h8':   10,
            'h08':  10,
            'h15':  11,
            'h16':  11,
            'h23':  12,
            'h24':  12,
            'h31':  13,
            'h32':  13,
            'l4':   16,
            'l04':  16,
            'l5':   16,
            'l6':   16,
            'l11':  17,
            'l12':  17,
            'l19':  18,
            'l20':  18,
            'l27':  19,
            'l28':  19,
            'l35':  20,
            'l36':  20,
            'p7':   23,
            'p07':  23,
            'p8':   23,
            'p08':  23,
            'p15':  24,
            'p16':  24,
            'p23':  25,
            'p24':  25,
            'p31':  26,
            'p32':  26,
            't11':  29,
            't12':  29,
            't19':  30,
            't20':  30,
            't27':  31,
            't28':  31
        }
        self.n_index = {
            'a12':  0,
            'a20':  1,
            'a28':  2,
            'c8':   3,
            'c08':  3,
            'c16':  4,
            'c24':  5,
            'c32':  6,
            'e8':   7,
            'e08':  7,
            'e16':  8,
            'e24':  9,
            'e32':  10,
            'g4':   11,
            'g04':  11,
            'g12':  12,
            'g20':  13,
            'g28':  14,
            'g36':  15,
            'i4':   16,
            'i04':  16,
            'i12':  17,
            'i20':  18,
            'i28':  19,
            'i36':  20,
            'k0':   21,
            'k00':  21,
            'k8':   22,
            'k08':  22,
            'k16':  23,
            'k24':  24,
            'k32':  25,
            'k40':  26,
            'm0':   27,
            'm00':  27,
            'm8':   28,
            'm08':  28,
            'm16':  29,
            'm24':  30,
            'm32':  31,
            'm40':  32,
            'o4':   33,
            'o04':  33,
            'o12':  34,
            'o20':  35,
            'o28':  36,
            'o36':  37,
            'q4':   38,
            'q04':  38,
            'q12':  39,
            'q20':  40,
            'q28':  41,
            'q36':  42,
            's8':   43,
            's08':  43,
            's16':  44,
            's24':  45,
            's32':  46,
            'u8':   47,
            'u08':  47,
            'u16':  48,
            'u24':  49,
            'u32':  50,
            'w12':  51,
            'w20':  52,
            'w28':  53
        }
        self.r_index = {
            'b10':  0,
            'b14':  1,
            'b18':  2,
            'b22':  3,
            'b26':  4,
            'b30':  5,
            'd8':   6,
            'd08':  6,
            'd16':  7,
            'd24':  8,
            'd32':  9,
            'f6':   10,
            'f06':  10,
            'f10':  11,
            'f14':  12,
            'f18':  13,
            'f22':  14,
            'f26':  15,
            'f30':  16,
            'f34':  17,
            'h4':   18,
            'h04':  18,
            'h12':  19,
            'h20':  20,
            'h28':  21,
            'h36':  22,
            'j2':   23,
            'j02':  23,
            'j6':   24,
            'j06':  24,
            'j10':  25,
            'j14':  26,
            'j18':  27,
            'j22':  28,
            'j26':  29,
            'j30':  30,
            'j34':  31,
            'j38':  32,
            'l0':   33,
            'l00':  33,
            'l8':   34,
            'l08':  34,
            'l16':  35,
            'l24':  36,
            'l32':  37,
            'l40':  38,
            'n2':   39,
            'n02':  39,
            'n6':   40,
            'n06':  40,
            'n10':  41,
            'n14':  42,
            'n18':  43,
            'n22':  44,
            'n26':  45,
            'n30':  46,
            'n34':  47,
            'n38':  48,
            'p4':   49,
            'p04':  49,
            'p12':  50,
            'p20':  51,
            'p28':  52,
            'p36':  53,
            'r6':   54,
            'r06':  54,
            'r10':  55,
            'r14':  56,
            'r18':  57,
            'r22':  58,
            'r26':  59,
            'r30':  60,
            'r34':  61,
            't8':   62,
            't08':  62,
            't16':  63,
            't24':  64,
            't32':  65,
            'v10':  66,
            'v14':  67,
            'v18':  68,
            'v22':  69,
            'v26':  70,
            'v30':  71
        }

    def generate_board(self):
        self.hexes = []
        self.nodes = []
        self.roads = []
        self.conns = []

        self.players = []

        diceValues = [2,3,3,4,4,5,5,6,6,8,8,9,9,10,10,11,11,12]
        random.shuffle(diceValues)
        resources = ['desert', 'wheat', 'wheat', 'wheat', 'wheat', 'sheep', 'sheep', 'sheep', 'sheep', 'brick', 'brick', 'brick', 'wood', 'wood', 'wood', 'wood', 'ore', 'ore', 'ore']
        random.shuffle(resources)

        resourceTiles = [5,6,7,10,11,12,13,16,17,18,19,20,23,24,25,26,29,30,31]

        # make the Hexes
        for i in range(37):
            if i not in resourceTiles: # ocean tiles
                self.hexes.append( Hex(i,True,0,'') )
            else:
                resource = resources.pop()
                if resource == 'desert':
                    diceValue = 0
                else:
                    diceValue = diceValues.pop()
                self.hexes.append( Hex(i,False,diceValue,resource) )

        # makes the Nodes
        for i in range(54):
            self.nodes.append( Node(i) )

        # make the Roads
        road_vertices = [(3,0),(0,4),(4,1),(1,5),(5,2),(2,6),(3,7),(4,8),(5,9),(6,10),(11,7),(7,12),(12,8),(8,13),(13,9),(9,14),(14,10),(10,15),(11,16),(12,17),(13,18),(14,19),(15,20),(21,16),(16,22),(22,17),(17,23),(23,18),(18,24),(24,19),(19,25),(25,20),(20,26),(21,27),(22,28),(23,29),(24,30),(25,31),(26,32),(27,33),(33,28),(28,34),(34,29),(29,35),(35,30),(30,36),(36,31),(31,37),(37,32),(33,38),(34,39),(35,40),(36,41),(37,42),(38,43),(43,39),(39,44),(44,40),(40,45),(45,41),(41,46),(46,42),(43,47),(44,48),(45,49),(46,50),(47,51),(51,48),(48,52),(52,49),(49,53),(53,50)]
        for i in range(72):
            self.roads.append( Road(i) )
            road_n0 = self.nodes[road_vertices[i][0]]
            road_n1 = self.nodes[road_vertices[i][1]]
            self.roads[i].set_vertices(road_n0, road_n1)
            road_n0.add_road(self.roads[i])
            road_n1.add_road(self.roads[i])

        # make the Connections
        conn_vertices = [(0,5),(4,5),(8,5),(12,5),(7,5),(3,5), (1,6),(5,6),(9,6),(13,6),(8,6),(4,6), (2,7),(6,7),(10,7),(14,7),(9,7),(5,7), (7,10),(12,10),(17,10),(22,10),(16,10),(11,10), (8,11),(13,11),(18,11),(23,11),(17,11),(12,11), (9,12),(14,12),(19,12),(24,12),(18,12),(13,12), (10,13),(15,13),(20,13),(25,13),(19,13),(14,13), (16,16),(22,16),(28,16),(33,16),(27,16),(21,16), (17,17),(23,17),(29,17),(34,17),(28,17),(22,17), (18,18),(24,18),(30,18),(35,18),(29,18),(23,18),(19,19),(25,19),(31,19),(36,19),(30,19),(24,19), (20,20),(26,20),(32,20),(37,20),(31,20),(25,20), (28,23),(34,23),(39,23),(43,23),(38,23),(33,23), (29,24),(35,24),(40,24),(44,24),(39,24),(34,24), (30,25),(36,25),(41,25),(45,25),(40,25),(35,25), (31,26),(37,26),(42,26),(46,26),(41,26),(36,26), (39,29),(44,29),(48,29),(51,29),(47,29),(43,29), (40,30),(45,30),(49,30),(52,30),(48,30),(44,30), (41,31),(46,31),(50,31),(53,31),(49,31),(45,31)]
        for i in range(114):
            self.conns.append( Connection(i) )
            conn_node = self.nodes[conn_vertices[i][0]]
            conn_hex = self.hexes[conn_vertices[i][1]]
            self.conns[i].set_vertices(conn_node, conn_hex)
            conn_node.add_conn(self.conns[i])
            conn_hex.add_conn(self.conns[i])

        # make the Players
        for i in range(4):
            self.players.append( Player(i) )


    def handle_input(self, args):
        args = args.split(' ')
        cmd = args[0]

        if cmd == 'help':
            if len(args) == 1:
                msg = u'For help with a specific command, type "help {cmd}".\n\u001b[38;5;244mavailable commands:\u001b[0m help, info'
            elif len(args) == 2:
                if args[1] == 'help':
                    msg = u"Usage: help $1\t\u001b[38;5;244m1: command (e.g. info)\u001b[0m"
                elif args[1] == 'info':
                    msg = u"Usage: info $1\t\u001b[38;5;244m1: coordinate (e.g. E24)\u001b[0m"
                else:
                    msg = '%s: Unrecognized command.  For a list of commands, type "help".' % args[1]
            else:
                msg = 'Command "help" requires one or two arguments.  For help, type "help".'

        elif cmd == 'info':
            if len(args) != 2:
                msg = 'Command "info" requires one argument.  For help, type "help info".'
            else:
                msg = self.cmd_info(args[1])
        elif cmd == '!n': # hide this command from end users (i.e. not in help menus)
            if len(args) != 2:
                msg = 'Command "!n" requires one argument.'
            else:
                msg = self.cmd_neighbors(args[1])
        elif cmd == '!reset': # hide this command from end users (i.e. not in help menus)
            self.generate_board()
            msg = "** regenerated board **"

        else:
            msg = '%s: Unrecognized command.  For a list of commands, type "help".' % cmd

        return msg


    def view(self, msg):
        os.system('cls' if os.name == 'nt' else 'clear')

        s = u"""\u001b[38;5;244m/================================ [ CaTEXT ] ==================================\\
   0         1         2         3         4
   01234567890123456789012345678901234567890\u001b[0m\t   .___________________.       \u001b[38;5;244m
 A\u001b[38;5;27m ~~~~~~~~~~~ \u001b[0m%s\u001b[38;5;27m ~~~~~ \u001b[0m%s\u001b[38;5;27m ~~~~~ \u001b[0m%s\u001b[38;5;27m ~~~~~~~~~~~ \u001b[38;5;244mA\u001b[0m     |__KEY______________|       \u001b[38;5;244m
 B\u001b[38;5;27m ~~~~~~~~~ \u001b[0m%s   %s\u001b[38;5;27m ~ \u001b[0m%s   %s\u001b[38;5;27m ~ \u001b[0m%s   %s\u001b[38;5;27m ~~~~~~~~~ \u001b[38;5;244mB\u001b[0m     | %s    %s     |       \u001b[38;5;244m
 C\u001b[38;5;27m ~~~~~~~ \u001b[0m%s       %s       %s       %s\u001b[38;5;27m ~~~~~~~ \u001b[38;5;244mC\u001b[0m     | %s     %s    |       \u001b[38;5;244m
 D\u001b[38;5;27m ~~~~~~~ \u001b[0m|  %2s   |  %2s   |  %2s   |\u001b[38;5;27m ~~~~~~~ \u001b[38;5;244mD\u001b[0m     | %s     %s   |       \u001b[38;5;244m
 E\u001b[38;5;27m ~~~~~~~ \u001b[0m%s       %s       %s       %s\u001b[38;5;27m ~~~~~~~ \u001b[38;5;244mE\u001b[0m     |______%s_______|       \u001b[38;5;244m
 F\u001b[38;5;27m ~~~~~ \u001b[0m%s   %s   %s   %s   %s   %s   %s   %s\u001b[38;5;27m ~~~~~ \u001b[38;5;244mF\u001b[0m                                 \u001b[38;5;244m
 G\u001b[38;5;27m ~~~ \u001b[0m%s       %s       %s       %s       %s\u001b[38;5;27m ~~~ \u001b[38;5;244mG\u001b[0m  ._________________________.    \u001b[38;5;244m
 H\u001b[38;5;27m ~~~ \u001b[0m|  %2s   |  %2s   |  %2s   |  %2s   |\u001b[38;5;27m ~~~ \u001b[38;5;244mH\u001b[0m  |__NAME_____Pts_Cards_DCs_|    \u001b[38;5;244m
 I\u001b[38;5;27m ~~~ \u001b[0m%s       %s       %s       %s       %s\u001b[38;5;27m ~~~ \u001b[38;5;244mI\u001b[0m  | %s  %s   %s   %s  |    \u001b[38;5;244m
 J\u001b[38;5;27m ~ \u001b[0m%s   %s   %s   %s   %s   %s   %s   %s   %s   %s\u001b[38;5;27m ~ \u001b[38;5;244mJ\u001b[0m  | %s  %s   %s   %s  |    \u001b[38;5;244m
 K\u001b[0m %s       %s       %s       %s       %s       %s \u001b[38;5;244mK\u001b[0m  | %s  %s   %s   %s  |    \u001b[38;5;244m
 L\u001b[0m |  %2s   |  %2s   |  %2s   |  %2s   |  %2s   | \u001b[38;5;244mL\u001b[0m  | %s  %s   %s   %s  |    \u001b[38;5;244m
 M\u001b[0m %s       %s       %s       %s       %s       %s \u001b[38;5;244mM\u001b[0m  |_________________________|    \u001b[38;5;244m
 N\u001b[38;5;27m ~ \u001b[0m%s   %s   %s   %s   %s   %s   %s   %s   %s   %s\u001b[38;5;27m ~ \u001b[38;5;244mN
 O\u001b[38;5;27m ~~~ \u001b[0m%s       %s       %s       %s       %s\u001b[38;5;27m ~~~ \u001b[38;5;244mO
 P\u001b[38;5;27m ~~~ \u001b[0m|  %2s   |  %2s   |  %2s   |  %2s   |\u001b[38;5;27m ~~~ \u001b[38;5;244mP
 Q\u001b[38;5;27m ~~~ \u001b[0m%s       %s       %s       %s       %s\u001b[38;5;27m ~~~ \u001b[38;5;244mQ
 R\u001b[38;5;27m ~~~~~ \u001b[0m%s   %s   %s   %s   %s   %s   %s   %s\u001b[38;5;27m ~~~~~ \u001b[38;5;244mR
 S\u001b[38;5;27m ~~~~~~~ \u001b[0m%s       %s       %s       %s\u001b[38;5;27m ~~~~~~~ \u001b[38;5;244mS
 T\u001b[38;5;27m ~~~~~~~ \u001b[0m|  %2s   |  %2s   |  %2s   |\u001b[38;5;27m ~~~~~~~ \u001b[38;5;244mT
 U\u001b[38;5;27m ~~~~~~~ \u001b[0m%s       %s       %s       %s\u001b[38;5;27m ~~~~~~~ \u001b[38;5;244mU
 V\u001b[38;5;27m ~~~~~~~~~ \u001b[0m%s   %s\u001b[38;5;27m ~ \u001b[0m%s   %s\u001b[38;5;27m ~ \u001b[0m%s   %s\u001b[38;5;27m ~~~~~~~~~ \u001b[38;5;244mV
 W\u001b[38;5;27m ~~~~~~~~~~~ \u001b[0m%s\u001b[38;5;27m ~~~~~ \u001b[0m%s\u001b[38;5;27m ~~~~~ \u001b[0m%s\u001b[38;5;27m ~~~~~~~~~~~ \u001b[38;5;244mW
   01234567890123456789012345678901234567890
   0         1         2         3         4
\\==============================================================================/\u001b[0m\t
%s"""

        print s % ( self.nodes[0], self.nodes[1], self.nodes[2], self.roads[0], self.roads[1], self.roads[2], self.roads[3], self.roads[4], self.roads[5], (COLORS['desert'] + u'desert' + COLORS['reset']), (COLORS['ore'] + 'ore' + COLORS['reset']), self.nodes[3], self.nodes[4], self.nodes[5], self.nodes[6], (COLORS['wheat'] + 'wheat' + COLORS['reset']), (COLORS['wood'] + 'wood' + COLORS['reset']), self.hexes[5], self.hexes[6], self.hexes[7], (COLORS['sheep'] + 'sheep' + COLORS['reset']), (COLORS['brick'] + 'brick' + COLORS['reset']),  self.nodes[7], self.nodes[8], self.nodes[9], self.nodes[10], (COLORS['black'] + COLORS['b_white'] + 'robber' + COLORS['reset']), self.roads[6], self.roads[7], self.roads[8], self.roads[9], self.roads[10], self.roads[11], self.roads[12], self.roads[13], self.nodes[11], self.nodes[12], self.nodes[13],  self.nodes[14], self.nodes[15], self.hexes[10], self.hexes[11], self.hexes[12], self.hexes[13], self.nodes[16], self.nodes[17], self.nodes[18], self.nodes[19], self.nodes[20], (COLORS['0'] + str(self.players[0]).ljust(8)), str(self.players[0].score).rjust(2), str(len(self.players[0].resCards)).rjust(2), (str(len(self.players[0].devCards)).rjust(2) + COLORS['reset']), self.roads[14], self.roads[15], self.roads[16], self.roads[17], self.roads[18], self.roads[19], self.roads[20], self.roads[21], self.roads[22], self.roads[23], (COLORS['1'] + str(self.players[1]).ljust(8)), str(self.players[1].score).rjust(2), str(len(self.players[1].resCards)).rjust(2), (str(len(self.players[1].devCards)).rjust(2) + COLORS['reset']), self.nodes[21], self.nodes[22], self.nodes[23], self.nodes[24], self.nodes[25], self.nodes[26], (COLORS['2'] + str(self.players[2])).ljust(8), str(self.players[2].score).rjust(2), str(len(self.players[2].resCards)).rjust(2), (str(len(self.players[2].devCards)).rjust(2) + COLORS['reset']), self.hexes[16], self.hexes[17], self.hexes[18], self.hexes[19], self.hexes[20], (COLORS['3'] + str(self.players[3]).ljust(8)), str(self.players[3].score).rjust(2), str(len(self.players[3].resCards)).rjust(2), (str(len(self.players[3].devCards)).rjust(2) + COLORS['reset']), self.nodes[27], self.nodes[28], self.nodes[29], self.nodes[30], self.nodes[31], self.nodes[32], self.roads[24], self.roads[25], self.roads[26], self.roads[27], self.roads[28], self.roads[29], self.roads[30], self.roads[31], self.roads[32], self.roads[33], self.nodes[33], self.nodes[34], self.nodes[35], self.nodes[36], self.nodes[37], self.hexes[23], self.hexes[24], self.hexes[25], self.hexes[26], self.nodes[38], self.nodes[39], self.nodes[40], self.nodes[41], self.nodes[42], self.roads[34], self.roads[35], self.roads[36], self.roads[37], self.roads[38], self.roads[39], self.roads[40], self.roads[41], self.nodes[43], self.nodes[44], self.nodes[45], self.nodes[46], self.hexes[29], self.hexes[30], self.hexes[31], self.nodes[47], self.nodes[48], self.nodes[49], self.nodes[50], self.roads[42], self.roads[43], self.roads[44], self.roads[45], self.roads[46], self.roads[47], self.nodes[51], self.nodes[52], self.nodes[53], msg)

    def isGameOver(self):
        return False

    def lookup(self, coord):
        coord = coord.lower()

        if coord in self.h_index:
            return self.hexes[self.h_index[coord]]
        elif coord in self.n_index:
            return self.nodes[self.n_index[coord]]
        elif coord in self.r_index:
            return self.roads[self.r_index[coord]]
        else:
            return False

    def cmd_info(self, coord):
        obj = self.lookup(coord)

        if obj == False:
            return 'Coordinate "%s" not found.' % coord
        else:
            return obj.show_info(coord)

    def cmd_neighbors(self, coord):
        obj = self.lookup(coord)

        if obj == False:
            return 'Coordinate "%s" not found.' % coord
        else:
            s = obj.show_info(coord)
            if type(obj) == type(self.hexes[0]):
                s += "\n > connections:\t{"
                for c in obj.conns:
                    s += str(c.num) + ", "
                s += "}"
            elif type(obj) == type(self.nodes[0]):
                s += "\n > connections:\t{"
                for c in obj.conns:
                    s += str(c.num) + ", "
                s += "}\n > roads:\t{"
                for r in obj.roads:
                    s += str(r.num) + ", "
                s += "}"
            elif type(obj) == type(self.roads[0]):
                s += "\n > nodes:\t{"
                for v in obj.vertices:
                    s += str(v.num) + ", "
                s += "}"
            return s

class Player(object):
    def __init__(self, num):
        self.num = num
        self.score = 0
        self.resCards = []
        self.devCards = []

    def __repr__(self):
        return u"Player %d" % (self.num + 1)

class Vertex(object):
    def __init__(self, num):
        self.num = num
        self.roads = set()
        self.conns = set()

    def add_road(self, road):
        self.roads.add(road)

    def add_conn(self, conn):
        self.conns.add(conn)

class Hex(Vertex):
    def __init__(self, num, isOcean, diceValue, resource):
        Vertex.__init__(self, num)
        self.resource = resource
        self.diceValue = diceValue
        self.isOcean = isOcean
        self.isBlocked = False
        if diceValue == 0 and isOcean == False:
            self.isBlocked = True

    def __repr__(self):
        s = u""
        if self.isBlocked:
            s += COLORS['b_white']
            s += COLORS['black']
            s += str(self.diceValue).rjust(2)
        elif not(self.isOcean):
            s += COLORS[self.resource]
            s += str(self.diceValue).rjust(2)
        s += COLORS['reset']
        return s

    def show_info(self, coord):
        s = u"%s = { type: HEX, resource: " % coord
        s += COLORS[self.resource] + self.resource.title() + COLORS['reset']
        s += ", diceroll: " + COLORS[self.resource] + str(self.diceValue) + COLORS['reset'] + ", is-blocked: " + COLORS['b_white'] + COLORS['black']
        if self.isBlocked:
            s += "YES"
        else:
            s += "NO"
        s += COLORS['reset'] + " }"
        return s

class Node(Vertex):
    def __init__(self, num):
        Vertex.__init__(self, num)
        self.owner = None
        self.isCity = False

    def __repr__(self):
        s = u""
        if self.owner != None:
            s += COLORS[str(self.owner)]
            if self.isCity:
                s += u"0"
            else:
                s += u"o"
            s += COLORS['reset']
        else:
            s += u"."
        return s

    def show_info(self, coord):
        s = u"%s = { type: NODE, owner: " % coord
        if self.owner == None:
            s += COLORS['b_white'] + COLORS['black'] + "NONE"
        else:
            s += COLORS[str(self.owner)] + "Player " + str(self.owner + 1)
        s += COLORS['reset'] + ", is-city: " + COLORS['b_white'] + COLORS['black']
        if self.isCity:
            s += "YES"
        else:
            s += "NO"
        s += COLORS['reset'] + " }"
        return s

    def make_city(self):
        self.isCity = True

class Edge(object):
    def __init__(self, num):
        self.num = num
        self.vertices = set()

    def set_vertices(self,u,v):
        self.vertices = {u,v}

class Road(Edge):
    def __init__(self, num):
        Edge.__init__(self, num)
        self.owner = None

    def __repr__(self):
        s = u""
        if self.owner != None:
            s += COLORS[str(self.owner)]
        if (self.num % 2 and self.num < 24) or ( self.num % 2 == 0 and self.num >= 24):
            s += "\\"
        else:
            s += "/"
        s += COLORS['reset']
        return s

    def show_info(self, coord):
        s = u"%s = { type: ROAD, owner: " % coord
        if self.owner == None:
            s += COLORS['b_white'] + COLORS['black'] + "NONE"
        else:
            s += COLORS[str(self.owner)] + "Player " + str(self.owner + 1)
        s += COLORS['reset'] + " }"
        return s

class Connection(Edge):
    def __init__(self, num):
        Edge.__init__(self, num)

    def __repr__(self):
        return "Connection(%s)" % ("<-->".join(str(e) for e in self.vertices))

def main():
    catan = Catan()
    catan.view('Welcome to CaTEXT, a text-based Catan game for your terminal!  If this is your\nfirst time, try typing "help".')

    while catan.isGameOver() != True:

        args = raw_input(': ')
        msg = catan.handle_input(args)

        catan.view(msg)

    return 0

if __name__ == "__main__":
    main()
