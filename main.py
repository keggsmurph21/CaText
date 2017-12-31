import gui, random

SETTINGS_BY_STYLE = {
    'standard': {
        'views': {'narrow', 'wide', },
        'narrow':{},
        'wide': {
            'border': True,
            'lpad':1,
            'mpad':3,
            'rpad':1,
            'order': [('tbanner',), ('game',('info',45,0),), ('lbanner',), ('pMsgs',), ('msg',),('prompt',),],
            'tbanner': u"&g/"+"="*33+" [ CaTEXT ] "+"="*33+"\\&&",
            'lbanner': u"&g\\"+"="*78+"/&&", },
        'prompt':" >",
        'genc':"  ObNdO5NdO5NdOb  \n  O9RsHtRbO1RsHtRbO1RsHtRbO9  \n  O7NdHfNdHfNdHfNdO7  \n  O7RvHxRvHxRvHxRvO7  \n  O7NdHgNdHgNdHgNdO7  \n  O5RsHtRbHbRsHtRbHbRsHtRbHbRsHtRbO5  \n  O3NdHfNdHfNdHfNdHfNdO3  \n  O3RvHxRvHxRvHxRvHxRvO3  \n  O3NdHgNdHgNdHgNdHgNdO3  \n  O1RsHtRbHbRsHtRbHbRsHtRbHbRsHtRbHbRsHtRbO1  \nNdHfNdHfNdHfNdHfNdHfNd\nRvHxRvHxRvHxRvHxRvHxRv\nNdHgNdHgNdHgNdHgNdHgNd\n  O1RbHbRsHtRbHbRsHtRbHbRsHtRbHbRsHtRbHbRsO1  \n  O3NdHfNdHfNdHfNdHfNdO3 \n  O3RvHxRvHxRvHxRvHxRvO3  \n  O3NdHgNdHgNdHgNdHgNdO3  \n  O5RbHbRsHtRbHbRsHtRbHbRsHtRbHbRsO5  \n  O7NdHfNdHfNdHfNdO7  \n  O7RvHxRvHxRvHxRvO7  \n  O7NdHgNdHgNdHgNdO7  \n  O9RbHbRsO1RbHbRsO1RbHbRsO9  \n  ObNdO5NdO5NdOb  ",
        'ienc':"s7Tas8\ns7Tbs8\nIt\nI s=|__NAME____VPs_Res_DCs_Army_|\nIm\nIb\ns7Das8\ns7Dbs8\nRt\nRss=|__RESOURCES_________Num____|\nRm\nRb\nVss=|__DEV CARDS_____Up__Down___|\nVm\nVb",
        'diceValues': [2,3,3,4,4,5,5,6,6,8,8,9,9,10,10,11,11,12],
        'resources': {
            'desert':   {'name':'Desert','tColor':'&dt','bColor':'&db','num':1,'isZero':True},
            'wheat':    {'name':'Wheat','tColor':'&at','bColor':'&ab','num':4,'isZero':False},
            'sheep':    {'name':'Sheep','tColor':'&st','bColor':'&sb','num':4,'isZero':False},
            'brick':    {'name':'Brick','tColor':'&rt','bColor':'&rb','num':3,'isZero':False},
            'wood':     {'name':'Wood','tColor':'&wt','bColor':'&wb','num':4,'isZero':False},
            'ore':      {'name':'Ore','tColor':'&ot','bColor':'&ob','num':3,'isZero':False}
        },
        'devCards': {
            'vp':       {'nameShort':'VP','nameLong':'Victory Point','namePlural':'VPs','num':5,'textColor':'&at'},
            'knight':   {'nameShort':'Knight','nameLong':'Knight','namePlural':'Knights','num':14,'textColor':'&p0'},
            'yop':      {'nameShort':'YoP','nameLong':'Year of Plenty','namePlural':'YoPs','num':32,'textColor':'&wt'},
            'monopoly': {'nameShort':'Monopoly','nameLong':'Monopoly','namePlural':'Monopolies','num':2,'textColor':'&wt'},
            'rb':       {'nameShort':'RB','nameLong':'Road Building','namePlural':'Road Builders','num':2,'textColor':'&wt'}
        },
        'colors':  {
            '&&':   u"\u001b[0m",           # RESET

            '&b':   u"\u001b[30m",          # black text
            '&g':   u"\u001b[38;5;244m",    # grey text
            '&~':   u"\u001b[38;5;234m\u001b[40m",    # ocean text
            '&_':   u"\u001b[47m",          # white bkg
            '&x':   u"\u001b[40m",          # robber

            '&dt':   u"\u001b[38;5;223m",   # desert text
            '&at':   u"\u001b[38;5;226m",   # wheat text
            '&st':   u"\u001b[38;5;155m",   # sheep text
            '&rt':   u"\u001b[38;5;208m",   # brick text
            '&wt':   u"\u001b[38;5;22m" ,   # wood text
            '&ot':   u"\u001b[38;5;240m",   # ore text
            '&db':   u"\u001b[48;5;223m\u001b[30m",    # desert bkg
            '&ab':   u"\u001b[48;5;226m\u001b[30m",    # wheat bkg
            '&sb':   u"\u001b[48;5;155m\u001b[30m",    # sheep bkg
            '&rb':   u"\u001b[48;5;208m",   # brick bkg
            '&wb':   u"\u001b[48;5;22m",    # wood bkg
            '&ob':   u"\u001b[48;5;240m",   # ore bkg

            '&p0':  u"\u001b[38;5;1m",      # player0 text
            '&p1':  u"\u001b[38;5;26m",     # player1 text
            '&p2':  u"\u001b[38;5;202m",    # player2 text
            '&p3':  u"\u001b[38;5;14m",     # player3 text
            '&P0':  u"\u001b[48;5;1m",      # player0 bkg
            '&P1':  u"\u001b[48;5;26m",     # player1 bkg
            '&P2':  u"\u001b[48;5;202m",    # player2 bkg
            '&P3':  u"\u001b[48;5;14m", } } }  # player3 bkg
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
        return self.dice[i].value

class Resource(object):
    def __init__(self, argv):
        self.resource = argv['name'].lower()
        self.name = argv['name']
        self.text = argv['tColor']
        self.bkg = argv['bColor']

class DevCard(object):
    def __init__(self, argv, func):
        self.name = argv['nameShort'].lower()
        self.short = argv['nameShort']
        self.long = argv['nameLong']
        self.plural = argv['namePlural']
        self.text = argv['textColor']
        self.func = func

    def do(player,action='draw'):
        return self.func(player,action)

class Catan(object):
    def __init__(self, numHumans, numCPUs):
        self.settings = SETTINGS_BY_STYLE['standard']

        self.turn = 0
        self.vpGoal = 10
        self.gui = gui.GUI(self)

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
        self.nonePlayer = Player(-1, self)

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
            't28':  31}
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
            'w28':  53}
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
            'v30':  71}
        self.hex_dots = { 0:0, 2:1, 3:2, 4:3, 5:4, 6:5, 8:5, 9:4, 10:3, 11:2, 12:1 } # for the computer

        self.cmds = {
            'info':     Cmd('info', ["coordinate (e.g. E24)"], self.cmd_info),
            'clear':    Cmd('clear', []),
            'help':     Cmd('help', ["command (e.g. info)"]),
            'abbrev':   Cmd('abbrev', [], self.cmd_abbrev),
            'n':        Cmd('n', ["coordinate (e.g. E24)"], self.cmd_neighbors, True),
            'roll':     Cmd('roll', [], self.roll),
            'reset':    Cmd('reset', [], self.reseed, True),
            'settle':   Cmd('settle', ["coordinate (e.g. E24) or opts"], self.cmd_settle),
            'pave':     Cmd('pave', ["coordinate (e.g. F26) or opts"], self.cmd_pave),
            'setname':  Cmd('setname', ["name (8 chars or less)"], self.cmd_setname),
            'setcpuname': Cmd('setcpuname', ["id (e.g. '4' for 'CPU 4')","name (8 chars or less)"], self.cmd_setcpuname)}

        self.devCards = {}
        self.resources = {}
        self.dcDeck = []

        self.reseed()

    def take_first_turn(self):
        self.turn += 1
        for p in self.players:
            self.currentPlayer = p
            p.settle()

        self.turn += 1
        for p in self.players[::-1]:
            self.currentPlayer = p
            p.settle()

        self.isFirstTurn = False

    def take_turn(self):
        self.turn += 1
        for p in self.players:
            self.currentPlayer = p
            p.take_turn()

        self.take_turn()

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
        self.take_turn()

        return "** RESEED **"

    def dc_vp(self, player, action):
        raise NotImplementedError

    def dc_knight(self, player, action):
        raise NotImplementedError

    def dc_yop(self, player, action):
        raise NotImplementedError

    def dc_monopoly(self, player, action):
        raise NotImplementedError

    def dc_rb(self, player, action):
        raise NotImplementedError

    def generate_board(self):
        self.hexes = []
        self.nodes = []
        self.roads = []
        self.conns = []

        # make the Dev Cards
        for key in self.settings['devCards'].keys():
            dc = self.settings['devCards'][key]
            if key == 'vp':
                func = self.dc_vp
            elif key == 'knight':
                func = self.dc_knight
            elif key == 'yop':
                func = self.dc_yop
            elif key == 'monopoly':
                func = self.dc_monopoly
            elif key == 'rb':
                func = self.dc_rb
            for num in range( dc['num'] ):
                devCard = DevCard( dc, func )
                self.devCards[key] = devCard
                self.dcDeck.append( devCard )


        # make the Hexes and Resources
        diceValues = self.settings['diceValues']
        random.shuffle(diceValues)
        resources = []
        for key in self.settings['resources'].keys():
            for num in range( self.settings['resources'][key]['num'] ):
                resources.append( key )
        random.shuffle(resources)
        for i in range(19):
            resource = resources.pop()
            resource = self.settings['resources'][resource]
            if resource['isZero']:
                diceValue = 0
            else:
                diceValue = diceValues.pop()
            resource = Resource( resource )
            self.hexes.append( Hex(i,False,diceValue,resource) )
            self.resources[resource.resource] = resource

        # makes the Nodes
        for i in range(54):
            self.nodes.append( Node(i, self.nonePlayer) )

        # make the Roads
        road_vertices = [(3,0),(0,4),(4,1),(1,5),(5,2),(2,6),(3,7),(4,8),(5,9),(6,10),(11,7),(7,12),(12,8),(8,13),(13,9),(9,14),(14,10),(10,15),(11,16),(12,17),(13,18),(14,19),(15,20),(21,16),(16,22),(22,17),(17,23),(23,18),(18,24),(24,19),(19,25),(25,20),(20,26),(21,27),(22,28),(23,29),(24,30),(25,31),(26,32),(27,33),(33,28),(28,34),(34,29),(29,35),(35,30),(30,36),(36,31),(31,37),(37,32),(33,38),(34,39),(35,40),(36,41),(37,42),(38,43),(43,39),(39,44),(44,40),(40,45),(45,41),(41,46),(46,42),(43,47),(44,48),(45,49),(46,50),(47,51),(51,48),(48,52),(52,49),(49,53),(53,50)]
        for i in range(72):
            self.roads.append( Road(i, self.nonePlayer) )
            road_n0 = self.nodes[road_vertices[i][0]]
            road_n1 = self.nodes[road_vertices[i][1]]
            self.roads[i].set_vertices(road_n0, road_n1)
            road_n0.add_road(self.roads[i])
            road_n1.add_road(self.roads[i])

        # make the Connections
        conn_vertices = [(0,0),(4,0),(8,0),(12,0),(7,0),(3,0), (1,1),(5,1),(9,1),(13,1),(8,1),(4,1), (2,2),(6,2),(10,2),(14,2),(9,2),(5,2), (7,3),(12,3),(17,3),(22,3),(16,3),(11,3), (8,4),(13,4),(18,4),(23,4),(17,4),(12,4), (9,5),(14,5),(19,5),(24,5),(18,5),(13,5), (10,6),(15,6),(20,6),(25,6),(19,6),(14,6), (16,7),(22,7),(28,7),(33,7),(27,7),(21,7), (17,8),(23,8),(29,8),(34,8),(28,8),(22,8), (18,9),(24,9),(30,9),(35,9),(29,9),(23,9),(19,10),(25,10),(31,10),(36,10),(30,10),(24,10), (20,11),(26,11),(32,11),(37,11),(31,11),(25,11), (28,12),(34,12),(39,12),(43,12),(38,12),(33,12), (29,13),(35,13),(40,13),(44,13),(39,13),(34,13), (30,14),(36,14),(41,14),(45,14),(40,14),(35,14), (31,15),(37,15),(42,15),(46,15),(41,15),(36,15), (39,16),(44,16),(48,16),(51,16),(47,16),(43,16), (40,17),(45,17),(49,17),(52,17),(48,17),(44,17), (41,18),(46,18),(50,18),(53,18),(49,18),(45,18)]
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

    def handle_input(self, msg=None, options={}):
        persistentOptions = {'info', 'clear', 'help', 'abbrev', 'setname', 'setcpuname'}

        if msg != None:
            self.gui.set_msg( msg )
        self.gui.render()
        args = self.gui.prompt().split(' ')
        cmd = args[0]

        if cmd in self.cmds.keys():
            cmd = self.cmds[cmd]

            if options != {} and cmd.name not in options and cmd.name not in persistentOptions:
                msg = u'%s: Could not execute.  &gCurrently available commands:PLY ' % cmd.name
                for opt in options:
                    msg += opt + ", "
                msg += "&&"
                for opt in persistentOptions:
                    msg += opt + ", "

            else:

                if cmd.name == 'help':
                    keys = sorted(self.cmds.keys())
                    if len(args) == 1:
                        msg = u'For help with a specific command, type "help {command}".\n&gCommands:&& '
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


        self.handle_input( msg, options )

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

    def lookup(self, coord, look=None):
        lists = { 'hexes' : self.h_index, 'nodes' : self.n_index, 'roads' : self.r_index }
        ret = False

        if look != None and look in lists:
            for item in lists[look].keys():
                if coord == lists[look][item]:
                    return item
        else:
            coord = coord.lower()

            if coord in self.h_index:
                ret = self.hexes[self.h_index[coord]]
            elif coord in self.n_index:
                ret = self.nodes[self.n_index[coord]]
            elif coord in self.r_index:
                ret = self.roads[self.r_index[coord]]

        return ret

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
        if coord == 'opts':
            msg = '&gAvailable locations to settle:&& '
            for node in self.nodes:
                if node.settle(self.currentPlayer, False) != False:
                    msg += '%s, ' % self.lookup(node.num, 'nodes')
            self.gui.set_msg( msg )
        else:
            node = self.lookup(coord)
            if node == False or type(node) != type(self.nodes[0]):
                return False
            if node.settle(self.currentPlayer) == False:
                return False

    def cmd_pave(self, coord):
        if coord == 'opts':
            msg = '&gAvailable locations to build a road:&& '
            for road in self.roads:
                if road.pave(self.currentPlayer, False) != False:
                    msg += '%s, ' % self.lookup(road.num, 'roads')
            self.gui.set_msg( msg )
        else:
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
                msg = "Successfully changed %s%s&& to %s%s&&" % (p.color, p.name, p.color, name[:8])
                p.name = name[:8]
                return msg
        return False

class Player(object):
    def __init__(self, num, catan):
        if num < 0:
            self.num = num
            self.score = 0
            self.resCards = { 'wheat':0, 'sheep':0, 'brick':0, 'wood':0, 'ore':0 } # resource cards
            self.devCardsU = { 'vp':0, 'knight':0, 'yop':0, 'monopoly':0, 'rb':0 } # played
            self.devCardsP = { 'vp':0, 'knight':0, 'yop':0, 'monopoly':0, 'rb':0 } # unplayed
            self.numKnights = 0
            self.hasLargestArmy = False
            self.color = u'&&'
            self.bcolor = u'&&'
            self.name = ''
            self.isHuman = False
            self.catan = catan
            self.settlements = []
            self.roads = []
            self.longestRoad = 0
            self.hasLongestRoad = False
            self.isNone = True
        else:
            self.num = num
            self.score = 0
            self.resCards = { 'wheat':0, 'sheep':0, 'brick':0, 'wood':0, 'ore':0 } # resource cards
            self.devCardsU = { 'vp':0, 'knight':0, 'yop':0, 'monopoly':0, 'rb':0 } # played
            self.devCardsP = { 'vp':0, 'knight':0, 'yop':0, 'monopoly':0, 'rb':0 } # unplayed
            self.numKnights = 0
            self.hasLargestArmy = False
            self.color = u'&p' + str(num)
            self.bcolor = u'&P' + str(num)
            self.name = ''
            self.isHuman = False
            self.catan = catan
            self.settlements = []
            self.roads = []
            self.longestRoad = 0
            self.hasLongestRoad = False
            self.isNone = False

    def print_line(self):
        return "%s %s %s  %s  %s   %s  &&" % (self.color, self.name.ljust(8), self.f(self.score), self.total(self.resCards), self.total(self.devCardsU), self.f(self.numKnights))

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

        self.catan.gui.add_pMsg( u"%s%s please choose a settlement (settle opts).&&" % (self.color, self.name) )
        self.catan.handle_input( None, {'settle'} )
        self.catan.gui.remove_pMsg()

        if self.catan.isFirstTurn:

            self.catan.gui.add_pMsg( u"%s%s please choose a road (pave opts).&&" % (self.color, self.name) )
            self.catan.handle_input( None, {'pave'} )
            self.catan.gui.remove_pMsg()

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
        self.color = resource.bkg
        self.diceValue = diceValue
        self.isOcean = isOcean
        self.isBlocked = False
        if diceValue == 0 and isOcean == False:
            self.isBlocked = True

    def escape(self, shape):
        s = self.color
        if shape == 'Hx':
            if self.isBlocked:
                s = '&x'
            s += " %2d  " % self.diceValue
        elif shape == 'Hf':
            s += "&& "
        elif shape == 'HF':
            s += "&& %s   && " % self.color
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
    def __init__(self, num, owner):
        Vertex.__init__(self, num)
        self.owner = owner
        self.isCity = False
        self.isSettleable = True

    def escape(self, shape=''):
        s = self.owner.bcolor
        if self.owner.isNone:
            s += u' . '
        elif self.isCity:
            s += u' C '
        else:
            s += u' s '
        return s

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

    def settle(self, player, save=True):
        if self.isSettleable:
            if save:
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
    def __init__(self, num, owner):
        Edge.__init__(self, num)
        self.owner = owner

    def pave(self, player, save=True):
        if self.owner == None:
            if player.catan.isFirstTurn:
                if True:#self in player.settlements[-1].roads: # check if adjacent to most recently placed settlement
                    if save:
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

    def escape(self, shape):
        s = self.owner.bcolor
        if shape == 'Rs':
            s += u' / '
        elif shape == 'Rb':
            s += u' \\ '
        elif shape == 'Rv':
            s += u' | '
        return s

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
