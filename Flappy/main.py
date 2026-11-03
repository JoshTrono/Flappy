# Joshua Trono
# Flappy Bird - web (pygbag) version

import asyncio
import ast
import json
import random

import pygame

pygame.init()
pygame.mixer.init()

# Audio (browsers only allow sound after a click, so it starts on the first click)
pygame.mixer.music.load("audio/airtone_-_reCreation.ogg")
pygame.mixer.music.set_volume(0.03)
music_started = False

clock = pygame.time.Clock()
fps = 60

# Fonts (no SysFont on the web)
font = pygame.font.Font(None, 80)
small_font = pygame.font.Font(None, 40)

white = (255, 255, 255)
black = (0, 0, 0)

screen_width = 864
screen_height = 936

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Flappy Bird")

# Scorelist
try:
    with open("scores.txt", "r") as data:
        scores = ast.literal_eval(data.read())
except Exception:
    scores = {}


def save_scores():
    # In the browser this only lasts until the page is reloaded
    try:
        with open("scores.txt", "w") as file:
            file.write(json.dumps(scores))
    except Exception:
        pass


# Define variables
ground_scroll = 0
scroll_speed = 4
flying = False
gameover = False
pipe_gap = 150
pipe_frequency = 1500  # milliseconds
last_pipe = pygame.time.get_ticks() - pipe_frequency
score = 0

entering_name = False
name_text = ""
show_scores = False

# Load images
bg = pygame.image.load("img/bg.png")
ground_image = pygame.image.load("img/ground.png")
imgreset = pygame.image.load("img/restart.png")
scorebtn = pygame.image.load("img/score.png")


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def reset():
    global score, flying, gameover, show_scores, entering_name, last_pipe
    pipe_group.empty()
    score = 0
    flying = False
    gameover = False
    show_scores = False
    entering_name = False
    last_pipe = pygame.time.get_ticks() - pipe_frequency
    flappy.rect.x = 100
    flappy.rect.y = int(screen_height / 2)
    flappy.vel = 0


def end_game():
    global gameover, entering_name, name_text
    if not gameover:
        gameover = True
        entering_name = True
        name_text = ""


class Buttons():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1, 4):
            img = pygame.image.load(f'img/bird{num}.png')
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.clicked = False

    def update(self):
        if flying:
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < 768:
                self.rect.y += int(self.vel)

        # jump
        if not gameover:
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                self.vel = -10
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # handle the animation
        self.counter += 1
        flap_cooldown = 5

        if self.counter > flap_cooldown:
            self.counter = 0
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0
        self.image = self.images[self.index]

        # rotate
        self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/pipe.png")
        self.rect = self.image.get_rect()
        # position 1 is top, -1 is bottom
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(pipe_gap / 2)]
        if position == -1:
            self.rect.topleft = [x, y + int(pipe_gap / 2)]

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

button = Buttons(100, 100, imgreset)
btnscore = Buttons(600, 100, scorebtn)


def draw_scoreboard():
    panel = pygame.Rect(182, 220, 500, 480)
    pygame.draw.rect(screen, black, panel)
    pygame.draw.rect(screen, white, panel, 4)
    draw_text("Top 10", font, white, panel.x + 150, panel.y + 15)
    top = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)[:10]
    for i, (name, pts) in enumerate(top):
        draw_text(f"{i + 1}. {name}: {pts}", small_font, white,
                  panel.x + 40, panel.y + 90 + i * 38)
    if not top:
        draw_text("No scores yet", small_font, white, panel.x + 40, panel.y + 100)


def draw_name_entry():
    panel = pygame.Rect(182, 380, 500, 160)
    pygame.draw.rect(screen, black, panel)
    pygame.draw.rect(screen, white, panel, 4)
    draw_text(f"Your score: {int(score)}", small_font, white, panel.x + 30, panel.y + 20)
    draw_text("Type your name, press Enter:", small_font, white, panel.x + 30, panel.y + 60)
    draw_text(name_text + "_", small_font, white, panel.x + 30, panel.y + 105)


async def main():
    global ground_scroll, flying, last_pipe, music_started
    global entering_name, name_text, show_scores, score

    run = True
    while run:
        clock.tick(fps)

        # Draw background
        screen.blit(bg, (0, 0))

        bird_group.draw(screen)
        bird_group.update()

        pipe_group.draw(screen)

        screen.blit(ground_image, (ground_scroll, 768))

        if not gameover and flying:
            pipe_group.update()

            # generate new pipes
            time_now = pygame.time.get_ticks()
            if time_now - last_pipe > pipe_frequency:
                pipe_height = random.randint(-100, 100)
                btm_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, -1)
                top_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, 1)
                pipe_group.add(btm_pipe)
                pipe_group.add(top_pipe)
                last_pipe = time_now

            ground_scroll -= scroll_speed
            if abs(ground_scroll) > 35:
                ground_scroll = 0

        draw_text(str(int(score)), font, white, int(screen_width / 2), 80)

        # collisions
        if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
            end_game()

        if flappy.rect.bottom > 768:
            end_game()
            flying = False

        if gameover:
            button.draw()
            btnscore.draw()
            if show_scores:
                draw_scoreboard()
            if entering_name:
                draw_name_entry()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if not music_started:
                    pygame.mixer.music.play(-1, 0.0)
                    music_started = True

                if gameover:
                    if btnscore.rect.collidepoint(event.pos):
                        show_scores = not show_scores
                    elif button.rect.collidepoint(event.pos):
                        reset()
                elif not flying:
                    flying = True

            if event.type == pygame.KEYDOWN and entering_name:
                if event.key == pygame.K_RETURN:
                    player = name_text.strip() or "Player"
                    scores[player] = int(score)
                    save_scores()
                    entering_name = False
                    show_scores = True
                elif event.key == pygame.K_BACKSPACE:
                    name_text = name_text[:-1]
                elif event.unicode and event.unicode.isprintable() and len(name_text) < 12:
                    name_text += event.unicode

        pygame.display.update()
        await asyncio.sleep(0)  # required for the browser

    pygame.quit()


asyncio.run(main())