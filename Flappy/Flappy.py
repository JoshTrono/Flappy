import pygame
import random
from pygame.locals import *

pygame.init()

clock = pygame.time.Clock()
fps = 60

font = pygame.font.SysFont('Bauhaus 93',60)

white = (255,255,255)

screen_width = 864
screen_height = 936

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Flappy Bird")

#Define variables
ground_scroll = 0
scroll_speed = 4
flying = False
gameover = False
pipe_gap = 150
pipe_frequency = 1500 #milliseconds
last_pipe = pygame.time.get_ticks() - pipe_frequency
score = 0
xcor = 300


#load images
bg = pygame.image.load("img/bg.png")
ground_image = pygame.image.load("img/ground.png")

def draw_text(text, font, text_col, x,y):
    img = font.render(text,True,text_col)
    screen.blit(img,(x,y))

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1,4):
            img = pygame.image.load(f'img/bird{num}.png')
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.vel = 0
        self.clicked = False
    def update(self):
        if flying == True:
            self.vel += 0.5
            if self.vel >8:
                self.vel = 8
            if self.rect.bottom < 768:
                self.rect.y += int(self.vel)

        #jump
        if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False :
            self.clicked = True
            self.vel = -10
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False


        #handle the animation
        self.counter += 1
        flap_cooldown = 5

        if self.counter > flap_cooldown:
            self.counter = 0
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0
        self.image = self.images[self.index]

        #rotate
        self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)

class Pipe(pygame.sprite.Sprite):
    def __init__(self,x,y,position):
        pygame.sprite.Sprite.__init__(self)
        pygame.sprite.LayeredUpdates.__init__(self)
        self.image = pygame.image.load("img/pipe.png")
        self.rect = self.image.get_rect()
        global score
        #position 1 is top -1 is bottom
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x,y - int(pipe_gap / 2)]
        if position == -1:
            self.rect.topleft = [x,y + int(pipe_gap / 2)]
    def update(self):
        global score
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()
        elif self.rect.x == 100:
            score += .5


bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

flappy = Bird(100, int(screen_height / 2))
bird_group.add(flappy)



run = True
while run:

    clock.tick(fps)
    #Draw backgound
    screen.blit(bg, (0,0))

    bird_group.draw(screen)
    bird_group.update()

    pipe_group.draw(screen)
   


    screen.blit(ground_image,(ground_scroll, 768))

    #score

    if gameover == False and flying == True:
        pipe_group.update()
        print(pipe_group)

        #generate new pipes
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipe_height = random.randint(-100,100)
            btm_pipe = Pipe(screen_width, int(screen_height /2) + pipe_height,-1)
            top_pipe = Pipe(screen_width,int(screen_height/2) + pipe_height,1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now
            
        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 35:
            ground_scroll = 0
    
    draw_text(str(int(score)),font,white,int(screen_width/2),80)
    #look for collision

    if pygame.sprite.groupcollide(bird_group,pipe_group, False, False) or flappy.rect.top <0:
        gameover = True


    #checks if bird hits the bottom
    if flappy.rect.bottom > 768:
        gameover = True
        flying = False


    #draw and scroll the ground
 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and gameover == False:
            flying = True
   
    pygame.display.update()
pygame.quit()