#based on
#https://levelup.gitconnected.com/writing-tetris-in-python-2a16bddb5318


import random
import tkinter as tk

colors = ['', 'red', 'green', 'blue', 'cyan', 'yellow', 'magenta']

class Block(object):
    x, y = 0, 0
    blocks = [
        [[1, 5, 9, 13], [4, 5, 6, 7]], #I
        [[1, 2, 5, 6]], #O
        [[2, 3, 6, 10], [1, 5, 6, 7], [2, 6, 9, 10], [5, 6, 7, 11]], #J
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]], #L
        [[2, 5, 6, 7], [2, 5, 6, 10], [5, 6, 7, 10], [2, 6, 7, 10]], #T
        [[5, 6, 10, 11], [2, 5, 6, 9]], #Z
        [[6, 7, 9, 10], [1, 5, 6, 10]], #S
              ]
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.randint(0, len(self.blocks) - 1)
        self.color = random.randint(1, (len(colors) - 1))
        self.rotation = 0

    def image(self):
        return self.blocks[self.type][self.rotation]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.blocks[self.type])

##    def calculateVertices(self):
##        self.vertices = []
##
##    def draw(self, canvas):
##        tiles = self.image()
##        vertices = []
##        for array in self.vertices:
##            vertices.append(array[0])
##            vertices.append(array[1])
##        try:
##            canvas.delete(self.polygon)
##        except:
##            pass
##        self.polygon = canvas.create_polygon(*vertices, fill='red')


class Tetris(tk.Frame):
    def __init__(self, window, height, width):
        super().__init__(window, borderwidth=2, relief='groove')
        self.height = height
        self.width = width
        self.gridSize = 20
        self.canvas = tk.Canvas(self, width=self.width*self.gridSize, height=self.height*self.gridSize)
        self.canvas.pack()
        #self.bind('<Down>', self.goDown)
        self.bind('<Down>', self.goSpace)
        self.bind('<Left>', lambda event, dx=-1: self.goSide(event, dx))
        self.bind('<Right>', lambda event, dx=1: self.goSide(event, dx))
        self.bind('<Up>', self.rotate)
        self.scoreLabel = tk.Label(self, text='Score:')
        self.scoreLabel.pack()
        self.field = []
        self.level = 1
        self.fps = int(1000/self.level)
        self.score = 0
        self.state = 'start'
        self.block = None
        self.blockOutline = 'grey'
        for i in range(height):
            newLine = []
            for j in range(width):
                newLine.append(0)
            self.field.append(newLine)
        self.drawField()
        self.startGame()

    def createBlock(self):
        self.block = Block(3, 0)
        self.drawBlock()

    def drawBlock(self):
        try:
            for rectangle in self.polygon:
                self.canvas.delete(rectangle)
        except:
            pass
        self.polygon = []
        for i in range(4):
            for j in range(4):
                p = 4 * i + j
                if p in self.block.image():
                    x1 = (self.block.x + j) * self.gridSize
                    y1 = (self.block.y + i) * self.gridSize
                    x2 = x1 + self.gridSize
                    y2 = y1 + self.gridSize
                    rectangle = self.canvas.create_rectangle(x1, y1, x2, y2, fill=colors[self.block.color], outline=self.blockOutline)
                    self.polygon.append(rectangle)

    def drawField(self):
        try:
            for rectangle in self.fieldPolygons:
                self.canvas.delete(rectangle)
        except:
            pass
        self.fieldPolygons = []
        for i in range(self.height):
            for j in range(self.width):
                x1 = j * self.gridSize
                y1 = i * self.gridSize
                x2 = x1 + self.gridSize
                y2 = y1 + self.gridSize
                if self.field[i][j] > 0:
                    rectangle = self.canvas.create_rectangle(x1, y1, x2, y2, fill=colors[self.field[i][j]], outline=self.blockOutline)
                    self.fieldPolygons.append(rectangle)
                else:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill='white', outline=self.blockOutline)

    def intersect(self):
        intersection = False
        for i in range(4):
            for j in range(4):
                if 4 * i + j in self.block.image():
                    condition1 = i + self.block.y > self.height - 1
                    condition2 = j + self.block.x > self.width - 1
                    condition3 = j + self.block.x < 0
##                    condition4 = self.field[i + self.block.y][j + self.block.x] > 0 #????
                    if condition1 or condition2 or condition3 or self.field[i + self.block.y][j + self.block.x] > 0: #????
                        intersection = True
        return intersection

    def freeze(self):
        for i in range(4):
            for j in range(4):
                if 4 * i + j in self.block.image():
                    self.field[i + self.block.y][j + self.block.x] = self.block.color
        self.breakLines()
        self.drawField()
        self.createBlock()
        if self.intersect():
            self.state = 'gameover'

    def breakLines(self):
        lines = 0
        for i in range(1, self.height):
            zeros = 0
            for j in range(self.width):
                if self.field[i][j] == 0:
                    zeros += 1
            if zeros == 0:
                lines += 1
                for i1 in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[i1][j] = self.field[i1 - 1][j]
        self.score += lines ** 2
        if lines > 0:
            print('score:', self.score)
            self.scoreLabel['text'] = 'Score: ' + str(self.score)
        #self.drawField()

    def goSpace(self, event):
        while not self.intersect():
            self.block.y += 1
        self.block.y -= 1
        self.freeze()
        self.drawBlock()

    def goDown(self):#, event):
        self.block.y += 1
        if self.intersect():
            self.block.y -= 1
            self.freeze()
        else:
            self.drawBlock()

    def goSide(self, event, dx):
        oldX = self.block.x
        self.block.x += dx
        if self.intersect():
            self.block.x = oldX
        else:
            self.drawBlock()

    def rotate(self, event):
        oldRotation = self.block.rotation
        self.block.rotate()
        if self.intersect():
            self.block.rotation = oldRotation
        else:
            self.drawBlock()

    def startGame(self):
        if self.block is None:
            self.createBlock()
        self.state = 'running'
        self.mover()

    def mover(self):
        def count():
            if self.state == 'running':
                self.goDown()
                self.canvas.after(self.fps, count)
            elif self.state == 'gameover':
                print('gameover')
            else:
                pass
        count()


root = tk.Tk()
tetris = Tetris(root, 20, 10)
tetris.focus_set()
tetris.pack()
root.mainloop()

