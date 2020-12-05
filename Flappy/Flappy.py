#Joshua Trono
#Student ID 597503
#import pygame,random,tkinter,ast,json
#ast to convert a text file into a dictionary and json to convert a dictionary into a text file for the scores





import pygame
import random
import tkinter as tk
import ast
import json
from pygame.locals import *

pygame.init()
#Time
clock = pygame.time.Clock()
fps = 60
#adding font
font = pygame.font.SysFont('Bauhaus 93',60)

white = (255,255,255)

screen_width = 864
screen_height = 936

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Flappy Bird")
#Scorelist
with open("scores.txt","r") as data:
    scores = ast.literal_eval(data.read())


#Add the popup

root=tk.Tk()
root.title('Program Selection')
canvas1=tk.Canvas(root,width =300, height=150)
canvas1.pack()
 
#Def prog2
    #sortedItems = sorted(scores.items())
    #canvas3=tk.Canvas(root,screen width = 300, height = 150)
    #canvas3.pack()
    #Text will be the first 5 items in the sorted scorelist
# def prog()
    #x = entry.get which gets the entry from the text field
    #canvas2 = tk.canvas
    #Canvas2.pack()
    #text= displays your score
    #create a new windows showing the text
    #Write your score onto file
    #calls prog2
def prog2():
    sortedItems = sorted(scores.items())
    canvas3=tk.Canvas(root,width = 300, height = 150)
    canvas3.pack()
    text = tk.Label(canvas3,text="{}\n{}\n{}\n{}\n{}".format(sortedItems[0],sortedItems[1],sortedItems[2],sortedItems[3],sortedItems[4]))
    canvas3.create_window(150,40,window = text)
    return
 
def prog():
    x = entry.get()
    canvas2 = tk.Canvas(root, width = 300,height= 150)
    canvas2.pack()
    text = tk.Label(canvas2,text="{} Your score is {}".format(x, score))
    canvas2.create_window(150,60,window=text)
    root.mainloop
    
    scores['{}'.format(x)] = score
  #  clock.wait(1500)
    with open('scores.txt', 'w') as file:
        file.write(json.dumps(scores))
    prog2()
    return
 

labelTop=tk.Label(canvas1,text='Enter your name')
canvas1.create_window(150,20,window=labelTop)

entry = tk.Entry(canvas1)
canvas1.create_window(150,50,window = entry)
button1=tk.Button(text='submit',command = prog)
canvas1.create_window(150,75,window=button1)
 
button2=tk.Button(text='Scorelist',command=prog2)
canvas1.create_window(150,110,window=button2)


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
imgreset = pygame.image.load("img/restart.png")
scorebtn = pygame.image.load("img/score.png")

#draw_text(text,font,text color,x,y)
    #img = font.render(text,True,text color)
    #screen.blit(img,(x,y)) #To display the text

#Def Reset()
    #pipe_group.empty #Removes the pipes
    #score Resets
    #places the character back
def draw_text(text, font, text_col, x,y):
    img = font.render(text,True,text_col)
    screen.blit(img,(x,y))
def reset():
    pipe_group.empty()
    score = 0
    flappy.rect.x = 100
    flappy.rect.y = int(screen_height/2)
    
#Class Buttons
    #Init self with x,y and an image variable
        #self.image = image
        #self.rect = self.image.get_rect()
        #self.rect.topleft = (x,y) to place the topleft of the image to be where the x,y position is
    #def draw(self)
        #action = False #for the button action to be False unless pressed

        #pos = pygame.mouse.get_pos() to display if the mouse is over the button
        #if self.rect.collidepoint(pos): # IF the mouse pos is over the button
            #if pygame.mouse.get_pressed()[0] == 1 THAN: if left button gets clicked
                #action = True
                # return action which is true
        #screen.blit to draw the button
class Buttons():
    def __init__(self,x,y,image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
    def draw(self):
        action = False
        #Mouse position
        pos = pygame.mouse.get_pos()
        #Check if pressed
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True
                return action
        screen.blit(self.image,(self.rect.x,self.rect.y))

#Class bird(pygame.Sprite.Sprite)
    #init(self,x,y)
        #pygame.sprite.Sprite.__init__(self) to make a pygame sprite
        # self.images = []
        #self.index = 0
        #self.counter = 0 
        #for num in range(1,4):
            #img = pygame.image.load(f'img/bird{num}.png')
            #self.images.append(img)
       #self.image = self.images[self.index]
       #self.rect = self.image.get_rect()
       #self.center = [x,y]
       #self.vel = 0 for the velacity
       #self.clicked = False
    #def update(self):
          #if flying == True:
          #  self.vel += 0.5
          #  if self.vel >8:
          #      self.vel = 8
          #  if self.rect.bottom < 768:
          #      self.rect.y += int(self.vel)

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

button = Buttons(100,100,imgreset)
btnscore = Buttons(600,100,scorebtn)

run = True
while run:

    clock.tick(fps)
    #Draw backgound
    screen.blit(bg, (0,0))

    bird_group.draw(screen)
    bird_group.update() # update Every time

    pipe_group.draw(screen)
   


    screen.blit(ground_image,(ground_scroll, 768))

    #score

    if gameover == False and flying == True:
        pipe_group.update() # update the pipes only if your flying
     #   print(pipe_group)

        #generate new pipes
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency: # if the timenow - when the last pipe got made is greater than the frequency Than make another pipe with a pipe gap.
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

    #if sprites collide or flappy is above the screen than its game over

    if pygame.sprite.groupcollide(bird_group,pipe_group, False, False) or flappy.rect.top <0:
        gameover = True 


    #checks if bird hits the bottom
    if flappy.rect.bottom > 768:
        gameover = True
        flying = False


    if gameover == True: #if gameover than display both buttons
        if btnscore.draw() == True:
            root.mainloop()
        if button.draw() == True:
            gameover = False
            reset()
 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and gameover == False:
            flying = True
   
    pygame.display.update()
pygame.quit()