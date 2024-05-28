import pygame
import sys
import os
from pygame.locals import*


pygame.init()


WIDTH, HEIGHT = 1200, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('The Game')

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


background = pygame.image.load('back.png')
    
background = pygame.transform.scale(background, (WIDTH, HEIGHT))



font = pygame.font.Font(None, 35)


option1_text = font.render('Space War', True, WHITE)
option2_text = font.render('Flappy Bird', True, WHITE)


option1_rect = option1_text.get_rect(center=(WIDTH // 4, HEIGHT // 1 - 200))
option2_rect = option2_text.get_rect(center=(WIDTH //1.35, HEIGHT // 1 - 200))

def flappy():
    
 import random
 import sys
 import pygame

 FPS = 35
 FPSCLOCK = pygame.time.Clock()
 SCREENWIDTH = 400
 SCREENHEIGHT = 511
 SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
 GROUNDY = SCREENHEIGHT * 0.82
 GAME_IMAGES = {}
 GAME_SOUNDS = {}
 PLAYER = 'all/images/bird.png'
 BACKGROUND = 'all/images/background.png'
 PIPE = 'all/images/pipe.png'


 def welcomeScreen():

    playerx = int(SCREENWIDTH/5)
    playery = int((SCREENHEIGHT - GAME_IMAGES['player'].get_height())/2)
    messagex = int((SCREENWIDTH - GAME_IMAGES['message'].get_width())/2)
    messagey = int(SCREENHEIGHT*0.05)
    basex = 0
    while True:
        for event in pygame.event.get():

            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            else:
                SCREEN.blit(GAME_IMAGES['background'], (0, 0))
                SCREEN.blit(GAME_IMAGES['player'], (playerx, playery))
                SCREEN.blit(GAME_IMAGES['message'], (messagex, messagey))
                SCREEN.blit(GAME_IMAGES['base'], (basex, GROUNDY))
                pygame.display.update()
                FPSCLOCK.tick(FPS)



 def mainGame():
    score = 0
    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENWIDTH/2)
    basex = 0

    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    upperPipes = [
        {'x': SCREENWIDTH+150, 'y': newPipe1[0]['y']},
        {'x': SCREENWIDTH+150+(SCREENWIDTH/2), 'y': newPipe2[0]['y']},
    ]

    lowerPipes = [
        {'x': SCREENWIDTH+150, 'y': newPipe1[1]['y']},
        {'x': SCREENWIDTH+150+(SCREENWIDTH/2), 'y': newPipe2[1]['y']},
    ]

    pipeVelX = -4

    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1

    playerFlapAccv = -8
    playerFlapped = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVelY = playerFlapAccv
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()

        crashTest = isCollide(playerx, playery, upperPipes, lowerPipes)
        if crashTest:
            return

        playerMidPos = playerx + GAME_IMAGES['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_IMAGES['pipe'][0].get_width()/2
            if pipeMidPos <= playerMidPos < pipeMidPos + 2:
                score += 1
                
                GAME_SOUNDS['point'].play()

        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped = False
        playerHeight = GAME_IMAGES['player'].get_height()
        playery = playery + min(playerVelY, GROUNDY - playery - playerHeight)

        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        if 0 < upperPipes[0]['x'] < 5:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

        if upperPipes[0]['x'] < -GAME_IMAGES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        SCREEN.blit(GAME_IMAGES['background'], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAME_IMAGES['pipe'][0],
                        (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(GAME_IMAGES['pipe'][1],
                        (lowerPipe['x'], lowerPipe['y']))

        SCREEN.blit(GAME_IMAGES['base'], (basex, GROUNDY))
        SCREEN.blit(GAME_IMAGES['player'], (playerx, playery))
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += GAME_IMAGES['numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH - width)/2

        for digit in myDigits:
            SCREEN.blit(GAME_IMAGES['numbers'][digit],
                        (Xoffset, SCREENHEIGHT*0.12))
            Xoffset += GAME_IMAGES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)


 def isCollide(playerx, playery, upperPipes, lowerPipes):
    if playery > GROUNDY - GAME_IMAGES['player'].get_height() or playery < 0:
        GAME_SOUNDS['hit'].play()
        return True

    player_rect = pygame.Rect(playerx, playery, GAME_IMAGES['player'].get_width(), GAME_IMAGES['player'].get_height())

    for pipe in upperPipes + lowerPipes:
        pipe_rect = pygame.Rect(pipe['x'], pipe['y'], GAME_IMAGES['pipe'][0].get_width(), GAME_IMAGES['pipe'][0].get_height())
        if player_rect.colliderect(pipe_rect):
            GAME_SOUNDS['hit'].play()
            return True

    return False


 def getRandomPipe():

    pipeHeight = GAME_IMAGES['pipe'][0].get_height()
    offset = SCREENHEIGHT/2.5
    y2 = offset + random.randrange(0, int(SCREENHEIGHT -
                                   GAME_IMAGES['base'].get_height() - 1.2 * offset))
    pipeX = SCREENWIDTH + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipeX, 'y': -y1},
        {'x': pipeX, 'y': y2}
    ]
    return pipe



 if __name__ == "__main__":

    pygame.init()

    pygame.display.set_caption('Flappy Bird')
    GAME_IMAGES['numbers'] = (
        pygame.image.load('all/images/0.png').convert_alpha(),
        pygame.image.load('all/images/1.png').convert_alpha(),
        pygame.image.load('all/images/2.png').convert_alpha(),
        pygame.image.load('all/images/3.png').convert_alpha(),
        pygame.image.load('all/images/4.png').convert_alpha(),
        pygame.image.load('all/images/5.png').convert_alpha(),
        pygame.image.load('all/images/6.png').convert_alpha(),
        pygame.image.load('all/images/7.png').convert_alpha(),
        pygame.image.load('all/images/8.png').convert_alpha(),
        pygame.image.load('all/images/9.png').convert_alpha(),
    )

    GAME_IMAGES['message'] = pygame.image.load(
        'all/images/message.png').convert_alpha()
    GAME_IMAGES['base'] = pygame.image.load(
        'all/images/base.png').convert_alpha()
    GAME_IMAGES['pipe'] = (pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180),
                           pygame.image.load(PIPE).convert_alpha()
                           )


    GAME_SOUNDS['die'] = pygame.mixer.Sound('all/audio//die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('all/audio//hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('all/audio//point.mp3')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('all/audio//swoosh.mp3')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('all/audio//wing.mp3')

    GAME_IMAGES['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_IMAGES['player'] = pygame.image.load(PLAYER).convert_alpha()

    while True:
        welcomeScreen()
        mainGame()



def spacegame():

 import pygame
 import os

 pygame.font.init()
 pygame.mixer.init()

 WIDTH, HEIGHT = 900, 600
 WIN = pygame.display.set_mode((WIDTH, HEIGHT))
 pygame.display.set_caption("Space war")

 WHITE = (255, 255, 255)
 BLACK = (0, 0, 0)
 RED = (255, 0, 0)
 YELLOW = (255, 255, 0) 

 BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT) 

 BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Grenade+1.mp3"))
 BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Gun+Silencer.mp3"))

 HEALTH_FONT = pygame.font.SysFont("comicsans", 40)
 WINNER_FONT = pygame.font.SysFont("comicscans", 100)

 FPS = 60
 VEL = 6
 BULLET_VEL = 15
 MAX_BULLETS = 30
 SPACESHIP_WIDTH, SPACE_HEIGHT = (55, 40)
 
 YELLOW_HIT = pygame.USEREVENT + 1
 RED_HIT = pygame.USEREVENT + 2
 
 YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join("Assets", "spaceship_yellow.png")
 )

 YELLOW_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACE_HEIGHT)), 90
 )

 RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join("Assets", "spaceship_red.png"))

 RED_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACE_HEIGHT)), 270
 )

 SPACE = pygame.transform.scale(
    pygame.image.load(os.path.join("Assets", "space.png")), (WIDTH, HEIGHT)
 )


 def start_screen():
    start_font = pygame.font.SysFont("comicsans", 60)
    text = start_font.render("Press any key to start", 1, WHITE)
    WIN.blit(
        text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2)
    )
    pygame.display.update()
    pygame.time.delay(1000)

    run_start = True
    while run_start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                run_start = False


 def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)
    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)
    pygame.display.update()


 def yellow_spaceship_movement_control(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:  # moves the spaceship left
        yellow.x -= VEL

    if (
        keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x
    ):  # moves the spaceship right
        yellow.x += VEL

    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:  # moves the spaceship up
        yellow.y -= VEL

    if (
        keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 20
    ):  # moves the spaceship down
        yellow.y += VEL


 def red_spaceship_movement_control(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:
        red.x -= VEL

    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH:
        red.x += VEL

    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:
        red.y -= VEL

    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 20:
        red.y += VEL


 def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)


 def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(
        draw_text,
        (
            WIDTH // 2 - draw_text.get_width() // 2,
            HEIGHT // 1.5 - draw_text.get_height() // 2,
        ),
    )
    pygame.display.update()
    pygame.time.delay(2000)


 def main():
    start_screen()
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACE_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACE_HEIGHT)

    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        yellow.x + yellow.width,
                        yellow.y + yellow.height // 2 - 2,
                        10,
                        5,
                    )
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height // 2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow Wins!!"

        if yellow_health <= 0:
            winner_text = "Red wins!!"
        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        yellow_spaceship_movement_control(keys_pressed, yellow)

        red_spaceship_movement_control(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)

    main()


 if __name__ == "__main__":
    main()

    


def run_option1():
    spacegame()
    

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill(RED)
        pygame.display.flip()

def run_option2():
    flappy()
      

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill(BLUE)
        pygame.display.flip()

def main_menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if option1_rect.collidepoint(mouse_pos):
                    run_option1()
                elif option2_rect.collidepoint(mouse_pos):
                    run_option2()

        screen.blit(background, (0, 0))
        screen.blit(option1_text, option1_rect)
        screen.blit(option2_text, option2_rect)
        pygame.display.flip()

# Run the main menu
main_menu()
