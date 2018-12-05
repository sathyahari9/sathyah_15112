# file taken from reddit.com, will be modified significantly for TP3. A similar mechanism will be used for making the blocks fall to implement GuitarHero.
# please ignore the following code for TP2, it is for my future reference.
import random
import pygame
from pygame.locals import *
pygame.init()
global clr
gfret = ( 43, 255, 0 )
rfret = ( 255, 0, 12 )
yfret = ( 255, 255, 0 )
bfret = ( 0, 171, 255)
ofret = ( 255, 84, 0 )
blk = ( 0, 0, 0 )
wte = ( 255, 255, 255 )
brwn = ( 133, 55, 0 )
#
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
done = False
xpos = (250 , 350 ,450, 550, 650)
note_list = []

def drawBoard(screen):
    pygame.draw.polygon(screen, blk,((200,900),(700,900),(700,0),(200,0),(200,900)),0)
    pygame.draw.polygon(screen, gfret,((200,850),(300,850),(300,800),(200,800),(200,850)),0)
    pygame.draw.polygon(screen, rfret,((300,850),(400,850),(400,800),(300,800),(300,850)),0)
    pygame.draw.polygon(screen, yfret,((400,850),(500,850),(500,800),(400,800),(400,850)),0)
    pygame.draw.polygon(screen, bfret,((500,850),(600,850),(600,800),(500,800),(500,850)),0)
    pygame.draw.polygon(screen, ofret,((600,850),(700,850),(700,800),(600,800),(600,850)),0)
    #ellipse is (x,y,stretch x, stretch y)

def getFretColor(color, xpos):
    if xpos == 250:
        color = ( 43, 255, 0 )
    elif xpos == 350:
        color = ( 255, 0, 12 )
    elif xpos == 450:
        color = ( 255, 0, 12 )
    elif xpos == 550:
        color = ( 255, 0, 12 )
    elif xpos == 650:
        color = ( 255, 0, 12 )
    return color

pygame.init()
#draws the window
screen=pygame.display.set_mode((900,900))
pygame.display.set_caption("Python Hero")
screen.fill(wte)
drawBoard(screen)

for i in range(1):
    x = random.choice(xpos)
    if x == 250:
        clr = gfret
    elif x == 350:
        clr = rfret
    elif x == 450:
        clr = yfret
    elif x == 550:
        clr = bfret
    elif x == 650:
        clr = ofret
    y = random.randrange(-100, 0)
    note_list.append([x, y])

clock = pygame.time.Clock()

#MAIN PROGRAM

done = False
while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    drawBoard(screen)
    for i in range(len(note_list)):
        pygame.draw.ellipse(screen, wte, (note_list[i][0]-45,note_list[i][1]-5, 90,55))
        pygame.draw.ellipse(screen, clr, (note_list[i][0]-40,note_list[i][1], 80,45))

        note_list[i][1] += 12
        pygame.display.flip()
        if note_list[i][1] > 900:
            y = random.randrange(-100, 0)
            note_list[i][1] = y
            x = random.choice(xpos)
            if x == 250:
                clr = gfret
            elif x == 350:
                clr = rfret
            elif x == 450:
                clr = yfret
            elif x == 550:
                clr = bfret
            elif x == 650:
                clr = ofret
            note_list[i][0] = x

    pygame.display.flip()
    clock.tick(60)


pygame.quit()