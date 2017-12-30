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
    'b_white':  u"\u001b[47m",
    'grey':     u"\u001b[38;5;244m",
    'ocean':    u"\u001b[38;5;234m",
    'b0':       u"\u001b[48;5;1m",
    'b1':       u"\u001b[48;5;26m",
    'b2':       u"\u001b[48;5;202m",
    'b3':       u"\u001b[48;5;14m"
}
DEBUG = True

class Cmd(object):
    def __init__(self, name, arg_desc, func=None, isDevCmd=False):
        self.name = name
        self.argc = len(arg_desc)
        self.argv = arg_desc
        self.func = func
        self.isDevCmd = isDevCmd

    def help_text(self):
        msg = u"Usage: " + self.name + " "
        for a in range(self.argc):
            msg += "$" + str(a+1) + " "
        msg += u"\t\u001b[38;5;244m"
        for a in range(self.argc):
            msg += str(a+1) + ": " + self.argv[a] + " "
        msg += u"\u001b[0m"
        if self.isDevCmd:
            msg += " (Note: this is a developer command)"

        return msg

    def wrong_args_text(self):
        return u'Command "%s" requires %s arguments.  For help, type "help".' % (self.name, str(self.argc))

    def do(self, args):
        if self.func == None:
            return ""
        return self.func(*args)

class Die(object):
    def __init__(self, initialValue=0):
        self.value = 0

    def __repr__(self):
        return str(self.value)

    def roll(self):
        self.value = random.randint(1,6)

class Dice(object):
    def __init__(self):
        self.dice = [ Die(), Die() ]

    def get_value(self):
        return self.dice[0].value + self.dice[1].value

    def roll(self):
        self.dice[0].roll()
        self.dice[1].roll()

        return self.get_value()

    def view(self,i):
        return self.dice[i]

class Catan(object):
    def __init__(self, numHumans, numCPUs):
        self.vpGoal = 10

        self.dice = Dice()
        self.hexes = []
        self.nodes = []
        self.roads = []
        self.conns = []

        self.numHumans = numHumans
        self.numCPUs = numCPUs
        self.players = []
        self.currentPlayer = None
        self.hasLargestArmy = None
        self.hasLongestRoad = None
        self.isFirstTurn = True

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
        self.hex_dots = { 0:0, 2:1, 3:2, 4:3, 5:4, 6:5, 8:5, 9:4, 10:3, 11:2, 12:1 }

        self.cmds = {
            'info':     Cmd('info', ["coordinate (e.g. E24)"], self.cmd_info),
            'clear':    Cmd('clear', []),
            'help':     Cmd('help', ["command (e.g. info)"]),
            'abbrev':   Cmd('abbrev', [], self.cmd_abbrev),
            'n':        Cmd('n', ["coordinate (e.g. E24)"], self.cmd_neighbors, True),
            'roll':     Cmd('roll', [], self.roll),
            'reset':    Cmd('reset', [], self.reseed, True),
            'settle':   Cmd('settle', ["coordinate (e.g. E24)"], self.cmd_settle),
            'pave':     Cmd('pave', ["coordinate (e.g. F26)"], self.cmd_pave),
            'setname':  Cmd('setname', ["name (8 chars or less)"], self.cmd_setname),
            'setcpuname': Cmd('setcpuname', ["id (e.g. '4' for 'CPU 4')","name (8 chars or less)"], self.cmd_setcpuname)
        }

        self.devCardDeck = []

        self.reseed()

    def take_first_turn(self):
        for p in self.players:
            self.currentPlayer = p
            p.settle()
        for p in self.players[::-1]:
            self.currentPlayer = p
            p.settle()

        self.isFirstTurn = False
        self.view('awaiting command')

    def roll(self):
        diceValue = self.dice.roll()

        if diceValue == 7:
            return "Robber!!"
        else:
            for h in self.hexes:
                if h.diceValue == diceValue and h.isBlocked == False:
                    for n in h.get_adj_nodes():
                        if n.owner != None:
                            n.owner.resCards[h.resource] += 1

            if diceValue in {8,11}:
                return "You rolled an %d." % diceValue
            return "You rolled a %d." % diceValue

    def reseed(self):
        self.generate_board()
        self.generate_players()
        self.take_first_turn()

        return "** RESEED **"

    def generate_board(self):
        self.hexes = []
        self.nodes = []
        self.roads = []
        self.conns = []

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

    def generate_players(self):
        self.players  = [ Human(i, self) for i in range(self.numHumans) ]
        self.players += [ CPU(self.numHumans + i, self) for i in range(self.numCPUs)]
        random.shuffle(self.players)

    def handle_input(self, in_msg="", msg=None, options={}):
        persistentOptions = {'info', 'clear', 'help', 'abbrev', 'setname', 'setcpuname'}

        if msg != None:
            self.view( in_msg + "\n" + self.printf(msg) )
        else:
            self.view( in_msg )
        args = raw_input('> ').split(' ')
        cmd = args[0]

        if cmd in self.cmds.keys():
            cmd = self.cmds[cmd]

            if options != {} and cmd.name not in options and cmd.name not in persistentOptions:
                msg = u'%s: Could not execute.  GRYCurrently available commands:PLY ' % cmd.name
                for opt in options:
                    msg += opt + ", "
                msg += "ReS"
                for opt in persistentOptions:
                    msg += opt + ", "

            else:

                if cmd.name == 'help':
                    keys = sorted(self.cmds.keys())
                    if len(args) == 1:
                        msg = u'For help with a specific command, type "help {command}".\nGRYCommands:ReS '
                        for key in keys:
                            if DEBUG == True or self.cmds[key].isDevCmd == False:
                                msg += self.cmds[key].name + ", "
                    else:
                        if args[1] in keys:
                            cmd = self.cmds[args[1]]
                            msg = cmd.help_text()
                        else:
                            msg = '%s: Unrecognized command.  For a list of commands, type "help".' % args[1]
                    if options == {}:
                        return

                else:
                    if len(args) - 1 == cmd.argc:
                        if DEBUG == True or cmd.isDevCmd == False:
                            msg = cmd.do(args[1:])
                            if msg == False:
                                msg = "Error executing %s.  Make sure all arguments are correct." % cmd.name
                            else:
                                if options == {} or cmd.name in options:
                                    return
                        else:
                            msg = "%s: Could not execute because developer commands are disabled for this session." % cmd.name
                    else:
                        msg = cmd.wrong_args_text()

        else:
            msg = '%s: Unrecognized command.  For a list of commands, type "help".' % cmd

        self.handle_input( in_msg, msg, options )

    def printf(self, line):
        line = line.replace(u"ReS", COLORS['reset'])
        line = line.replace(u"GRY", COLORS['grey'])
        line = line.replace(u"RED", COLORS['0'])
        line = line.replace(u"BLU", COLORS['1'])
        line = line.replace(u"YEL", COLORS['wheat'])
        line = line.replace(u"LGR", COLORS['sheep'])
        line = line.replace(u"ORA", COLORS['brick'])
        line = line.replace(u"DGR", COLORS['wood'])
        line = line.replace(u"ORE", COLORS['ore'])
        line = line.replace(u"OCE", COLORS['ocean'])
        line = line.replace(u"PLY", self.currentPlayer.color)

        return line

    def view(self, msg):
        os.system('cls' if os.name == 'nt' else 'clear')

        board = u""

        board += self.printf( u"GRY/================================ [ CaTEXT ] ==================================\\\n")
        board += self.printf( u"   0         1         2         3         4\n" )
        board += self.printf( u"   01234567890123456789012345678901234567890ReS    .___________________________.GRY\n" )
        board += self.printf( u" AOCE ~~~~~~~~~~~ReS%sOCE~~~~~ReS%sOCE~~~~~ReS%sOCE~~~~~~~~~~~ GRYAReS  |__NAME____VPs_Res_DCs_Army_|GRY\n" %                                              (self.nodes[0], self.nodes[1], self.nodes[2]) )
        board += self.printf( u" BOCE ~~~~~~~~~ReS%s %sOCE~ReS%s %sOCE~ReS%s %sOCE~~~~~~~~~ GRYBReS  |%s|GRY\n" %                                           (self.roads[0], self.roads[1], self.roads[2], self.roads[3], self.roads[4], self.roads[5], self.players[0].print_line()) )
        board += self.printf( u" COCE ~~~~~~~ReS%s     %s     %s     %sOCE~~~~~~~ GRYCReS  |%s|GRY\n" %                                                         (self.nodes[3], self.nodes[4], self.nodes[5], self.nodes[6], self.players[1].print_line()) )
        board += self.printf( u" DOCE ~~~~~~~ReS%s %s  %s %s  %s %s  %sOCE~~~~~~~ GRYDReS  |%s|GRY\n" %                                                         (self.roads[6], self.hexes[5], self.roads[7], self.hexes[6], self.roads[8], self.hexes[7], self.roads[9], self.players[2].print_line()) )
        board += self.printf( u" EOCE ~~~~~~~ReS%s     %s     %s     %sOCE~~~~~~~ GRYEReS  |%s|GRY\n" %                    (self.nodes[7], self.nodes[8], self.nodes[9], self.nodes[10], self.players[3].print_line()) )
        board += self.printf( u" FOCE ~~~~~ReS%s %s %s %s %s %s %s %sOCE~~~~~ GRYFReS  |___________________________|GRY\n" %                (self.roads[10], self.roads[11], self.roads[12], self.roads[13], self.roads[14], self.roads[15], self.roads[16], self.roads[17]) )
        board += self.printf( u" GOCE ~~~ReS%s     %s     %s     %s     %sOCE~~~ GRYGReS                ._. ._.GRY\n" %                                     (self.nodes[11], self.nodes[12], self.nodes[13],  self.nodes[14], self.nodes[15]) )
        board += self.printf( u" HOCE ~~~ReS%s %s  %s %s  %s %s  %s %s  %sOCE~~~ GRYHReS         Dice:  |%s| |%s|GRY\n" %                                               (self.roads[18], self.hexes[10], self.roads[19], self.hexes[11], self.roads[20], self.hexes[12], self.roads[21], self.hexes[13], self.roads[22],self.dice.view(0),self.dice.view(1)) )
        board += self.printf( u" IOCE ~~~ReS%s     %s     %s     %s     %sOCE~~~ GRYI\n" %                                            (self.nodes[16], self.nodes[17], self.nodes[18], self.nodes[19], self.nodes[20]) )
        board += self.printf( u" JOCE ~ReS%s %s %s %s %s %s %s %s %s %sOCE~ GRYJ  PLY.___________________________.GRY\n" %                                       (self.roads[23], self.roads[24], self.roads[25], self.roads[26], self.roads[27], self.roads[28], self.roads[29], self.roads[30], self.roads[31], self.roads[32]) )
        board += self.printf( u" KReS%s     %s     %s     %s     %s     %sGRYK  PLY|__RESOURCES_________Num____|GRY\n" %                        (self.nodes[21], self.nodes[22], self.nodes[23], self.nodes[24], self.nodes[25], self.nodes[26]) )
        board += self.printf( u" LReS%s %s  %s %s  %s %s  %s %s  %s %s  %sGRYL  PLY|YEL Wheat               %s    PLY|GRY\n" %                        (self.roads[33], self.hexes[16], self.roads[34], self.hexes[17], self.roads[35], self.hexes[18], self.roads[36], self.hexes[19], self.roads[37], self.hexes[20], self.roads[38], self.currentPlayer.count('wheat')) )
        board += self.printf( u" MReS%s     %s     %s     %s     %s     %sGRYM  PLY|LGR Sheep               %s    PLY|GRY\n" %                  (self.nodes[27], self.nodes[28], self.nodes[29], self.nodes[30], self.nodes[31], self.nodes[32], self.currentPlayer.count('sheep')) )
        board += self.printf( u" NOCE ~ReS%s %s %s %s %s %s %s %s %s %sOCE~ GRYN  PLY|ORA Brick               %s    PLY|GRY\n" %        (self.roads[39], self.roads[40], self.roads[41], self.roads[42], self.roads[43], self.roads[44], self.roads[45], self.roads[46], self.roads[47], self.roads[48], self.currentPlayer.count('brick')) )
        board += self.printf( u" OOCE ~~~ReS%s     %s     %s     %s     %sOCE~~~ GRYO  PLY|DGR Wood                %s    PLY|GRY\n" %             (self.nodes[33], self.nodes[34], self.nodes[35], self.nodes[36], self.nodes[37], self.currentPlayer.count('wood')) )
        board += self.printf( u" POCE ~~~ReS%s %s  %s %s  %s %s  %s %s  %sOCE~~~ GRYP  PLY|ORE Ore                 %s    PLY|GRY\n" %             (self.roads[49], self.hexes[23], self.roads[50], self.hexes[24], self.roads[51], self.hexes[25], self.roads[52], self.hexes[26], self.roads[53], self.currentPlayer.count('ore')) )
        board += self.printf( u" QOCE ~~~ReS%s     %s     %s     %s     %sOCE~~~ GRYQ  PLY|___________________________|GRY\n" %             (self.nodes[38], self.nodes[39], self.nodes[40], self.nodes[41], self.nodes[42]) )
        board += self.printf( u" ROCE ~~~~~ReS%s %s %s %s %s %s %s %sOCE~~~~~ GRYR  PLY|__DEV CARDS_____Up__Down___|GRY\n" %                (self.roads[54], self.roads[55], self.roads[56], self.roads[57], self.roads[58], self.roads[59], self.roads[60], self.roads[61]) )
        board += self.printf( u" SOCE ~~~~~~~ReS%s     %s     %s     %sOCE~~~~~~~ GRYS  PLY|YEL VPs            %s   %s    PLY|GRY\n" %                    (self.nodes[43], self.nodes[44], self.nodes[45], self.nodes[46], self.currentPlayer.count('vp','up'), self.currentPlayer.count('vp','down')) )
        board += self.printf( u" TOCE ~~~~~~~ReS%s %s  %s %s  %s %s  %sOCE~~~~~~~ GRYT  PLY|RED Knights        %s   %s    PLY|GRY\n" %              (self.roads[62], self.hexes[29], self.roads[63], self.hexes[30], self.roads[64], self.hexes[31], self.roads[65], self.currentPlayer.count('knight','up'), self.currentPlayer.count('knight','down')) )
        board += self.printf( u" UOCE ~~~~~~~ReS%s     %s     %s     %sOCE~~~~~~~ GRYU  PLY|DGR YoPs           %s   %s    PLY|GRY\n" %              (self.nodes[47], self.nodes[48], self.nodes[49], self.nodes[50], self.currentPlayer.count('yop','up'), self.currentPlayer.count('yop','down')) )
        board += self.printf( u" VOCE ~~~~~~~~~ReS%s %sOCE~ReS%s %sOCE~ReS%s %sOCE~~~~~~~~~ GRYV  PLY|DGR Monopolies     %s   %s    PLY|GRY\n" % (self.roads[66], self.roads[67], self.roads[68], self.roads[69], self.roads[70], self.roads[71], self.currentPlayer.count('monopoly','up'), self.currentPlayer.count('monopoly','down')) )
        board += self.printf( u" WOCE ~~~~~~~~~~~ReS%sOCE~~~~~ReS%sOCE~~~~~ReS%sOCE~~~~~~~~~~~ GRYW  PLY|DGR Road Builders  %s   %s    PLY|GRY\n" %   (self.nodes[51], self.nodes[52], self.nodes[53], self.currentPlayer.count('rb','up'), self.currentPlayer.count('rb','down')) )
        board += self.printf( u"   01234567890123456789012345678901234567890    PLY|___________________________|GRY\n" % () )
        board += self.printf( u"   0         1         2         3         4  \n" % () )
        board += self.printf( u"\\==============================================================================/ReS\t\n" )
        board += self.printf( u"%s" % msg )

        print board

    def is_game_over(self):
        for player in self.players:
            if player.score >= self.vpGoal:
                print "%s wins!" % player.name
                exit()

    def checkLongestRoad(self):
        if self.hasLongestRoad != None:
            currentHolder = self.hasLongestRoad
            currentLongestRoad = currentHolder.longestRoad
        else:
            currentLongestRoad = 0
        for player in self.players:
            if player.longestRoad > currentLongestRoad:
                currentHolder = player
                currentLongestRoad = currentHolder.longestRoad
        if currentLongestRoad > 4:
            if currentHolder != self.hasLongestRoad:
                currentHolder.hasLongestRoad = True
                currentHolder.score += 2
                if self.hasLongestRoad != None:
                    self.hasLongestRoad.hasLongestRoad = False
                    self.hasLongestRoad.score -= 2
                self.hasLongestRoad = currentHolder
        self.is_game_over()

    def get_player_by_id(self, i):
        for p in self.players:
            if p.num == i:
                return p
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

    def cmd_abbrev(self):
        return "List of abbreviations:\nVPs=Victory points, Res=Resource cards, DCs=(Unplayed) development cards,\nArmy=Number of knights (player with largest army has a star *),\nUp=Unplayed development cards, Down=Played development cards"

    def cmd_settle(self, coord):
        node = self.lookup(coord)
        if node == False or type(node) != type(self.nodes[0]):
            return False
        if node.settle(self.currentPlayer) == False:
            return False

    def cmd_pave(self, coord):
        road = self.lookup(coord)
        if road == False or type(road) != type(self.roads[0]):
            return False
        if road.pave(self.currentPlayer) == False:
            return False
        return self.currentPlayer.add_road(road)

    def cmd_setname(self, name):
        self.currentPlayer.name = name[:8]

    def cmd_setcpuname(self, i, name):
        p = self.get_player_by_id(int(i)-1)
        if p != False:
            if type(p) == type(CPU(0, self)):
                msg = "Successfully changed %s%sReS to %s%sReS" % (p.color, p.name, p.color, name[:8])
                p.name = name[:8]
                return msg
        return False

class Player(object):
    def __init__(self, num, catan):
        self.num = num
        self.score = 0
        self.resCards = { 'wheat':0, 'sheep':0, 'brick':0, 'wood':0, 'ore':0 } # resource cards
        self.devCardsU = { 'vp':0, 'knight':0, 'yop':0, 'monopoly':0, 'rb':0 } # played
        self.devCardsP = { 'vp':0, 'knight':0, 'yop':0, 'monopoly':0, 'rb':0 } # unplayed
        self.numKnights = 0
        self.hasLargestArmy = False
        self.color = COLORS[str(num)]
        self.bcolor = COLORS['b' + str(num)]
        self.name = ''
        self.isHuman = False
        self.catan = catan
        self.settlements = []
        self.roads = []
        self.longestRoad = 0
        self.hasLongestRoad = False

    def print_line(self):
        return "%s %s %s  %s  %s   %s  %s" % (self.color, self.name.ljust(8), self.f(self.score), self.total(self.resCards), self.total(self.devCardsU), self.f(self.numKnights), COLORS['reset'])

    def total(self, dic):
        acc = 0
        for key in dic.keys():
            acc += dic[key]
        return self.f(acc)

    def f(self, num, rjust=2): # format
        return str(num).rjust(rjust)

    def count(self, res, within='resources'):
        if within == 'up':
            dic = self.devCardsU
        elif within == 'down':
            dic = self.devCardsP
        else:
            dic = self.resCards
        return str(dic[res]).rjust(2)

    def calc_longest_road(self):
        longestRoad = 0
        self.longestRoad = longestRoad
        self.catan.checkLongestRoad()

    def add_settlement(self, node):
        self.score += 1
        self.settlements.append(node)

    def add_road(self, road):
        self.roads.append(road)
        self.calc_longest_road()

class Human(Player):
    def __init__(self, num, catan):
        Player.__init__(self, num, catan)
        self.isHuman = True
        self.name = "Player " + str(self.num + 1)

    def settle(self):
        self.catan.handle_input( u"PLY%s please choose a settlement (settle $1).ReS" % self.name, None, {'settle'} )
        if self.catan.isFirstTurn:
            self.catan.handle_input( u"PLY%s please choose a road (pave $1).ReS" % self.name, None, {'pave'})

class CPU(Player):
    def __init__(self, num, catan):
        Player.__init__(self, num, catan)
        self.name = "CPU " + str(self.num + 1)

    def settle(self):
        bestNode = None
        bestTotal = 0
        for node in self.catan.nodes:
            if node.isSettleable:
                thisTotal = 0
                for adj_hex in node.get_adj_hexes():
                    thisTotal += self.catan.hex_dots[adj_hex.diceValue]
                if thisTotal > bestTotal:
                    bestNode = node
                    bestTotal = thisTotal
        bestNode.settle(self)

        if self.catan.isFirstTurn:
            self.pave(bestNode)

    def pave(self, restrict=None):
        if self.catan.isFirstTurn:
            r = random.choice(self.settlements[-1].roads)
            r.pave(self)

class Vertex(object):
    def __init__(self, num):
        self.num = num
        self.roads = []
        self.conns = []

    def add_road(self, road):
        self.roads.append(road)

    def add_conn(self, conn):
        self.conns.append(conn)

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

    def get_adj_nodes(self):
        nodes = []
        for c in self.conns:
            nodes.append(c.vertices[0])
        return nodes

class Node(Vertex):
    def __init__(self, num):
        Vertex.__init__(self, num)
        self.owner = None
        self.isCity = False
        self.isSettleable = True

    def __repr__(self):
        s = u""
        if self.owner != None:
            s += self.owner.bcolor
            if self.isCity:
                s += u" C "
            else:
                s += u" s "
            s += COLORS['reset']
        else:
            s += u" . "
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
        s += COLORS['reset'] + ", is-settleable: " + COLORS['b_white'] + COLORS['black']
        if self.isSettleable:
            s += "YES"
        else:
            s += "NO"
        s += COLORS['reset'] + " }"
        return s

    def settle(self, player):
        if self.isSettleable:
            self.owner = player
            self.isSettleable = False
            for adj_node in self.get_adj_nodes():
                adj_node.isSettleable = False
            player.add_settlement(self)
            return True

        return False

    def make_city(self):
        self.isCity = True

    def get_adj_nodes(self):
        nodes = []
        for r in self.roads:
            if r.vertices[0].num != self.num:
                nodes.append(r.vertices[0])
            else:
                nodes.append(r.vertices[1])
        return nodes

    def get_adj_hexes(self):
        hexes = []
        for c in self.conns:
            hexes.append(c.vertices[1])
        return hexes

class Edge(object):
    def __init__(self, num):
        self.num = num
        self.vertices = []

    def set_vertices(self,u,v):
        self.vertices = [u,v]

class Road(Edge):
    def __init__(self, num):
        Edge.__init__(self, num)
        self.owner = None

    def pave(self, player):
        if self.owner == None:
            if player.catan.isFirstTurn:
                if self in player.settlements[-1].roads: # check if adjacent to most recently placed city
                    self.owner = player
                    player.add_road(self)
                    return True
            else:
                for r in player.roads:
                    if self.calc_distance(r) <= 1: # check if adjacent to any other built roads
                        self.owner = player
                        player.add_road(self)
                        return True

        return False

    def __repr__(self):
        s = u""
        if self.owner != None:
            s += self.owner.bcolor
        if self.num in {0,2,4,10,12,14,16,23,25,27,29,31,40,42,44,46,48,55,57,59,61,67,69,71}:
            s += " / "
        elif self.num in {1,3,5,11,13,15,17,24,26,28,30,32,39,41,43,45,47,54,56,58,60,66,68,70}:
            s += " \\ "
        elif self.num in {6,7,8,9,18,19,20,21,22,33,34,35,36,37,38,49,50,51,52,53,62,63,64,65}:
            s += " | "
        else:
            return "?"
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
    catan = Catan(1,3)
    #catan.view('Welcome to CaTEXT, a text-based Catan game for your terminal!  If this is your\nfirst time, try typing "help".')

    while catan.is_game_over() != True:
        pass

    return 0

if __name__ == "__main__":
    main()
