from graphics import *
from math import atan, cos, sin, sqrt
from random import randint, shuffle

class GUI(object):
    def __init__(self, graph, harbors):
        self.bgcolor = color_rgb(60, 130, 230)
        self.edge_size = 45
        self.resource_colors = {
            "desert" : color_rgb(230,230,230),
            "ore"    : color_rgb(50,50,60),
            "brick"  : color_rgb(220,120,60),
            "wool"   : color_rgb(140,210,40),
            "grain"  : color_rgb(255,210,0),
            "lumber" : color_rgb(40,120,30),
            "mystery": color_rgb(255,255,255) }
        self.player_colors = {
            0 : color_rgb(255,20,0),    # Red
            1 : color_rgb(0,10,255),    # Blue
            2 : color_rgb(35,140,35),   # Green
            3 : color_rgb(170,100,40) } # Brown

        self.win = GraphWin("Catan", 640, 480)
        self.center = Point(320,240)
        self.win.setBackground(self.bgcolor)

        shuffle(harbors)

        for vert in graph.verts:
            x = self.format_x(vert.x)
            y = self.format_y(vert.y)
            color = color_rgb(255,255,255)
            vert.obj = Pt(x,y,color)
            #vert.obj.draw(self.win)

        for edge in graph.edges:
            if edge.v1.harbor and edge.v2.harbor:
                resource = harbors.pop()
                color = self.resource_colors[resource]
                port = Port(edge.v1,edge.v2,self.edge_size,color)
                port.draw(self.win)
                edge.v1.harbor = resource
                edge.v2.harbor = resource

        for tile in graph.tiles:
            x = self.format_x(tile.x)
            y = self.format_y(tile.y)
            color = self.resource_colors[tile.resource]
            diceroll = tile.diceroll
            tile.obj = Hexagon(x,y,self.edge_size,color,diceroll)
            tile.obj.draw(self.win)

        for edge in graph.edges:
            p1 = edge.v1.obj.point.clone()
            p2 = edge.v2.obj.point.clone()
            color = color_rgb(255,255,255)
            edge.obj = Road(p1,p2,color)
            edge.obj.draw(self.win)

        self.robber = Robber()

    def moveRobber(self,tile):
        x = tile.obj.x
        y = tile.obj.y
        self.robber.move(x,y,self.edge_size,self.win)

    def changecolor(self,thing):  ### TEMP FXN to test robustness
        thing.obj.object.setFill(randomColor())

    def clickObj(self,click,graph,ret):
        this = None
        dist = self.edge_size

        x = click.getX()
        y = click.getY()

        if ret == "r" or ret == "e":
            it = graph.edges
        elif ret == "t" or ret == "h":
            it = graph.tiles
        elif ret == "v" or ret == "n":
            it = graph.verts

        for i in it:
            d = sqrt((i.obj.x-x)**2 + (i.obj.y-y)**2)
            if d < dist:
                this = i
                dist = d

        return this

    def pause(self):
        click = self.win.getMouse()
        self.win.close()

    def format_x(self, x):
        x = self.center.getX() + sqrt(3)/2 * self.edge_size * (x-5)
        return x

    def format_y(self, y):
        y = self.center.getY() + 1.0/2 * self.edge_size * (y-8)
        return y

class Robber(object):
    def __init__(self):
        self.object = Point(0,0)

    def move(self,x,y,len,win):
        self.undraw()
        self.object = Circle(Point(x,y),12)

        self.object.setOutline(color_rgb(0,0,0))
        self.object.setWidth(5)
        self.draw(win)

    def draw(self,win):
        self.object.draw(win)

    def undraw(self):
        self.object.undraw()


class Hexagon(object):
    def __init__(self, x, y, len, color, diceroll):
        self.x = x
        self.y = y

        self.object = Polygon(
            Point(x - sqrt(3)/2 * len, y - 1.0/2 * len),
            Point(x - sqrt(3)/2 * len, y + 1.0/2 * len),
            Point(x, y + len),
            Point(x + sqrt(3)/2 * len, y + 1.0/2 * len),
            Point(x + sqrt(3)/2 * len, y - 1.0/2 * len),
            Point(x, y - len))
        self.object.setFill(color)
        self.object.setWidth(0)

        if diceroll:
            text = str(diceroll)
        else:
            text = ''

        self.textobject = Text(Point(x,y), text)

    def draw(self, win):
        self.object.draw(win)
        self.textobject.draw(win)

    def undraw(self):
        self.object.undraw()
        self.textobject.undraw()

class Port(object):
    def __init__(self, v1, v2, len, color):
        x1 = v1.obj.x
        x2 = v2.obj.x
        dx = x2-x1+0.000001 # Protect against division by 0
        xbar = x1 + dx/2

        y1 = v1.obj.y
        y2 = v2.obj.y
        dy = y2-y1+0.000001
        ybar = y1 + dy/2

        theta = atan(dy/dx)
        xadj = sin(theta) * len * 0.2
        yadj = cos(theta) * len * 0.2

        self.object = Polygon(
            v1.obj.point.clone(),
            Point(xbar - xadj, ybar + yadj),
            v2.obj.point.clone(),
            Point(xbar + xadj, ybar - yadj) )
        self.object.setFill(color)
        self.object.setOutline(color)

    def draw(self,win):
        self.object.draw(win)

    def undraw(self):
        self.undraw()

class Pt(object):
    def __init__(self,x,y,color):
        self.x = x
        self.y = y

        self.point = Point(x,y)
        self.object = Circle(self.point,6)
        self.object.setFill(color)
        self.object.setWidth(0)

    def draw(self, win):
        self.object.draw(win)

    def undraw(self):
        self.object.undraw()


class Road(object):
    def __init__(self,p1,p2,color):
        self.x = (p1.getX() + p2.getX())/2
        self.y = (p1.getY() + p2.getY())/2

        self.object = Line(p1,p2)
        self.object.setOutline(color)
        self.object.setWidth(3)

    def draw(self, win):
        self.object.draw(win)

    def undraw(self):
        self.object.undraw()

class Settlement(object):
    def __init__(self):
        pass

class City(object):
    def __init__(self):
        pass

def randomColor():
    return color_rgb(randint(0,255),randint(0,255),randint(0,255))
