class Block(object):
    shapes = ['I', 'J', 'L', 'O', 'S', 'T', 'Z']
    def __init__(self, shape, col, row):
        self.shape = shape
        self.col, self.row = col, row
        self.blockSize = 10 #must come from canvas or well/matrix object
        self.calculateVertices()

    def print(self):
        print('Shape ', self.shape, ' at ', self.row, ',', self.col, sep='')

    def calculateVertices(self):
        if self.shape == 'I':
            sides = [1, 4, 1, 4]
            x0, y0 = self.blockSize * self.col, self.blockSize * (self.row + 1)
            x1, y1 = x0, y0 - self.blockSize * 1
            x2, y2 = x1 + self.blockSize * 4, y1
            x3, y3 = x2, y2 + self.blockSize * 1
            self.vertices = [x0, y0, x1, y1, x2, y2, x3, y3]
        elif self.shape == 'O':
            sizes = [2, 2, 2, 2]
            x0, y0 = self.blockSize * self.col, self.blockSize * (self.row + 1)
            x1, y1 = x0, y0 - self.blockSize * 2
            x2, y2 = x1 + self.blockSize * 2, y1
            x3, y3 = x2, y2 + self.blockSize * 2
            self.vertices = [x0, y0, x1, y1, x2, y2, x3, y3]
        elif self.shape == 'J':
            sizes = [2, 1, 1, 2, 1, 3]
            x0, y0 = self.blockSize * self.col, self.blockSize * (self.row + 1)
            x1, y1 = x0, y0 - self.blockSize * 2
            x2, y2 = x1 + self.blockSize * 1, y1
            x3, y3 = x2, y2 + self.blockSize * 1
            x4, y4 = x3 + self.blockSize * 2, y3
            x5, y5 = x4, y4 + self.blockSize * 1
            self.vertices = [x0, y0, x1, y1, x2, y2, x3, y3, x4, y4, x5, y5]
        elif self.shape == 'L':
            sizes = [1, 2, 1, 1, 2, 3]
            x0, y0 = self.blockSize * self.col, self.blockSize * (self.row + 1)
            x1, y1 = x0, y0 - self.blockSize * 1
            x2, y2 = x1 + self.blockSize * 2, y1
            x3, y3 = x2, y2 - self.blockSize * 1
            x4, y4 = x3 + self.blockSize * 1, y3
            x5, y5 = x4, y4 + self.blockSize * 2
            self.vertices = [x0, y0, x1, y1, x2, y2, x3, y3, x4, y4, x5, y5]
        elif self.shape == 'S':
            sizes = [1, 1, 1, 2, 1, 1, 1, 2]
            x0, y0 = self.blockSize * self.col, self.blockSize * (self.row + 1)
            x1, y1 = x0, y0 - self.blockSize * 1
            x2, y2 = x1 + self.blockSize * 1, y1
            x3, y3 = x2, y2 - self.blockSize * 1
            x4, y4 = x3 + self.blockSize * 2, y3
            x5, y5 = x4, y4 + self.blockSize * 1
            x6, y6 = x5 - self.blockSize * 1, y5
            x7, y7 = x6, y6 + self.blockSize * 1
            self.vertices = [x0, y0, x1, y1, x2, y2, x3, y3, x4, y4, x5, y5, x6, y6, x7, y7]
        elif self.shape == 'Z':
            sizes = [1, 1, 1, 2, 1, 1, 1, 2]
        elif self.shape == 'T':
            sizes = [1, 1, 1, 1, 1, 1, 1, 3]
        else:
            pass

    def draw(self, canvas):
        try:
            canvas.delete(self.polygon)
        except:
            pass
        self.polygon = canvas.create_polygon(*self.vertices, fill='red')
            
    def move(self, event, direction, canvas):
        if direction == 'down':
            self.row += 1
        elif direction == 'left':
            self.col -= 1
        elif direction == 'right':
            self.col += 1
        self.print()
        self.calculateVertices()
        self.draw(canvas)

##    def rotate(self, event, direction, canvas):
##        #rotate around x0, y0 !
##        print(self.vertices)
##        if direction == '+':
##            R = [[0, -1], [1, 0]]
##            for i in range(0, len(self.vertices), 2):
##                #R.v
##                xi = -self.vertices[i+1]
##                yi = self.vertices[i]
##                self.vertices[i], self.vertices[i+1] = xi, yi
##            pass
##        elif direction == '-':
##            R = [[0, 1], [-1, 0]]
##            pass
##        else:
##            pass
##        print(self.vertices)
##        self.draw(canvas)

def mover(canvas):
    def count():
        global counter
        #print(counter)
        if running == True:
            block.move('<Down>', 'down', canvas)
            canvas.after(1000, count)
            counter -= 1
        else:
            pass
    count()


##def drawShape(x0, y0, sides, blockSize, angle):
##    #calculate vertices from side lengths, given an origin an starting angle
##    #x0, y0: origin
##    #blockSize: length of a unit size
##    #angle: starting direction from origin, 90 = up
##    vertices = [(x0, y0), ]
##    i = 1
##    while len(vertices) < len(sides):
##        xi, yi = x0, y0 + blockSize * sides[i-1]
##        vertices.append((xi, yi))
##        i += 1
##        angle = ( angle + 90 ) % 360
##        print(i, angle)
##    return vertices
##print(drawShape(0, 0, [1, 1, 1, 1], 10, 90))
    


import tkinter as tk
import time

global running
running = False
global counter
counter = 0
root = tk.Tk()
frame = tk.Frame(root, borderwidth=2, relief='groove')
frame.focus_set()
frame.pack()
canvas = tk.Canvas(frame, width=100, height=240)
canvas.pack()
frame.bind('<Down>', lambda event, direction='down', canvas=canvas: block.move(event, direction, canvas))
frame.bind('<Left>', lambda event, direction='left', canvas=canvas: block.move(event, direction, canvas))
frame.bind('<Right>', lambda event, direction='right', canvas=canvas: block.move(event, direction, canvas))
frame.bind('<+>', lambda event, direction='+', canvas=canvas: block.rotate(event, direction, canvas))
block = Block('S', 1, 1)
block.print()
block.draw(canvas)
##moveDownButton = tk.Button(root, text='down', command=lambda direction='down', canvas=canvas: block.move(direction, canvas))
##moveDownButton.pack()
##moveLeftButton = tk.Button(root, text='left', command=lambda direction='left', canvas=canvas: block.move(direction, canvas))
##moveLeftButton.pack()
##moveRightButton = tk.Button(root, text='right', command=lambda direction='right', canvas=canvas: block.move(direction, canvas))
##moveRightButton.pack()

running = True
mover(canvas)

tk.mainloop()




    

