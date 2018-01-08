import datetime, gui, json, os, random

DEBUG = True
STYLE = 'standard'

class Settings(object):
    def __init__(self, style, numHumans, numCPUs, savepath=None):
        with open('settings.json', 'r') as f:
            data = json.load( f )
        self.data = data[style]
        self.data['numHumans'] = numHumans
        self.data['numCPUs'] = numCPUs
        if savepath == None:
            self.data['savepath'] = self.make_save_path()
        else:
            self.data['savepath'] = savepath

    def make_save_path(self):
        # generate a new save directory
        num = 0
        path = './saves/game_%d/' % num
        while os.path.exists( path ):
            num += 1
            path = './saves/game_%d/' % num
        os.mkdir( path )

        with open( '%sdata.txt' % path, 'w' ) as f:
            f.write( 'humans:%d, CPUs:%d, turn:%d, modified:%s' % (self.data['numHumans'], self.data['numCPUs'], 0, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") ) )

        return path

    def get(self, key):
        return self.data[key]

    def set(self, key, value):
        self.data[key] = value

class Cmd(object):
    def __init__(self, name, func, d):
        self.name = name
        self.argv = d['args']
        self.argc = len(self.argv)
        self.func = func
        self.isAdminCommand = d['isAdminCommand']
        self.isPersistentCommand = d['isPersistentCommand']

    def help_text(self):
        msg = u"Usage: " + self.name + " "
        for a in range(self.argc):
            msg += "$" + str(a+1) + " "
        msg += u"\t\u001b[38;5;244m"
        for a in range(self.argc):
            msg += str(a+1) + ": " + self.argv[a] + " "
        msg += u"\u001b[0m"
        if self.isAdminCommand:
            msg += " (Note: this is a developer command)"

        return msg

    def wrong_args_text(self):
        return u'Command "%s" requires %s arguments.  For help, type "help".' % (self.name, str(self.argc))

    def do(self, args):
        return self.func(args)

class Die(object):
    def __init__(self, initialValue=0):
        self.value = 0

    def roll(self):
        self.value = random.randint(1,6)

class Dice(object):
    def __init__(self):
        self.dice = [ Die(), Die() ]

    def save(self, keyword):
        if keyword == 'public':
            d = {
                '0': self.view(0),
                '1': self.view(1)}
        return d

    def load(self, data):
        self.dice[0].value = data['0']
        self.dice[1].value = data['1']

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
    def __init__(self, argv):
        self.name = argv['nameShort'].lower()
        self.short = argv['nameShort']
        self.long = argv['nameLong']
        self.plural = argv['namePlural']
        self.text = argv['textColor']

        if self.name == 'vp':
            self.func = self.dc_vp
        elif self.name == 'knight':
            self.func = self.dc_knight
        elif self.name == 'yop':
            self.func = self.dc_yop
        elif self.name == 'monopoly':
            self.func = self.dc_monopoly
        elif self.name == 'rb':
            self.func = self.dc_rb

    def do(player,action='draw'):
        return self.func(player,action)

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

class Options(object):
    def __init__(self, catan):
        self.data = { 'admin':{}, 'all':{}, 'available':{}, 'persistent':{} }
        self.catan = catan
        funcs = {
            'quit':         self.c_quit,
            'load':         self.c_load,
            'force':        self.c_force,
            'info':         self.c_info,
            'clear':        self.c_clear,
            'help':         self.c_help,
            'abbrev':       self.c_abbrev,
            'neighbors':    self.c_neighbors,
            'roll':         self.c_roll,
            'reset':        self.c_reset,
            'settle':       self.c_settle,
            'pave':         self.c_pave,
            'setname':      self.c_setname,
            'setcpuname':   self.c_setcpuname,
            'build':        self.c_build,
            'flip':         self.c_flip,
            'pass':         self.c_pass}

        commands = catan.settings.get('commands')
        for key in commands.keys():
            command = Cmd( key, funcs[key], commands[key]  )
            if command.isAdminCommand:
                self.data['admin'][key] = command
                self.data['persistent'][key] = command
            if command.isPersistentCommand:
                self.data['persistent'][key] = command
            self.data['all'][key] = command

    def dump(self, within='all'):
        return self.data[within].keys()

    def get(self, key, within='all'):
        return self.data[within][key]

    def set(self, options={}):
        self.data['available'] = {}
        if options == {}:
            options = self.dump()
        for opt in options:
            self.data['available'][opt] = self.get( opt )
        return self.data['available']

    def add(self, opt):
        self.data['available'][opt] = self.get( opt )

    def remove(self, options={}):
        for opt in options:
            self.data['available'].pop( opt, None )

    def c_quit(self, args):
        exit()

    def c_load(self, args):
        if len(args) < 3:
            if len(args) == 2:
                if args[1] == 'opts':
                    msg = '&gAvailable save files:&&\n  '
                    for f in sorted( os.listdir('saves') ):
                        msg += '%s ( ' % f.replace('game_', '')
                        with open( 'saves/%s/data.txt' % f, 'r' ) as g:
                            msg += g.readline()
                        msg += ' ),\n  '
                    self.catan.gui.set_msg( msg )
                    return False
                try:
                    path = 'saves/game_%d/' % int(args[1])
                except ValueError:
                    self.catan.gui.set_msg( "load: Unable to load game `%s`. For a list of available options, try load opts." % args[1])
                    return False
            else:
                path = 'saves/%s/' % sorted(os.listdir('saves')).pop()

            path = '%s%s/' % ( path, sorted(os.listdir(path)).pop() )
            ret = self.catan.loadGame( path )
            if ret == True:
                if self.catan.turn == 1:
                    self.catan()
                self.catan.gui.set_msg( "load: Successfully loaded %s." % args[1] )
                return True
            else:
                self.catan.gui.set_msg( ret )
                return False

        elif len(args) == 3 and self.catan.isAuthenticated( args[0] ) and args[1] == 'h':
            try:
                path = 'hardsaves/game_%d/' % int(args[2])
                for f in os.listdir( 'tmp' ):
                    os.remove(f)
            except ValueError:
                self.catan.gui.set_msg( "load: Unable to load game `%s`.  For a list of available options, try load opts." % args[2])

            ret = self.catan.loadGame( path )
            if ret == True:
                if self.catan.turn == 1:
                    self.catan()
                self.catan.gui.set_msg( "load: Successfully loaded %s." % args[1] )
                self.catan.settings.set( 'savepath', 'tmp' )
                print self.catan.settings.get( 'savepath' )
                return True
            else:
                self.catan.gui.set_msg( ret )
                return False

        else:
            self.catan.gui.set_msg( "load: Invalid number of arguments.  Expected 0 or 1, got %d." % (len(args)-1) )

    def c_force(self, args):
        if len(args) > 1:
            return self.get( args[1] ).do( args[1:] )
        else:
            self.catan.gui.set_msg( "force: Invalid number of arguments.  Expected at least argument, got 0." )

    def c_info(self, args):
        if len(args) == 2:
            obj = self.catan.lookup(args[1])

            if obj == False:
                self.catan.gui.set_msg( 'info: Coordinate "%s" not found.' % args[1] )
            else:
                self.catan.gui.set_msg( obj.show_info(self.catan, args[1]) )
                return True
        else:
            self.catan.gui.set_msg( "info: Invalid number of arguments.  Expected 1, got %d." % (len(args)-1) )

    def c_clear(self, args):
        self.catan.gui.set_msg( None )
        return True

    def c_help(self, args):
        keys = self.dump()

        if len(args) == 1:
            msg = u'For help with a specific command, type "help {command}".\n&gCommands:&& '
            for key in keys:
                if self.catan.isAuthenticated( key ):
                    msg += self.get(key).name + ", "
            self.catan.gui.set_msg( msg )
            return True
        elif len(args) == 2:
            if args[1] in keys:
                self.catan.gui.set_msg( self.get( args[1] ).help_text() )
                return True
            else:
                self.catan.gui.set_msg( '%s: Unrecognized command.  For a list of commands, type "help".' % args[1] )
        else:
            return "help: Invalid number of arguments.  Expected 0 or 1, got %d." % (len(args)-1)

    def c_roll(self, args):
        self.catan.gui.set_msg()
        self.catan.gui.remove_pMsg()
        self.catan.roll()
        self.catan.hasRolled = True
        return True

    def c_reset(self, args):
        self.catan.gui.remove_pMsg( 'all' )
        self.catan.gui.set_msg( "reset: Successfully reset board." )
        self.catan.reseed()
        self.catan.loop( 0 )
        return True

    def c_neighbors(self, args):
        if len(args) == 2:
            obj = self.catan.lookup( args[1] )

            if obj == False:
                self.catan.gui.set_msg( 'Coordinate "%s" not found.' % args[1] )
            else:
                s = obj.show_info( self.catan, args[1] )
                if isinstance( obj, Hex ):
                    s += "\n - connections:\t{"
                    for c in obj.conns:
                        s += str(c.num) + ", "
                    s += "}"
                elif isinstance( obj, Node ):
                    s += "\n - connections:\t{"
                    for c in obj.conns:
                        s += str(c.num) + ", "
                    s += "}\n - roads:\t{"
                    for r in obj.roads:
                        s += str(r.num) + ", "
                    s += "}"
                elif isinstance( obj, Road ):
                    s += "\n - nodes:\t{"
                    for v in obj.vertices:
                        s += str(v.num) + ", "
                    s += "}"
                self.catan.gui.set_msg( s )
                return True
        else:
            self.catan.gui.set_msg( "neighbors: Invalid number of arguments.  Expected 1, got %d." % (len(args)-1) )

    def c_abbrev(self, args):
        self.catan.gui.set_msg( "List of abbreviations:\nVPs=Victory points, Res=Resource cards, DCs=(Unplayed) development cards,\nArmy=Number of knights (player with largest army has a star *),\nUp=Unplayed development cards, Down=Played development cards" )
        return True

    def c_settle(self, args):
        if len(args) == 2:
            if args[1] == 'opts':
                msg = '&gAvailable locations to settle:&& '
                for node in self.catan.nodes:
                    if node.settle(self.catan.currentPlayer, False) == True:
                        msg += '%s, ' % self.catan.lookup(node.num, 'nodes')
                self.catan.gui.set_msg( msg )
            else:
                node = self.catan.lookup( args[1] )
                if node == False or not( isinstance(node, Node) ):
                    self.catan.gui.set_msg( "settle: Error square %s is not a node." % args[1] )
                    return False
                ret = node.settle( self.catan.currentPlayer )
                if ret == True:
                    self.catan.gui.set_msg( "settle: Settled square %s." % args[1] )
                    return True
                else:
                    self.catan.gui.set_msg( ret )
                    return False
        else:
            self.catan.gui.set_msg( "settle: Invalid number of arguments.  Expected 1, got %d." % (len(args)-1) )

    def c_pave(self, args):
        if len(args) == 2:
            if args[1] == 'opts':
                msg = '&gAvailable locations to build a road:&& '
                for road in self.catan.roads:
                    if road.pave(self.catan.currentPlayer, False) == True:
                        msg += '%s, ' % self.catan.lookup(road.num, 'roads')
                self.catan.gui.set_msg( msg )
            else:
                road = self.catan.lookup( args[1] )
                if road == False or not( isinstance(road, Road) ):
                    self.catan.gui.set_msg( "pave: Error square %s is not a road." % args[1] )
                    return False
                ret = road.pave( self.catan.currentPlayer )
                if ret == True:
                    self.catan.gui.set_msg( "pave: Paved square %s." % args[1] )
                    return True
                else:
                    self.catan.gui.set_msg( ret )
                    return False
        else:
            self.catan.gui.set_msg( "pave: Invalid number of arguments.  Expected 1, got %d." % (len(args)-1) )

    def c_setname(self, args):
        if len(args) == 2:
            old = self.catan.currentPlayer.name
            new = args[1][:8]
            color = self.catan.currentPlayer.color
            self.catan.currentPlayer.name = new
            self.catan.gui.set_msg( "setname: Changed name %s%s&& to %s%s&&." % (color, old, color, new) )
            return True
        else:
            self.catan.gui.set_msg( "setname: Invalid number of arguments.  Expected 1 got %d." % (len(args)-1) )

    def c_setcpuname(self, args):
        if len(args) == 3:
            p = self.catan.get_player_by_id( int(args[1])-1 )
            if p != False:
                if isinstance( p, CPU ):
                    old = p.name
                    new = args[2][:8]
                    color = p.color
                    p.name = new
                    self.catan.gui.set_msg( "setcpuname: Changed name %s%s&& to %s%s&&." % (color, old, color, new) )
                    return True
                else:
                    self.catan.gui.set_msg( "setcpuname: Invalid player id number.  Cannot change name of Human player." )
            else:
                self.catan.gui.set_msg( "setcpuname: Invalid player id number.")
        else:
            self.catan.gui.set_msg( "setcpuname: Invalid number of arguments.  Expected 2 got %d." % (len(args)-1) )

    def c_build(self, args):
        self.catan.gui.set_msg( 'build' )
        return True

    def c_flip(self, args):
        self.catan.gui.set_msg( 'flip' )
        return True

    def c_pass(self, args):
        self.catan.hasPassed = True
        self.catan.gui.set_msg( 'pass' )
        return True

class Catan(object):
    def __init__(self, numHumans, numCPUs):
        self.settings = Settings( STYLE, numHumans, numCPUs )
        self.options = Options( self )
        self.gui = gui.GUI( self )
        self.history = []
        self.reseed()

        self.loop()

    def loadGame(self, path):
        if os.path.isdir( path ):
            # retrieve hidden game data
            if os.path.exists( path+'hidden.json' ):
                with open( path + 'hidden.json', 'r' ) as f:
                    hiddenData = json.load( f )
            else:
                return '%s: Error retrieving hidden data. File missing or corrupted.' % path

            # retrieve public game data
            if os.path.exists( path+'public.json' ):
                with open( path + 'public.json', 'r' ) as f:
                    publicData = json.load( f )
            else:
                return '%s: Error retrieving public data. File missing or corrupted.' % path

            # retrieve private game data
            if os.path.exists( path+'private.json' ):
                with open( path + 'private.json', 'r' ) as f:
                    privateData = json.load( f )
            else:
                return '%s: Error retrieving private data. File missing or corrupted.' % path

            # overwrite stuff from the constructor
            self.settings = Settings( publicData['style'], publicData['numHumans'], publicData['numCPUs'], publicData['savepath'] )
            self.options = Options( self )
            self.gui = gui.GUI( self )
            self.history = publicData['history']
            self.reseed()

            # build hidden data
            self.dcDeck = [ self.devCards[dc] for dc in hiddenData['dcDeck'] ]

            # build public data
            self.savepath = publicData['savepath']
            self.turn = publicData['turn']
            self.isFirstTurn = publicData['isFirstTurn']
            self.players = [ self.get_player_by_id(p) for p in publicData['playerOrder'] ]
            self.currentPlayer = self.get_player_by_id( publicData['currentPlayer'] )
            self.hasLargestArmy = self.get_player_by_id( publicData['hasLargestArmy'] )
            self.hasLongestRoad = self.get_player_by_id( publicData['hasLongestRoad'] )
            self.dice.load( publicData['dice'] )
            for p in self.players:
                p.load( 'public', publicData['players'][str(p.num)], self )
            for h in publicData['hexes']:
                self.hexes[h['num']].load( 'public', h, self )
            for n in publicData['nodes']:
                self.nodes[n['num']].load( 'public', n, self )
            for r in publicData['roads']:
                self.roads[r['num']].load( 'public', r, self )
            for c in publicData['conns']:
                self.conns[c['num']].load( 'public', c, self )

            # build private data
            for p in self.players:
                p.load( 'private', privateData[str(p.num)], self )

            # enter the game at the last checkpoint
            self.loop( self.turn-1 )

            return True

        else:
            return '%s: Error retrieving save files.  Files missing or corrupted.' % path

    def saveGame(self):
        # get filepath
        path = self.settings.get('savepath')
        with open( '%sdata.txt' % path, 'w' ) as f:
            f.write( 'humans:%d, CPUs:%d, turn:%d, modified:%s' % (self.settings.get('numHumans'), self.settings.get('numCPUs'), self.turn, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") ) )
        path = '%sturn_%d/' % ( path, self.turn )
        if os.path.exists( path ) == False:
            os.mkdir( path )
        print path

        # save hidden game
        kw = 'hidden'
        data = { 'dcDeck': [ dc.name for dc in self.dcDeck ] }
        with open( path + kw + '.json', 'w' ) as f:
            json.dump( data, f, indent=4 )

        # save public game
        kw = 'public'
        data = {}
        data['style'] = STYLE
        data['savepath'] = self.settings.get('savepath')
        data['numHumans'] = self.settings.get('numHumans')
        data['numCPUs'] = self.settings.get('numCPUs')
        data['history'] = self.history
        data['turn'] = self.turn
        data['isFirstTurn'] = self.isFirstTurn
        data['playerOrder'] = [ p.num for p in self.players ]
        data['currentPlayer'] = self.currentPlayer.num
        data['hasLargestArmy'] = self.hasLargestArmy.num
        data['hasLongestRoad'] = self.hasLongestRoad.num
        data['dice'] = self.dice.save( kw )
        data['players'] = {}
        for p in self.players:
            data['players'][p.num] = p.save( kw )
        data['hexes'] = [ h.save(kw) for h in self.hexes ]
        data['nodes'] = [ n.save(kw) for n in self.nodes ]
        data['roads'] = [ r.save(kw) for r in self.roads ]
        data['conns'] = [ c.save(kw) for c in self.conns ]
        with open( path + kw + '.json', 'w' ) as f:
            json.dump( data, f, indent=4 )

        # save private games
        kw = 'private'
        data = {}
        for p in self.players:
            data[p.num] = p.save( kw )
        with open( path + kw + '.json', 'w' ) as f:
            json.dump( data, f, indent=4 )

    def reseed(self):
        self.nonePlayer = Player(-1, self)
        self.nonePlayer.color = "&hb&bt"
        self.nonePlayer.name = "NONE"
        self.nonePlayer.isNonePlayer = True

        self.generate_board()
        self.generate_players()

    def generate_board(self):
        self.dice = Dice()

        self.hexes = []
        self.nodes = []
        self.roads = []
        self.conns = []

        self.resources = {}
        self.devCards = {}
        self.dcDeck = []

        # make the Dev Cards
        for key in self.settings.get('devCards').keys():
            dc = self.settings.get('devCards')[key]
            for num in range( dc['num'] ):
                devCard = DevCard( dc )
                self.devCards[key] = devCard
                self.dcDeck.append( devCard )
                random.shuffle( self.dcDeck )

        # make the Hexes and Resources
        diceValues = self.settings.get('diceValues')[:]
        random.shuffle( diceValues )
        resources = []
        for key in self.settings.get('resources').keys():
            for num in range( self.settings.get('resources')[key]['num'] ):
                resources.append( key )
        random.shuffle(resources)
        for i in range(19):
            resource = resources.pop()
            resource = self.settings.get('resources')[resource]
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
        self.players = []
        self.currentPlayer = self.nonePlayer
        self.hasLargestArmy = self.nonePlayer
        self.hasLongestRoad = self.nonePlayer

        self.players  = [ Human(i, self) for i in range(self.settings.get('numHumans')) ]
        self.players += [ CPU(self.settings.get('numHumans') + i, self) for i in range(self.settings.get('numCPUs'))]
        random.shuffle(self.players)

    def take_turn(self):
        if self.turn < 2 * len(self.players):
            if self.turn == 0:
                self.firstTwoTurnsQueue = [ p for p in self.players ] + [ p for p in self.players[::-1] ]
                self.isFirstTurn = True

            self.currentPlayer = self.firstTwoTurnsQueue[ self.turn ]
            self.turn += 1
            self.currentPlayer.settle()

            if self.turn > len(self.players): # each player's second turn collect resources
                s = self.currentPlayer.settlements[-1]
                for conn in s.conns:
                    r = conn.vertices[1].resource.resource
                    self.currentPlayer.harvest(r)

            if self.turn == 2 * len(self.players):
                self.isFirstTurn = False

        else:
            self.currentPlayer = self.players[ self.turn % len(self.players) ]
            self.turn += 1
            self.hasRolled = False
            self.hasPlayedDC = False
            self.hasPassed = False

            self.currentPlayer.take_turn()

    def loop(self, turn=0):
        self.turn = turn
        while self.is_game_over() == False:
            self.take_turn()
            self.saveGame()
        print "%s wins!" % player.name

    def roll(self):
        diceValue = self.dice.roll()
        if diceValue in {8,11}:
            self.gui.add_pMsg( "%s - %s rolled an %d" % (self.currentPlayer.color, self.currentPlayer.name, diceValue) )
        else:
            self.gui.add_pMsg( "%s - %s rolled a %d" % (self.currentPlayer.color, self.currentPlayer.name, diceValue) )

        if diceValue == 7:
            for p in self.players:
                if p.total('res') > 7:
                    p.discard()
            self.currentPlayer.move_robber()
        else:
            for h in self.hexes:
                if h.diceValue == diceValue and h.isBlocked == False:
                    for n in h.get_adj_nodes():
                        n.owner.harvest( h.resource.resource )

    def isAuthenticated(self, opt):
        return DEBUG or opt not in self.options.dump( 'admin' ) or not( self.currentPlayer.isAdmin )

    def handle_input(self):
        self.gui.render()

        args = self.gui.prompt().split(' ')
        cmd = args[0]
        self.history.append( { 'pid':self.currentPlayer.num, 'turn':self.turn, 'command':args } ) # add history to CPUs

        if cmd in self.options.dump():
            if cmd in self.options.dump( 'available' ) or cmd in self.options.dump( 'persistent' ):
                if self.isAuthenticated( cmd ):
                    command = self.options.get( cmd )
                    ret = command.do( args )
                    if ret == True and cmd in self.options.dump( 'available' ):
                        return True
                else:
                    self.gui.set_msg( "%s: Could not execute because developer commands are disabled for this session." % cmd )
            else:
                msg = u'%s: Could not execute.\n  &gCurrently available commands:&&\n' % cmd
                for opt in self.options.dump( 'available' ):
                    if self.isAuthenticated( opt ):
                        msg += opt + ", "
                msg += u'\n  &gAlways available commands:&&\n'
                for opt in self.options.dump( 'persistent' ):
                    if self.isAuthenticated( opt ):
                        msg += opt + ", "
                msg += "&&"
                self.gui.set_msg( msg )
        else:
            self.gui.set_msg( '%s: Unrecognized command.  For a list of commands, type "help".' % cmd )

        self.handle_input()

    def is_game_over(self):
        for player in self.players:
            return player.privateScore >= self.settings.get('victoryPointsGoal')

    def check_longest_road(self):
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
                currentHolder.publicScore += 2
                currentHolder.privateScore += 2
                if self.hasLongestRoad != None:
                    self.hasLongestRoad.hasLongestRoad = False
                    self.hasLongestRoad.publicScore -= 2
                    self.hasLongestRoad.privateScore -= 2
                self.hasLongestRoad = currentHolder
        self.is_game_over()

    def get_player_by_id(self, i):
        for p in self.players:
            if p.num == i:
                return p
        return self.nonePlayer

    def lookup(self, coord, look=None):
        h_index = self.settings.get("h_index")
        n_index = self.settings.get("n_index")
        r_index = self.settings.get("r_index")

        lists = {
            'hexes' : h_index,
            'nodes' : n_index,
            'roads' : r_index}
        ret = False

        if look != None and look in lists:
            for item in lists[look].keys():
                if coord == lists[look][item]:
                    return item
        else:
            coord = coord.lower()

            if coord in h_index:
                ret = self.hexes[h_index[coord]]
            elif coord in n_index:
                ret = self.nodes[n_index[coord]]
            elif coord in r_index:
                ret = self.roads[r_index[coord]]

        return ret

class Player(object):
    def __init__(self, num, catan):
        self.num = num
        self.publicScore = 0
        self.privateScore = 0
        self.resCards = { 'wheat':0, 'sheep':0, 'brick':0, 'wood':0, 'ore':0 } # resource cards
        self.devCardsU = { 'vp':0, 'knight':0, 'yop':0, 'monopoly':0, 'rb':0 } # played
        self.devCardsP = { 'vp':0, 'knight':0, 'yop':0, 'monopoly':0, 'rb':0 } # unplayed
        self.numKnights = 0
        self.hasLargestArmy = False
        self.name = ''
        self.isHuman = False
        self.catan = catan
        self.settlements = []
        self.roads = []
        self.longestRoad = 0
        self.hasLongestRoad = False
        if num < 0:
            self.isNonePlayer = True
            self.color = u'&&'
            self.bcolor = u'&&'
        else:
            self.isNonePlayer = False
            self.color = u'&p%dt' % num
            self.bcolor = u'&p%db' % num

    def save(self, keyword):
        if keyword == 'public':
            d = {
                'num': self.num,
                'devCardsP': self.devCardsP,
                'numKnights': self.numKnights,
                'hasLargestArmy': self.hasLargestArmy,
                'name': self.name,
                'isHuman': self.isHuman,
                'settlements': [ s.num for s in self.settlements ],
                'roads': [ r.num for r in self.roads ],
                'hasLongestRoad': self.hasLongestRoad,
                'color': self.color,
                'bcolor': self.bcolor }
        elif keyword == 'private':
            d = {
                'resCards': self.resCards,
                'devCardsU': self.devCardsU}
        return d

    def load(self, keyword, data, catan):
        if keyword == 'public':
            self.isNonePlayer = False
            self.catan = catan

            self.devCardsP = data['devCardsP']
            self.numKnights = data['numKnights']
            self.hasLargestArmy = data['hasLargestArmy']
            self.name = data['name']
            self.isHuman = data['isHuman']
            self.settlements = [ catan.nodes[num] for num in data['settlements'] ]
            self.roads = [ catan.roads[num] for num in data['roads'] ]
            self.hasLongestRoad = data['hasLongestRoad']
            self.color = data['color']
            self.bcolor = data['bcolor']

            self.publicScore = 0
            for s in self.settlements:
                self.publicScore += 1
                if s.isCity:
                    self.publicScore += 1
            if self.hasLargestArmy:
                self.publicScore += 2
            if self.hasLongestRoad:
                self.publicScore += 2
            self.privateScore = self.publicScore

        elif keyword == 'private':
            self.resCards = data['resCards']
            self.devCardsU = data['devCardsU']

            for dc in self.devCardsU:
                if dc == 'vp':
                    self.privateScore += 1

    def harvest(self, resource):
        if resource in self.resCards and self.isNonePlayer == False:
            self.resCards[resource] += 1
        else:
            return False

    def print_line(self):
        score = self.publicScore
        if self == self.catan.currentPlayer:
            score = self.privateScore
        return "%s %-8s %2d  %2d  %2d   %2d  &&" % (self.color, self.name, score, self.total('res'), self.total('dcu'), self.numKnights)

    def total(self, datatype):
        acc = 0
        data = { 'res':self.resCards, 'dcu':self.devCardsU }[datatype]
        for key in data.keys():
            acc += data[key]
        return acc

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
        self.catan.check_longest_road()

    def add_settlement(self, node):
        self.publicScore += 1
        self.privateScore += 1
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

        self.catan.gui.add_pMsg( u"%schoose a settlement (settle opts)&&" % self.color)
        self.catan.options.set( {'settle'} )
        self.catan.handle_input()
        self.catan.gui.remove_pMsg()

        if self.catan.isFirstTurn:

            self.catan.gui.add_pMsg( u"%schoose a road (pave opts)&&" % self.color )
            self.catan.options.set( {'pave'} )
            self.catan.handle_input()
            self.catan.gui.remove_pMsg()

    def discard(self):
        pass

    def move_robber(self):
        pass

    def take_turn(self):
        self.catan.gui.add_pMsg( u"%sroll or flip a development card (roll, flip opts)" % self.color )
        while self.catan.hasPassed == False:
            self.catan.options.set( {'flip'} ) # always able to play VP but not necessarily other cards
            if self.catan.hasRolled:
                self.catan.gui.add_pMsg( u"%sbuild, flip a development card, or pass (build, flip opts, pass)" % self.color)
                self.catan.options.add( 'build' )
                self.catan.options.add( 'pass' )
            else:
                self.catan.options.add( 'roll' )
            self.catan.handle_input()

        self.catan.gui.remove_pMsg( 'all' )

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
                    thisTotal += self.catan.settings.get("hex_dots")[str(adj_hex.diceValue)]
                if thisTotal > bestTotal:
                    bestNode = node
                    bestTotal = thisTotal
        bestNode.settle(self)

        if self.catan.isFirstTurn:
            self.pave(bestNode)

    def discard(self):
        old = self.total('res')
        new = self.total('res')
        while old - new < int(old/2):
            key = random.choice( self.resCards.keys() )
            if self.resCards[key] > 0:
                self.resCards[key] -= 1
            new = self.total('res')

        self.catan.gui.add_pMsg( '   %s%s discarded %d cards' % (self.color, self.name, old-new) )

    def move_robber(self):
        pass

    def pave(self, restrict=None):
        if self.catan.isFirstTurn:
            r = random.choice(self.settlements[-1].roads)
            r.pave(self)

    def take_turn(self):
        self.catan.roll()

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

    def save(self, keyword):
        if keyword == 'public':
            d = {
                'num': self.num,
                'resource': self.resource.resource,
                'diceValue': self.diceValue,
                'isOcean': self.isOcean,
                'isBlocked': self.isBlocked,
                'conns': [ c.num for c in self.conns ]}
        return d

    def load(self, keyword, data, catan):
        if keyword == 'public':
            self.resource = catan.resources[ data['resource'] ]
            self.color = self.resource.bkg
            self.diceValue = data['diceValue']
            self.isOcean = data['isOcean']
            self.isBlocked = data['isBlocked']
            self.conns = [ catan.conns[num] for num in data['conns'] ]

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

    def show_info(self, catan, coord=''):
        s = u"%s = { type: HEX, coord: %s, resource: %s%s&&" % ( coord, catan.lookup(self.num, 'hexes'), self.resource.text, self.resource.name )
        s += ", diceroll: %s%d&&, is-blocked: &hb&bt" % ( self.resource.text, self.diceValue)
        if self.isBlocked:
            s += "YES"
        else:
            s += "NO"
        s += "&& }"
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

    def save(self, keyword):
        if keyword == 'public':
            d = {
                'num': self.num,
                'owner': self.owner.num,
                'isCity': self.isCity,
                'isSettleable': self.isSettleable,
                'roads': [ r.num for r in self.roads ],
                'conns': [ c.num for c in self.conns ]}
        return d

    def load(self, keyword, data, catan):
        self.owner = catan.get_player_by_id( data['owner'] )
        self.isCity = data['isCity']
        self.isSettleable = data['isSettleable']
        self.roads = [ catan.roads[num] for num in data['roads'] ]
        self.conns = [ catan.conns[num] for num in data['conns'] ]

    def escape(self, shape=''):
        s = self.owner.bcolor
        if self.owner.isNonePlayer:
            s += u' . '
        elif self.isCity:
            s += u' C '
        else:
            s += u' s '
        return s

    def show_info(self, catan, coord=''):
        s = u"%s = { type: NODE, coord: %s, owner: %s%s&&, is-city: &hb&bt" % ( coord, catan.lookup(self.num, 'nodes'), self.owner.color, self.owner.name )
        if self.isCity:
            s += "YES"
        else:
            s += "NO"
        s += "&&, is-settleable: &hb&bt"
        if self.isSettleable:
            s += "YES"
        else:
            s += "NO"
        s += "&& }"
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

        return "settle: Error not settleable."

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

    def save(self, keyword):
        if keyword == 'public':
            d = {
                'num': self.num,
                'vertices': (self.vertices[0].num, self.vertices[1].num),
                'owner': self.owner.num }
        return d

    def load(self, keyword, data, catan):
        self.owner = catan.get_player_by_id( data['owner'] )
        self.set_vertices( catan.nodes[ data['vertices'][1] ], catan.nodes[ data['vertices'][1] ] )

    def pave(self, player, save=True):
        if self.owner.isNonePlayer:
            if player.catan.isFirstTurn:
                if self in player.settlements[-1].roads: # check if adjacent to most recently placed settlement
                    if save:
                        self.owner = player
                        player.add_road(self)
                    return True
                else:
                    return "pave: Error need to pave a road adjacent to most recent settlement."
            else:
                for r in player.roads:
                    if self.calc_distance(r) <= 1: # check if adjacent to any other built roads
                        if save:
                            self.owner = player
                            player.add_road(self)
                        return True
                    return "pave: Error road needs to be adjacent to existing road or settlement."
        else:
            return "pave: Error road already paved by %s%s&&." % ( self.owner.color, self.owner.name )

    def escape(self, shape):
        s = self.owner.bcolor
        if shape == 'Rs':
            s += u' / '
        elif shape == 'Rb':
            s += u' \\ '
        elif shape == 'Rv':
            s += u' | '
        return s

    def show_info(self, catan, coord=''):
        s = u"%s = { type: ROAD, coord: %s, owner: %s%s&& }" % ( coord, catan.lookup(self.num, 'roads'), self.owner.color, self.owner.name )
        return s

class Connection(Edge):
    def __init__(self, num):
        Edge.__init__(self, num)

    def __repr__(self):
        return "<n:%d, h:%d>" % (self.vertices[0].num, self.vertices[1].num)

    def save(self, keyword):
        if keyword == 'public':
            d = {
                'num': self.num,
                'vertices': (self.vertices[0].num, self.vertices[1].num)}
        return d

    def load(self, keyword, data, catan):
        self.set_vertices( catan.nodes[ data['vertices'][0] ], catan.hexes[ data['vertices'][1] ] )

def main():
    catan = Catan(1,2)
    return 0

if __name__ == "__main__":
    main()
