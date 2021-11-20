import sys
import pygame
from pygame.locals import *

pygame.font.init()

SCREENWIDTH = 600
SCREENHEIGHT = 600
BORDER = 200
diff_r = SCREENHEIGHT/9
diff_c = SCREENWIDTH/9
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT + BORDER))

# Backgroung color
B_COLOR = (255, 255, 255)

# Line Color
L_COLOR = (0, 0, 0)
# Line thickness
b_L_thick = 5
L_thick = 1

# Box color & its thickness
BX_COLOR = (255, 0, 0)
BX_thick = 5

# Grid font
T1_COLOR = (0, 0, 0)
f1_size = int((diff_r + diff_c)/3)
font1 = pygame.font.SysFont(None, f1_size)

# Details font
T2_COLOR = (0, 0, 0)
f2_size = int(BORDER/5)
font2 = pygame.font.SysFont("comicsans", f2_size)
text1 = font2.render('Press R to Reset the board', 1, T2_COLOR)
text2 = font2.render('Press Enter to get results', 1, T2_COLOR)
x_t1 = 2
y_t1 = SCREENHEIGHT + (BORDER)/20
x_t2 = 2
y_t2 = y_t1 + f2_size

# Decision font
T3_COLOR = (57, 255, 20)
f3_size = int(2*BORDER/5)
font3 = pygame.font.SysFont(None, f3_size)
text3 = font3.render('WRONG SUDOKO', 1, T3_COLOR)
x_t3 = (SCREENWIDTH - text3.get_width())/2
y_t3 = y_t2 + f2_size

# Highlight Color
H_COLOR = (211, 211, 211)

# wrong ans flag
wrong = 0

x = int(-100)
y = int(-100)
grid = [[-1 for i in range(9)] for j in range(9)]


# Class that solves the sudoko
class Solver:
    def __init__(self):
        pass
    
    def helper(self, i = 0, j = 0):
        if i == 9:
            return True
        if j == 9:
            return self.helper(i+1)
        
        if grid[i][j] != -1:
            return self.helper(i, j+1)

        for val in range(1, 10):
            if self.check(i, j, val):
                self.grid[i][j] = val
                if self.helper(i, j+1):
                    return True

                grid[i][j] = -1

        return False

    def solve(self, grid):
        self.grid = grid
        return self.helper()
        
    
    def check(self, i, j, val):
        if(i < 0 or j < 0 or i > 8 or j > 8 or val < 1 or val > 9):
            return False
        
        for k in range(9):
            if self.grid[k][j] == val or self.grid[i][k] == val:
                return False
        
        for p in range(3):
            for q in range(3):
                if self.grid[3*int(i/3) + p][3*int(j/3) + q] == val:
                    return False
        return True

s = Solver()

# Checks wether a val is suitable for that position or not
def check(i, j, val):
    if(i < 0 or j < 0 or i > 8 or j > 8 or val < 1 or val > 9):
        return False
    
    for k in range(9):
        if grid[k][j] == val or grid[i][k] == val:
            return False
    
    for p in range(3):
        for q in range(3):
            if grid[3*int(i/3) + p][3*int(j/3) + q] == val:
                return False
    return True


# Gives the coordinates of the click
def get_cord(pos):
    global x
    x = int(pos[0]//diff_c)
    global y
    y = int(pos[1]//diff_r)

# For exiting the system
def Exit():
    pygame.quit()
    sys.exit()

# Managing the solution
def Calc():
    global grid, wrong
    temp = grid
    if s.solve(temp):
        grid = temp
    else:
        wrong = 1000

# for drawing the inline of the grid
def draw():
    SCREEN.fill(B_COLOR)
    SCREEN.blit(text1, (x_t1, y_t1))
    SCREEN.blit(text2, (x_t2, y_t2))
    for i in range(10):
        if i%3 == 0:
            thick = b_L_thick
        else:
            thick = L_thick
        pygame.draw.line(SCREEN, L_COLOR, (0, i*diff_r), (SCREENWIDTH, i*diff_r), thick)
        pygame.draw.line(SCREEN, L_COLOR, (i*diff_c, 0), (diff_c*i, SCREENHEIGHT), thick)

    global wrong
    if wrong > 0:
        wrong = max(wrong - 1, 0)
        SCREEN.blit(text3, (x_t3, y_t3))

# for drawing the outline of the highlighted box
def draw_box():
	for i in range(2):
		pygame.draw.line(SCREEN, BX_COLOR, (x * diff_c-3, (y + i)*diff_r), (x * diff_c + diff_c + 3, (y + i)*diff_r), BX_thick)
		pygame.draw.line(SCREEN, BX_COLOR, ((x + i)* diff_c, y * diff_r), ((x + i) * diff_c, y * diff_r + diff_r), BX_thick)

# for printing the grid
def print_grid():
    x = 0
    y = 0
    for row in grid:
        for val in row:
            if val != -1:
                text = font1.render(str(val), 1, T1_COLOR)
                SCREEN.blit(text, (x + diff_c/3, y + diff_r/3))
                pass
            x += diff_c
        x = 0
        y += diff_r

# Resets the Grid
def reset():
    global grid
    grid = [[-1 for i in range(9)] for j in range(9)]

# Deletes the character at that position
def Del():
    if(x >= 0 and y >= 0 and x < 9 and y < 9):
        grid[y][x] = -1


def WelcomeScreen():
    
    global x, y
    
    while 1:
        val = 0
        flag2 = False
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                Exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                get_cord(pos)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x = max(0, x-1)
                elif event.key == pygame.K_RIGHT:
                    x = min(8, x+1)
                elif event.key == pygame.K_UP:
                    y = max(0, y-1)
                elif event.key == pygame.K_DOWN:
                    y = min(8, y+1)
                elif event.key == pygame.K_1:
                    flag2 = True
                    val = 1
                elif event.key == pygame.K_2:
                    flag2 = True
                    val = 2
                elif event.key == pygame.K_3:
                    flag2 = True
                    val = 3
                elif event.key == pygame.K_4:
                    flag2 = True
                    val = 4
                elif event.key == pygame.K_5:
                    flag2 = True
                    val = 5
                elif event.key == pygame.K_6:
                    flag2 = True
                    val = 6
                elif event.key == pygame.K_7:
                    flag2 = True
                    val = 7
                elif event.key == pygame.K_8:
                    flag2 = True
                    val = 8
                elif event.key == pygame.K_9:
                    flag2 = True
                    val = 9
                elif event.key == K_RETURN:
                    Calc()
                elif event.key == K_r:
                    reset()
                elif event.key == K_DELETE or event.key == K_BACKSPACE:
                    Del()
        
        draw()
        draw_box()
        print_grid()
        if flag2 and check(y, x, val):
            grid[y][x] = val

        pygame.display.update()

def main():
    pygame.init()
    pygame.display.set_caption("Sudoko Solver by Rocko")
    img = pygame.image.load('gallery/pictures/icon.png')
    pygame.display.set_icon(img)
    WelcomeScreen()

if __name__ == '__main__':
    main()
