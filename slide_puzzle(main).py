import pygame,sys,random
from pygame.locals import *

WIDTH = 800
HEIGHT = 600
BOXSIZE = 90
ROW = 4
COLUMN = 4
GAPSIZE = 5
MARGINX = ( WIDTH - ( ROW * ( BOXSIZE + GAPSIZE ))) / 2
MARGINY = ( HEIGHT - ( COLUMN * ( BOXSIZE + GAPSIZE ))) / 2
COUNT = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]

WHITE = (255, 255, 255)
BLACK = (0,0,0)
GREEN = (0,255,0)
ORANGE = (255,128,0)
PURPLE = (255,0,255)
NAVYBLUE = (0,0,125)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

BGCOLOR = NAVYBLUE
BOXCOLOR = PURPLE
OUTLINE = RED
TEXTCOLOR = BLACK
HIGHLIGHTCOLOR = WHITE

def main():
    global DISPLAYSURF
    global FPSCLOCK, FPS
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('SLIDE PUZZLE')
    FPSCLOCK = pygame.time.Clock()
    FPS = 30
    mousex = 0
    mousey = 0
    DISPLAYSURF.fill(GREEN)
    ANSWER = drawstartingboard()
    pygame.display.update()
    pygame.time.wait(2000)
    boxes, NONE = getboxes()
    mainboard(boxes)
    flag = False

    while True:
        DISPLAYSURF.fill(BGCOLOR)
        mainboard(boxes)
        mouseclicked = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseclicked = True
            boxx, boxy = checkifclickedonbox(mousex, mousey)
            if boxx != None or boxy != None:
                highlightbox(boxx, boxy)
                if mouseclicked == True:
                    NONE, boxes = checkifboxadjacent(boxx, boxy, NONE, boxes)
            flag = checkifwon(boxes, ANSWER)
            if flag == True:
                gamewonanimation()

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def checkifwon(boxes, ANSWER):
    flag = False
    for i in range(16):
        if ANSWER[i] != boxes[i]:
            flag = False
            break
    return flag


def gamewonanimation():
    color_1 = BLACK
    color_2 = BLUE
    for i in range(20):
        color_1, color_2 = color_2, color_1
        DISPLAYSURF.fill(color_1)
        font = pygame.font.Font('freesansbold.ttf',40)
        text=font.render('YOU WON', True, WHITE)
        textrect=text.get_rect()
        textrect.center=(WIDTH//2,HEIGHT//2 )
        DISPLAYSURF.blit(text, textrect)
        pygame.display.update()
        pygame.time.wait(300)


def checkifboxadjacent(boxx, boxy, NONE, boxes):
    adjacent = False
    none = NONE
    ind_1 = 0
    ind_2 = 0
    left = (NONE[0] - 1, NONE[1])
    right = (NONE[0] + 1, NONE[1])
    up = (NONE[0], NONE[1] - 1)
    down = (NONE[0], NONE[1] + 1)
    if (boxx, boxy) == left:
        adjacent = True
        none = (boxx, boxy)
    elif (boxx, boxy) == right:
        adjacent = True
        none = (boxx, boxy)
    elif (boxx, boxy) == up:
        adjacent = True
        none = (boxx, boxy)
    elif (boxx, boxy) == down:
        adjacent = True
        none = (boxx, boxy)
    if adjacent == True:
        for i in range(16):
            if (boxes[i][0], boxes[i][1]) == NONE:
                old_none_val = boxes[i][2]
            if (boxes[i][0], boxes[i][1]) == none:
                new_none_val = boxes[i][2]
        boxes = getnewboxes(old_none_val, new_none_val, boxes, NONE, none)
    return (none, boxes)


def getnewboxes(old_none_val, new_none_val, boxes, NONE, none):
    box = []
    for i in range(16):
        if (boxes[i][0], boxes[i][1]) == NONE:
            box.append((boxes[i][0], boxes[i][1], new_none_val))
        elif (boxes[i][0], boxes[i][1]) == none:
            box.append((boxes[i][0], boxes[i][1], old_none_val))
        else:
            box.append(boxes[i])
    return box



def getboxes():
    count = COUNT[:]
    random.shuffle(count)
    counting = 0
    boxes = []
    none = (0, 0)
    for x in range(ROW):
        for y in range(COLUMN):
            boxes.append((x, y, count[counting]))
            counting = counting + 1
    for i in range(16):
        if boxes[i][2] == 16:
            none = (boxes[i][0], boxes[i][1])
            break
    return (boxes, none)


def highlightbox(boxx, boxy):
    top, left = topleftcoor(boxx, boxy)
    pygame.draw.rect(DISPLAYSURF, HIGHLIGHTCOLOR, (left -3, top -3, BOXSIZE + 6, BOXSIZE + 6), 3)


def checkifclickedonbox(mousex, mousey):
    for x in range(ROW):
        for y in range(COLUMN):
            top, left = topleftcoor(x, y)
            boxrect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if boxrect.collidepoint(mousex, mousey):
                return (x, y)
    return (None, None)


def drawstartingboard():
    count = COUNT[:]
    counting = 0
    boxes = []
    for x in range(ROW):
        for y in range(COLUMN):
            boxes.append((x, y, count[counting]))
            counting = counting + 1
    drawicons(boxes)
    return boxes


def mainboard(boxes):
    drawicons(boxes)

def drawicons(box):
    counting = -1
    for i in range(0,16):
        counting += int(1)
        if box[i][2] != 16:
            half = BOXSIZE // 2
            top, left = topleftcoor(box[i][0], box[i][1])
            pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, BOXSIZE, BOXSIZE))
            font = pygame.font.Font('freesansbold.ttf',18)
            text=font.render(str(box[counting][2]), True, TEXTCOLOR)
            textrect=text.get_rect()
            textrect.center=(left + half, top + half)
            DISPLAYSURF.blit(text, textrect)
    outline()

def topleftcoor(boxx, boxy):
    left = boxx * (BOXSIZE + GAPSIZE) + MARGINX
    top = boxy * (BOXSIZE + GAPSIZE) + MARGINY
    return (top, left)

def outline():
    top, left = topleftcoor(0, 0)
    pygame.draw.rect(DISPLAYSURF, OUTLINE, (left - 4, top - 4, ((BOXSIZE + GAPSIZE) * 4) + 3, ((BOXSIZE + GAPSIZE) * 4) + 3), 4)

if __name__ == "__main__":
    main()
