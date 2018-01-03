import os

class GUI(object):
    def __init__(self, catan, view='wide'):

        self.catan = catan
        self.settings = self.catan.settings
        self.view = self.settings.get(view)
        self.colors = self.settings.get('colors')

        self.pMsgs = [] # persistent messages
        self.msg = None

        self.gameText = None
        self.gameEscs = None

        self.infoText = None
        self.infoEscs = None

    def set_msg(self, msg):
        self.msg = msg

    def add_pMsg(self, pMsg):
        self.pMsgs.append(pMsg)

    def remove_pMsg(self, pMsg=None):
        if pMsg == None:
            self.pMsgs.pop()
        elif pMsg in self.pMsgs:
            self.pMsgs.remove( pMsg )
        else:
            return False

    def escape(self, s):
        for code in self.colors.keys():
            s = s.replace(code, self.colors[code])
        return s

    def join_screens(self, left, right, lWidth, offset=0, pad=True):
        if pad:
            lpad = ' '*self.view['lpad']
            mpad = ' '*self.view['mpad']
            rpad = ' '*self.view['rpad']
        else:
            lpad = ''
            mpad = ''
            rpad = ''

        lOff = -1*offset if offset<0 else 0
        rOff = offset if offset>0 else 0

        lText = [ ' '*lWidth for i in range(lOff) ] + left + [ ' '*lWidth for i in range( len(left)+lOff, len(right)+rOff )]
        rText = [ '' for i in range(rOff) ] + right +  [ ' ' for i in range( len(right)+rOff, len(left)+lOff) ]
        join = [ lpad + lText[i] + mpad + rText[i] + rpad for i in range(len( lText )) ]

        return join

    def render(self, screen='all'):
        if screen == 'all':
            screen = []

            for row in self.view['order']:
                if 'prompt' not in row:
                    left = self.render( row[0] )
                    for col in row[1:]:
                        right = self.render( col[0] )
                        lWidth = col[1]
                        offset = col[2]
                        left = self.join_screens( left, right, lWidth, offset )
                    screen += left

            self.out( screen )

        elif screen == 'tbanner':
            return [ self.view['tbanner'] ]

        elif screen == 'game':
            chunk = []

            if self.gameText == None or self.gameEscs == None:
                genc = self.view['genc'].split("\n")

                gameText = []
                gameEscs = [ [] for line in genc ]

                counts = { 'Nd':0, 'Rd':0, 'Ht':0, 'Hf':0, 'Hg':0, 'Hx':0, 'Hb':0 }

                for l in range(len(genc)):
                    line = genc[l]
                    tline = u""
                    for i in range(0,len(line),2):

                        if line[i] == ' ': # empty space
                            tline += " "

                        elif line[i] == 'O': # ocean tile
                            tline += "&~"
                            for n in range( int(line[i+1],16) ):
                                tline += "~"

                        elif line[i] == 'N':
                            tline += "%s"
                            gameEscs[l].append(('n', counts[ line[i:i+2] ]))
                            counts[ line[i:i+2] ] += 1

                        elif line[i] == 'R':
                            tline += "%s"
                            gameEscs[l].append((line[i:i+2], counts[ 'Rd' ]))
                            counts[ 'Rd' ] += 1

                        elif line[i] == 'H':
                            tline += "%s"
                            if line[i+1] == 'x':
                                gameEscs[l].append(('Hx', counts[ 'Hx' ]))
                            elif line[i+1] == 't' or line[i+1] == 'b':
                                gameEscs[l].append(('Hf', counts[ line[i:i+2] ]))
                            else:
                                gameEscs[l].append(('HF', counts[ line[i:i+2] ]))
                            counts[ line[i:i+2] ] += 1

                        else:
                            return False
                    gameText.append(tline)

                self.gameText = gameText
                self.gameEscs = gameEscs

            args = []

            for line in self.gameEscs:
                argLine = []
                for item in line:
                    if item[0][0] == 'n':
                        argLine.append( self.catan.nodes[ item[1] ].escape() )
                    elif item[0][0] == 'R':
                        argLine.append( self.catan.roads[ item[1] ].escape( item[0] ))
                    elif item[0][0] == 'H':
                        argLine.append( self.catan.hexes[ item[1] ].escape( item[0] ))
                args.append(argLine)

            # escape everything and add the letters and numbers on the border
            if self.view['border']:
                for l in range(len(self.gameText)):
                    chunk.append( ('&g' + chr(65+l) + self.gameText[l] + '&g' + chr(65+l)) % tuple(args[l]) )
                tens = '&g  '
                ones = '&g  '
                for i in range(41):
                    tens += str( int(i/10) ) if i%10==0 else ' '
                    ones += str(i%10)
                tens += '  '
                ones += '  '
                chunk = [tens, ones] + chunk + [ones, tens]

            return chunk

        elif screen == 'info':
            chunk = []

            if self.infoText == None or self.infoEscs == None:
                ienc = self.view['ienc'].split("\n")

                infoText = []
                infoEscs = []

                for l in range(len(ienc)):
                    line = ienc[l]
                    tline = ""
                    eline = []
                    scanning = True
                    useThis = True

                    for i in range(0,len(line),2):
                        if scanning:

                            if line[i] == 's':
                                if line[i+1] == '=':
                                    tline += line[i+2:]
                                    scanning = False
                                else:
                                    tline += " "*int(line[i+1],16)

                            elif line[i] == 'T':
                                if line[i+1] == 'a':
                                    tline += "&&       ._. ._."
                                elif line[i+1] == 'b':
                                    tline += "&&Turn:  |%d| |%d|"
                                    eline += [('T',0), ('T',1)]

                            elif line[i] == 'I':
                                tline += '&&'
                                if line[i+1] == 't':
                                    tline += '.___________________________.'
                                elif line[i+1] == 'm':
                                    for p in range(len(self.catan.players)):
                                        infoText.append( '&&|%s|' )
                                        infoEscs.append( [('P',p)] )
                                    useThis = False
                                elif line[i+1] == 'b':
                                    tline += '|___________________________|'

                            elif line[i] == 'D':
                                if line[i+1] == 'a':
                                    tline += "&&       ._. ._."
                                elif line[i+1] == 'b':
                                    tline += "&&Dice:  |%d| |%d|"
                                    eline += [('D',0), ('D',1)]

                            elif line[i] == 'R':
                                tline += '%s'
                                eline += [('P','c')]
                                if line[i+1] == 't':
                                    tline += '.___________________________.'
                                elif line[i+1] == 'm':
                                    for r in [ 'wheat', 'sheep', 'brick', 'wood', 'ore' ]:
                                        infoText.append( '%s| %s%-5s               %s    %s|' )
                                        infoEscs.append( [('P','c'),('R',r,'color'),('R',r,'n'),('R',r,'c'),('P','c')] )
                                    useThis = False
                                elif line[i+1] == 'b':
                                    tline += '|___________________________|'

                            elif line[i] == 'V':
                                tline += '%s'
                                eline += [('P','c')]
                                if line[i+1] == 'm':
                                    for v in [ 'vp', 'knight', 'yop', 'monopoly', 'rb' ]:
                                        infoText.append( '%s| %s%-13s  %s   %s    %s|' )
                                        infoEscs.append( [('P','c'),('V',v,'color'),('V',v,'n'),('V',v,'u'),('V',v,'d'),('P','c')] )
                                    useThis = False
                                elif line[i+1] == 'b':
                                    tline += '|___________________________|'

                    if useThis:
                        infoText.append(tline)
                        infoEscs.append(eline)

                self.infoText = infoText
                self.infoEscs = infoEscs

            args = []

            for line in self.infoEscs:
                argLine = []
                for item in line:
                    if item[0] == 'T':
                        if item[1]==0:
                            argLine.append( int(self.catan.turn/10) )
                        else:
                             argLine.append( self.catan.turn%10 )
                    elif item[0] == 'D':
                        argLine.append( self.catan.dice.view( item[1] ))
                    elif item[0] == 'P':
                        if item[1] == 'c':
                            argLine.append( self.catan.currentPlayer.color )
                        else:
                            argLine.append( self.catan.players[ item[1] ].print_line() )
                    elif item[0] == 'R':
                        resource = self.catan.resources[ item[1] ]
                        if item[2] == 'color':
                            argLine.append( resource.text )
                        if item[2] == 'n':
                            argLine.append( resource.name )
                        elif item[2] == 'c':
                            argLine.append( self.catan.currentPlayer.count( resource.resource ))
                    elif item[0] == 'V':
                        devCard = self.catan.devCards[ item[1] ]
                        if item[2] == 'color':
                            argLine.append( devCard.text )
                        if item[2] == 'n':
                            argLine.append( devCard.plural )
                        elif item[2] == 'u':
                            argLine.append( self.catan.currentPlayer.count( devCard.name, 'up' ))
                        elif item[2] == 'd':
                            argLine.append( self.catan.currentPlayer.count( devCard.name, 'down' ))
                    else:
                        argLine.append( item )

                args.append(argLine)

            for l in range(len(self.infoText)):
                chunk.append( self.infoText[l] % tuple(args[l]) )

            return chunk

        elif screen == 'lbanner':
            return [ self.view['lbanner'] ]

        elif screen == 'pMsgs':
            return [ "%s&&" % pMsg for pMsg in self.pMsgs]

        elif screen == 'msg':
            if self.msg == None:
                return []
            else:
                return [ self.msg ]

        else:
            return False

    def prompt(self, prompt=None, color='&&'):
        if prompt == None:
            prompt = self.settings.get('prompt')
        prompt = self.escape( color + prompt + ' ' )
        return raw_input(prompt)

    def out(self, screen, clear=True, singleLine=False):
        if clear:
            os.system('cls' if os.name == 'nt' else 'clear')
        if singleLine:
            print self.escape(screen + '&&')
        else:
            for line in screen:
                print self.escape(line + '&&')
