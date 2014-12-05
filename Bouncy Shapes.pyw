from graphics import *
from time import sleep
from random import randrange
from _thread import start_new_thread
from math import sqrt

class Shape():
    def __init__(self,name,window):
        self.name = name
        self.window = window

    def drw(self):
        if self.name == "circle":
            self.s = Circle(Point(200,350),30)
            self.s.setFill("red")
            self.s.setOutline("red")
        else:
            self.s = Rectangle(Point(170,320),Point(230,380))
            self.s.setFill("blue")
            self.s.setOutline("blue")

        self.s.draw(self.window)

    def jump(self,shape,hurdle,score,scoreText,bestScore,bscoreText):
        x = 0
        for i in range(33):
            sleep(0.01)
            if checkCrash(shape,hurdle) == True: break
            x -= 1
            self.s.move(0,20 / x)

        x = 0
        for j in range(40):
            sleep(0.01)
            if checkCrash(shape,hurdle) == True: break
            x += 1
            self.s.move(0,x / 10)

        if checkCrash(shape,hurdle) != True:
            self.s.undraw()
            self.drw()
            score[0] += 1
            scoreText.pop().undraw()
            scoreText.append(Text(Point(150,50),"Score: %d" %score[0]))
            scoreText[0].setOutline("red")
            scoreText[0].setSize(18)
            scoreText[0].draw(self.window)
            if score[0] > bestScore[0]:
                bestScore[0] = score[0]
                bscoreText.pop().undraw()
                bscoreText.append(Text(Point(300,50),"Best Score: %d" %bestScore[0]))
                bscoreText[0].setOutline("red")
                bscoreText[0].setSize(18)
                bscoreText[0].draw(self.window)

class Hurdle:
    def __init__(self,window):
        self.win = window

    def drw(self):
        r = randrange(320,370)
        self.h = Rectangle(Point(400,r),Point(425,380))
        self.h.setFill("brown")
        self.h.setOutline("brown")
        self.h.draw(self.win)

    def animate(self):
        sleep(0.01)
        self.h.move(-2,0)

        if self.h.getP2().getX() < 0:
            self.h.undraw()
            self.drw()

def main():
    shapeName = chooseShape()

    win = GraphWin("Bouncy Shapes",400,400)
    win.setBackground("#00FFFF")

    shape = Shape(shapeName,win)
    shape.drw()

    grass = Polygon(Point(0,380),Point(400,380),Point(400,400),Point(0,400),Point(0,380))
    grass.setFill("green")
    grass.setOutline("green")
    grass.draw(win)

    sun(win)

    scoreFromFile = readFile("best_score")

    score = [0]
    scoreText = [Text(Point(150,50),"Score: %d" %score[0])]
    scoreText[0].setOutline("red")
    scoreText[0].setSize(18)
    scoreText[0].draw(win)

    bestScore = [int(scoreFromFile[0])]
    bscoreText = [Text(Point(300,50),"Best Score: %d" %bestScore[0])]
    bscoreText[0].setOutline("red")
    bscoreText[0].setSize(18)
    bscoreText[0].draw(win)

    begin = Text(Point(200,200),"Click to start!")
    begin.setOutline("black")
    begin.setSize(30)
    begin.draw(win)

    hurdle = Hurdle(win)
    hurdle.drw()

    stop = [False]

    win.getMouse()
    begin.undraw()

    start_new_thread(backgroundAnim,(hurdle,win,shape,bestScore,stop))

    while stop[0] == False:
        c = win.checkMouse()
        if c != None:
            shape.jump(shape,hurdle,score,scoreText,bestScore,bscoreText)

    sleep(2)
    win.close()

def backgroundAnim(hurdle,win,shape,bestScore,stop):
    while True:
        hurdle.animate()
        if checkCrash(shape,hurdle) == True: break
    gameover(str(bestScore[0]),win)
    stop[0] = True

def checkCrash(shape,hurdle):
    shapeCenterX = shape.s.getCenter().getX()
    shapeCenterY = shape.s.getCenter().getY()
    if shape.name == "square":
        if (shapeCenterX + 30 >= hurdle.h.getP1().getX()) and \
            (shapeCenterY + 30 >= hurdle.h.getP1().getY()) and \
            (shapeCenterX - 30 <= hurdle.h.getP2().getX()): return True
        else: return False
    else:
        ans = False
        for i in range(1,31,1):
            x = shapeCenterX + i
            y = shapeCenterY + sqrt((30**2) - (i**2))
            x2 = shapeCenterX - i
            if (x >= hurdle.h.getP1().getX()) and \
                (y >= hurdle.h.getP1().getY()) and \
                (x2 <= hurdle.h.getP2().getX()): ans = True
        return ans

def chooseShape():
    win = GraphWin("Pick a shape",200,100)

    circ = Circle(Point(60,50),30)
    circ.setFill("red")
    circ.draw(win)

    sq = Rectangle(Point(110,20),Point(170,80))
    sq.setFill("blue")
    sq.draw(win)

    clik = win.getMouse()

    while True:
        if clik.getX() > 110 and clik.getX() < 170 and clik.getY() > 20 and clik.getY() < 80:
            win.close()
            return "square"
            break
        elif clik.getX() > 30 and clik.getX() < 90 and clik.getY() > 20 and clik.getY() < 80:
            win.close()
            return "circle"
            break
        else: clik = win.getMouse()

def sun(win):
    sun = Circle(Point(50,50),20)
    sun.setFill("yellow")
    sun.setOutline("yellow")
    sun.draw(win)

    l1 = Line(Point(50,25),Point(50,10))
    l2 = Line(Point(50,75),Point(50,90))
    l3 = Line(Point(25,50),Point(10,50))
    l4 = Line(Point(75,50),Point(90,50))

    l5 = Line(Point(35,35),Point(20,20))
    l6 = Line(Point(65,65),Point(80,80))
    l7 = Line(Point(65,35),Point(80,20))
    l8 = Line(Point(35,65),Point(20,80))

    lines =[l1,l2,l3,l4,l5,l6,l7,l8]

    for l in lines:
        l.setOutline("yellow")
        l.setWidth(3)
        l.draw(win)

def readFile(name):
    try:
        inFile = open(name + ".txt","r")
        line_list = inFile.readlines()
        inFile.close()

        for i in range(len(line_list)-1):
            line_list[i] = line_list[i][:-1]

        return line_list
    except FileNotFoundError:
        return 0

def gameover(bestScore,win):
    outFile = open("best_score.txt","w")
    outFile.write(bestScore)
    outFile.close()

    over = Text(Point(200,200),"GAME OVER!")
    over.setOutline("black")
    over.setSize(30)
    over.draw(win)

if __name__ == '__main__':
    main()
