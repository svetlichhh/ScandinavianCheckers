class Class1:
    def __init__(self, id):
        self.id = id
    #...
    def test(self):
        return 1000 + self.id

class Now(Class1):
    # ...
    pass

dictt = {}
lis = []

#for num in range(4):
#    print("obj"+str(num))

import pygame as pg
from pygame.locals import *
from sys import exit

WHITE = (255, 255, 255)
YELLOW = (255, 223, 0)

W = 600
H = 400

screen = pg.display.set_mode((W, H), 0, 32)

class Object():
    def __init__(self):
        pass

class Cell(Object):

    count = 0

    def __init__(self, side, color, thickness, coordinates):
        self.side = side
        self.color = color
        self.thickness = thickness
        self.coordinates = coordinates
        self.rect = pg.Rect(self.coordinates[0], self.coordinates[1], side, side)

    def render(self):
        pg.draw.rect(screen, self.color, self.rect, self.thickness)

cell = Cell(30, YELLOW, 0, (40,60))
cell2 = Cell(30, YELLOW, 0, (120,60))

dictt.update({1 : cell})
dictt.update({2 : cell2})

while True:
    for event in pg.event.get():
        if event.type == QUIT:
            exit()

    screen.fill((0, 0, 0))
    print(dictt)
    print("next!")

    try:
        cell.render()
        counter = 0
       
        if pg.mouse.get_pressed()[0] and cell.rect.collidepoint(pg.mouse.get_pos()):
            print("that's right!")
            del cell

    except NameError: pass

    print(dictt[1])

    #print(Cell.count)
    
    #if isinstance(cell, Object):
    #    print("!!!!!!!!!!")

    #if type(cell).__name__ == "Object":
    #    print("nice!")

    pg.display.update()
