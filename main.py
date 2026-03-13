import pygame as pg
from pygame.locals import *

from sys import exit
from itertools import chain

pg.init()

W = 600
H = 400

screen = pg.display.set_mode((W, H), 0, 32)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 223, 0)
RUSSET = (60, 35, 27)
RED = (255, 0, 0)

board_sprite = pg.image.load("pygaming/naturalwood.jpeg")
king_sprite = pg.image.load("pygaming/crown.png")
def_sprite = pg.image.load("pygaming/shield.jpg")
att_sprite = pg.image.load("pygaming/sword.png")

# LISTS -----

cells_all = {}
cells_win = {}
cell_center = {}

occupied_def = {}
occupied_att = {}

buttons = []

active_objects = {}
king_coordinates = None

chosen = None
possib_cells = []
player_counter = 1
active_func = None

# CLASSES ------

class Button():

    def __init__(self, coordinates, function, text):
        self.coordinates = coordinates
        self.text = text
        self.function = function

        self.rect = pg.Rect(self.coordinates[0], self.coordinates[1], 250, 75)

class Cell():

    def __init__(self, side, color, thickness, coordinates):
        self.side = 30
        self.color = color
        self.thickness = thickness
        self.coordinates = coordinates

        self.rect = pg.Rect(self.coordinates[0], self.coordinates[1], side, side)
        cells_all.update({self.coordinates : self})

    def render(self):
        pg.draw.rect(screen, self.color, self.rect, self.thickness)

    def is_occupied(self):
        # put in occupied
        # 
        pass


class Cell_Norm(Cell):
    def __init__(self, coordinates):
        Cell.__init__(self, 30, WHITE, 3, coordinates)

class Cell_Win(Cell):
    def __init__(self, coordinates):
        Cell.__init__(self, 30, YELLOW, 0, coordinates)
        cells_win.update({self.coordinates : self})

        self.enemy_class = None

class Cell_Center(Cell):
    def __init__(self, coordinates):
        Cell.__init__(self, 30, WHITE, 8, coordinates)
        cell_center.update({self.coordinates : self})

        global king_coordinates
        king_coordinates = list(cell_center.keys())[0]

        self.enemy_class = None

# ---------------------------------------------------------------- #

class Checker():

    def __init__(self, sprite, coordinates, *restrictions): # change everything (sprites) later
        self.sprite = sprite
        self.coordinates = coordinates
        self.rect = pg.Rect(self.coordinates[0], self.coordinates[1], 30, 30)

        self.enemy_class = None
        self.restrictions = restrictions

    def render(self): # change to sprite later
        #pg.draw.rect(screen, self.color, self.rect)
        screen.blit(self.sprite, self.rect)

    def update_restricted(self):
        self.restricted = [i for i in chain({**occupied_def, **occupied_att}.keys(), *self.restrictions)]

    #-----#

    def check_killed(self): # THINK!!!!!!!!!!! - that should work

        global active_objects
        
        if king_coordinates == list(cell_center.keys())[0]: active_objects = {**occupied_def, **occupied_att, **cells_win}
        else: active_objects = {**occupied_def, **occupied_att, **cells_win, **cell_center}

        counter_x, counter_y = 0, 0

        def inner_kill(x, y):
            
            if (type(self).__name__ == "Checker_Att"):
                return self.killed()
                                            
            if (type(self).__name__ == "Checker_Def"):
                return self.killed()
                                   
            if (type(self).__name__ == "Checker_King"):
                if self.near_throne():
                    if (x == 1 and y == 1): return self.killed()
                    else: return None
                else: return self.killed()

        try:

            if (isinstance(active_objects[(self.coordinates[0] + 27, self.coordinates[1])], self.enemy_class) and isinstance(active_objects[(self.coordinates[0] - 27, self.coordinates[1])], self.enemy_class)):
                counter_x += 1
                inner_kill(counter_x, counter_y) 

        except (KeyError, UnboundLocalError): pass

        try:

            if isinstance(active_objects[(self.coordinates[0], self.coordinates[1] + 27)], self.enemy_class) and isinstance(active_objects[(self.coordinates[0], self.coordinates[1] - 27)], self.enemy_class):
                counter_y += 1
                inner_kill(counter_x, counter_y)

        except (KeyError, UnboundLocalError): pass
    
    def killed(self):
        global player_counter
        player_counter -= 1

        if type(self).__name__ == "Checker_Att":
            Checker_Def.murder_count += 1
            del occupied_att[self.coordinates]

        if type(self).__name__ == "Checker_Def":
            Checker_Att.murder_count += 1
            del occupied_def[self.coordinates]

        if type(self).__name__ == "Checker_King":
            Checker_Att.murder_count = 9
            
        del self

        check_win()

class Checker_Att(Checker):

    murder_count = 0
    dict = occupied_att

    def __init__(self, coordinates):
        Checker.__init__(self, att_sprite, coordinates, cells_win)
        self.dict.update({self.coordinates : self})

        self.enemy_class = (Checker_Def, Cell_Win, Cell_Center)

class Checker_Def(Checker):

    murder_count = 0
    dict = occupied_def

    def __init__(self, coordinates):
        Checker.__init__(self, def_sprite, coordinates, cells_win)
        self.dict.update({self.coordinates : self})

        self.enemy_class = (Checker_Att, Cell_Win, Cell_Center)

class Checker_King(Checker_Def):

    dict = occupied_def

    def __init__(self, coordinates):
        Checker.__init__(self, king_sprite, coordinates, (0,0))
        self.dict.update({self.coordinates :  self})

        self.enemy_class = (Checker_Att, Cell_Win, Cell_Center)
    
    def update_king_coord(self):
        global king_coordinates
        king_coordinates = self.coordinates

    def near_throne(self):
        s = self.coordinates
        c = list(cell_center.keys())[0]

        if s == (c[0], c[1]) or s == (s[0], c[1] + 27) or s == (s[0], c[0] - 27) or s == (c[0] + 27, s[1]) or s == (c[0] - 27, s[1]): return True
        else: return False
        

# WORLD ---------------------------------------------------------

def create_cells(quant):
    coorstart_x = ((W - 30 * quant) / 2) + 15 - 27 # + halfside (15) because of topleft - side - thickness (27)
    coorstart_y = ((H - 30 * quant) / 2) + 15 # + halfside (15) because of topleft
    center = (quant // 2)
    x = coorstart_x

    for i in range(quant):
        x += 27 # side - thickness
        y = coorstart_y

        for j in range(quant):

            if (i == 0 or i == quant - 1) and (j == 0 or j == quant - 1):
                Cell_Win((x, y))
                
            elif i == center and j == center:
                Cell_Center((x,y))
                
            else:
                Cell_Norm((x,y))
                
            y += 27 # side - thickness

def draw_cells():
    for cell in cells_all.values():
        cell.render()

def create_checkers_9():
    coorstart_x = ((W - 30 * 9) / 2) + 15 - 27 # + halfside (15) because of topleft - side - thickness (27)
    coorstart_y = ((H - 30 * 9) / 2) + 15 # + halfside (15) because of topleft
    x = coorstart_x

    val_att = [(0,3), (0,4), (0,5), (1,4),
               (3,0), (3,8), (4,0), (4,1), (4,7), (4,8), (5,0), (5,8),
                (7,4), (8,3), (8,4), (8,5)]
    val_def = [(2,4), (3,4),
               (4,2), (4,3), (4,5), (4,6),
               (5,4), (6,4)]
    val_king = [(4,4)]

    counter_w = 0
    counter_b = 0

    for i in range(9):
        x += 27 # side - thickness
        y = coorstart_y

        for j in range(9):
            try:
                if i == val_att[counter_b][0]:
                    if j == val_att[counter_b][1]:
                
                        Checker_Att((x,y))

                        counter_b += 1

                if i == val_def[counter_w][0]:
                    if j == val_def[counter_w][1]:

                        Checker_Def((x,y))

                        counter_w += 1

                if i == val_king[0][0] and j == val_king[0][1]:
                        
                    Checker_King((x,y))

            except IndexError:
                pass
            
            y += 27
    
def draw_checkers():
    for checker in {**occupied_def, **occupied_att}.values():
        checker.render()

def create_buttons():
    coor_start_x, coor_start_y = (W-250)//2 , (H-((75+40)*3)+40)//2

    button = Button((coor_start_x, coor_start_y), play, "PLAY")
    buttons.append(button)
    coor_start_y += 75+40

    button = Button((coor_start_x, coor_start_y), options, "OPTIONS")
    buttons.append(button)
    coor_start_y += 75+40

    button = Button((coor_start_x, coor_start_y), exit_game, "EXIT GAME")
    buttons.append(button)

# ----- #

def choose(m_pos):
    global chosen

    if player_counter % 2 == 0: active_dict = occupied_def
    else: active_dict = occupied_att
    
    for checker in active_dict.values():
        if checker.rect.collidepoint(m_pos):
            chosen = checker
        
def possib_moves(): # WITHOUT CENTRAL CELL, when boarder reached - cycle ends (fixed: everything in try - except)
    global possib_cells

    try:
        next_cell_x = chosen.coordinates[0] + 27 # coord[1] is constant
        while (next_cell_x, chosen.coordinates[1]) not in chosen.restricted:
            possib_cells.append(cells_all[(next_cell_x, chosen.coordinates[1])])
            next_cell_x += 27
    except (KeyError, AttributeError): pass

    try:
        prev_cell_x = chosen.coordinates[0] - 27 # coord[1] is constant
        while (prev_cell_x, chosen.coordinates[1]) not in chosen.restricted:
            possib_cells.append(cells_all[(prev_cell_x, chosen.coordinates[1])])
            prev_cell_x -= 27
    except (KeyError, AttributeError): pass
    
    try:
        next_cell_y = chosen.coordinates[1] + 27 # coord[0] is constant
        while (chosen.coordinates[0], next_cell_y) not in chosen.restricted:
            possib_cells.append(cells_all[(chosen.coordinates[0], next_cell_y)])
            next_cell_y += 27
    except (KeyError, AttributeError): pass
    
    try:        
        prev_cell_y = chosen.coordinates[1] - 27 # coord[0] is constant
        while (chosen.coordinates[0], prev_cell_y) not in chosen.restricted:
            possib_cells.append(cells_all[(chosen.coordinates[0], prev_cell_y)])
            prev_cell_y -= 27
    except (KeyError, AttributeError): pass

def move_checker(m_pos):
    global possib_cells
    global chosen
    global player_counter

    if (type(chosen).__name__ != "Checker_King") and (list(cell_center.values())[0] in possib_cells): possib_cells.remove(list(cell_center.values())[0])
    
    for cell in possib_cells:
        if cell.rect.collidepoint(m_pos):
            # get key of destination cell and attach checker to this key

            dest_coord = [i for i in cells_all if cells_all[i] == cell]
            chosen.dict.update({dest_coord[0] : chosen})
            del chosen.dict[chosen.coordinates]

            chosen.rect.move_ip(dest_coord[0][0] - chosen.coordinates[0], dest_coord[0][1] - chosen.coordinates[1])
            chosen.coordinates = dest_coord[0]

            if isinstance(chosen, Checker_King): chosen.update_king_coord()

            check_win()

            player_counter += 1
            possib_cells = []
            chosen = None

def check_win():

    if ((isinstance(chosen, Checker_King)) and (chosen.coordinates in list(cells_win.keys()))) or Checker_Def.murder_count == 16:
        print ("Defenders won!")
        exit()
    if Checker_Att.murder_count == 9:
        print("Attackers won!")
        exit()        

# MENU -------------------------------------------------------------

def play():
    global possib_cells
    global chosen
    global active_func

    for event in pg.event.get():
        if event.type == QUIT:
            exit()
        if (event.type == KEYDOWN) and (event.key == K_ESCAPE):
            active_func = call_menu
        if (event.type == MOUSEBUTTONDOWN) and (event.button == 1):
            possib_cells = []
            try:
                choose(event.pos)
                chosen.update_restricted()
                possib_moves()
                move_checker(event.pos)
            except (KeyError, AttributeError): chosen = None

    for checker in list({**occupied_def, **occupied_att}.values()):
        checker.check_killed()

        # ПО ВСЕЙ ВИДИМОСТИ ПРОБЛЕМА БЫЛА В ТОМ, ЧТО EXCEPT ВОЗНИКАЛ НА ПЕРВОЙ ЧАСТИ УСЛОВИЯ, НЕ ДАВАЯ ВТОРОМУ ПРОВЕРИТЬСЯ
        # ОБЯЗАТЕЛЬНО ПОЗЖЕ РАЗОБРАТЬ ЭТОТ МОМЕНТ 

    draw_cells()
    draw_checkers()

    for cell in possib_cells:
        pg.draw.circle(screen, RED, cell.rect.center, 2)

def call_menu():
    global active_func

    for button in buttons:
        pg.draw.rect(screen, RUSSET, button.rect)

    for event in pg.event.get():
        if event.type == QUIT:
            exit()
        for button in buttons: #can't put higher
            if (event.type == MOUSEBUTTONDOWN) and (event.button == 1) and (button.rect.collidepoint(event.pos)):
                active_func = button.function
 
def options():
    global active_func

    for event in pg.event.get():
        if (event.type == KEYDOWN) and (event.key == K_ESCAPE):
            active_func = call_menu
        if event.type == QUIT:
            exit()

def exit_game():
    exit()

# RUN (func later)--------------------------------------------------

def run():
    global active_func
    active_func = call_menu

    clock = pg.time.Clock()

    create_buttons()
    create_cells(9)
    create_checkers_9()

    while True:

        screen.blit(board_sprite, (0, 0))
        
        active_func()

        clock.tick(60)
        pg.display.update()

if __name__ == "__main__":
    run()