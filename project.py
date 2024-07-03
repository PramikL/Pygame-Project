import pygame
import sys
import os
import random
from pygame.locals import *

pygame.init()

WIDTH, HEIGHT = 1200, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("The Game")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

background = pygame.image.load("back.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

font = pygame.font.Font(None, 35)

option1_text = font.render("Space War", True, WHITE)
option2_text = font.render("Flappy Bird", True, WHITE)

option1_rect = option1_text.get_rect(center=(WIDTH // 4, HEIGHT // 1 - 200))
option2_rect = option2_text.get_rect(center=(WIDTH // 1.35, HEIGHT // 1 - 200))


def flappy():
    FPS = 37
    FPSCLOCK = pygame.time.Clock()
    SCREENWIDTH = 400
    SCREENHEIGHT = 511
    SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    GROUNDY = SCREENHEIGHT * 0.82
    GAME_IMAGES = {}
    GAME_SOUNDS = {}
    PLAYER = "all/images/bird.png"
    BACKGROUND = "all/images/background.png"
    PIPE = "all/images/pipe.png"

    def welcomeScreen():
        playerx = int(SCREENWIDTH / 5)
        playery = int((SCREENHEIGHT - GAME_IMAGES["player"].get_height()) / 2)
        messagex = int((SCREENWIDTH - GAME_IMAGES["message"].get_width()) / 2)
        messagey = int(SCREENHEIGHT * 0.05)
        basex = 0
        while True:
            for event in pygame.event.get():
                if event.type == QUIT or (
                    event.type == KEYDOWN and event.key == K_ESCAPE
                ):
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN and (
                    event.key == K_SPACE or event.key == K_UP
                ):
                    return
                else:
                    SCREEN.blit(GAME_IMAGES["background"], (0, 0))
                    SCREEN.blit(GAME_IMAGES["player"], (playerx, playery))
                    SCREEN.blit(GAME_IMAGES["message"], (messagex, messagey))
                    SCREEN.blit(GAME_IMAGES["base"], (basex, GROUNDY))
                    pygame.display.update()
                    FPSCLOCK.tick(FPS)

    def mainGame():
        score = 0
        playerx = int(SCREENWIDTH / 5)
        playery = int(SCREENWIDTH / 2)
        basex = 0

        newPipe1 = getRandomPipe()
        newPipe2 = getRandomPipe()

        upperPipes = [
            {"x": SCREENWIDTH + 150, "y": newPipe1[0]["y"]},
            {"x": SCREENWIDTH + 150 + (SCREENWIDTH / 2), "y": newPipe2[0]["y"]},
        ]

        lowerPipes = [
            {"x": SCREENWIDTH + 150, "y": newPipe1[1]["y"]},
            {"x": SCREENWIDTH + 150 + (SCREENWIDTH / 2), "y": newPipe2[1]["y"]},
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
                if event.type == QUIT or (
                    event.type == KEYDOWN and event.key == K_ESCAPE
                ):
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN and (
                    event.key == K_SPACE or event.key == K_UP
                ):
                    if playery > 0:
                        playerVelY = playerFlapAccv
                        playerFlapped = True
                        GAME_SOUNDS["wing"].play()

            crashTest = isCollide(playerx, playery, upperPipes, lowerPipes)
            if crashTest:
                displayTryAgain()
                return

            playerMidPos = playerx + GAME_IMAGES["player"].get_width() / 2
            for pipe in upperPipes:
                pipeMidPos = pipe["x"] + GAME_IMAGES["pipe"][0].get_width() / 2
                if pipeMidPos <= playerMidPos < pipeMidPos + 2:
                    score += 1
                    print(f"Your score is {score}")
                    GAME_SOUNDS["point"].play()

            if playerVelY < playerMaxVelY and not playerFlapped:
                playerVelY += playerAccY

            if playerFlapped:
                playerFlapped = False
            playerHeight = GAME_IMAGES["player"].get_height()
            playery = playery + min(playerVelY, GROUNDY - playery - playerHeight)

            if playery >= GROUNDY - playerHeight:
                playery = GROUNDY - playerHeight
                GAME_SOUNDS["hit"].play()
                displayTryAgain()
                return

            for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
                upperPipe["x"] += pipeVelX
                lowerPipe["x"] += pipeVelX

            if 0 < upperPipes[0]["x"] < 5:
                newpipe = getRandomPipe()
                upperPipes.append(newpipe[0])
                lowerPipes.append(newpipe[1])

            if upperPipes[0]["x"] < -GAME_IMAGES["pipe"][0].get_width():
                upperPipes.pop(0)
                lowerPipes.pop(0)

            SCREEN.blit(GAME_IMAGES["background"], (0, 0))
            for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
                SCREEN.blit(GAME_IMAGES["pipe"][0], (upperPipe["x"], upperPipe["y"]))
                SCREEN.blit(GAME_IMAGES["pipe"][1], (lowerPipe["x"], lowerPipe["y"]))

            SCREEN.blit(GAME_IMAGES["base"], (basex, GROUNDY))
            SCREEN.blit(GAME_IMAGES["player"], (playerx, playery))
            myDigits = [int(x) for x in list(str(score))]
            width = 0
            for digit in myDigits:
                width += GAME_IMAGES["numbers"][digit].get_width()
            Xoffset = (SCREENWIDTH - width) / 2

            for digit in myDigits:
                SCREEN.blit(
                    GAME_IMAGES["numbers"][digit], (Xoffset, SCREENHEIGHT * 0.12)
                )
                Xoffset += GAME_IMAGES["numbers"][digit].get_width()
            pygame.display.update()
            FPSCLOCK.tick(FPS)

    def isCollide(playerx, playery, upperPipes, lowerPipes):
        if playery > GROUNDY - GAME_IMAGES["player"].get_height() or playery < 0:
            GAME_SOUNDS["hit"].play()
            return True

        player_rect = pygame.Rect(
            playerx,
            playery,
            GAME_IMAGES["player"].get_width(),
            GAME_IMAGES["player"].get_height(),
        )

        for pipe in upperPipes + lowerPipes:
            pipe_rect = pygame.Rect(
                pipe["x"],
                pipe["y"],
                GAME_IMAGES["pipe"][0].get_width(),
                GAME_IMAGES["pipe"][0].get_height(),
            )
            if player_rect.colliderect(pipe_rect):
                GAME_SOUNDS["hit"].play()
                return True

        return False

    def displayTryAgain():
        font = pygame.font.Font("freesansbold.ttf", 32)
        text = font.render("Try Again", True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (SCREENWIDTH // 2, SCREENHEIGHT // 2)
        SCREEN.blit(text, textRect)
        pygame.display.update()
        pygame.time.wait(1200)

        text = font.render("Press Space Key", True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (SCREENWIDTH // 2, SCREENHEIGHT // 2 + 50)
        SCREEN.blit(text, textRect)
        pygame.display.update()

        waitForSpaceKey()

    def waitForSpaceKey():
        while True:
            for event in pygame.event.get():
                if event.type == QUIT or (
                    event.type == KEYDOWN and event.key == K_ESCAPE
                ):
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN and event.key == K_SPACE:
                    return

    def getRandomPipe():
        pipeHeight = GAME_IMAGES["pipe"][0].get_height()
        offset = SCREENHEIGHT / 2.5
        y2 = offset + random.randrange(
            0, int(SCREENHEIGHT - GAME_IMAGES["base"].get_height() - 1.2 * offset)
        )
        pipeX = SCREENWIDTH + 10
        y1 = pipeHeight - y2 + offset
        pipe = [{"x": pipeX, "y": -y1}, {"x": pipeX, "y": y2}]
        return pipe

    if __name__ == "__main__":
        pygame.init()
        pygame.display.set_caption("Flappy Bird")
        GAME_IMAGES["numbers"] = (
            pygame.image.load("all/images/0.png").convert_alpha(),
            pygame.image.load("all/images/1.png").convert_alpha(),
            pygame.image.load("all/images/2.png").convert_alpha(),
            pygame.image.load("all/images/3.png").convert_alpha(),
            pygame.image.load("all/images/4.png").convert_alpha(),
            pygame.image.load("all/images/5.png").convert_alpha(),
            pygame.image.load("all/images/6.png").convert_alpha(),
            pygame.image.load("all/images/7.png").convert_alpha(),
            pygame.image.load("all/images/8.png").convert_alpha(),
            pygame.image.load("all/images/9.png").convert_alpha(),
        )

        GAME_IMAGES["message"] = pygame.image.load(
            "all/images/message.png"
        ).convert_alpha()
        GAME_IMAGES["base"] = pygame.image.load("all/images/base.png").convert_alpha()
        GAME_IMAGES["pipe"] = (
            pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180),
            pygame.image.load(PIPE).convert_alpha(),
        )
        GAME_IMAGES["background"] = pygame.image.load(BACKGROUND).convert()
        GAME_IMAGES["player"] = pygame.image.load(PLAYER).convert_alpha()

        GAME_SOUNDS["die"] = pygame.mixer.Sound("all/audio/die.wav")
        GAME_SOUNDS["hit"] = pygame.mixer.Sound("all/audio/hit.wav")
        GAME_SOUNDS["point"] = pygame.mixer.Sound("all/audio/point.wav")
        GAME_SOUNDS["swoosh"] = pygame.mixer.Sound("all/audio/swoosh.wav")
        GAME_SOUNDS["wing"] = pygame.mixer.Sound("all/audio/wing.wav")

        while True:
            welcomeScreen()
            mainGame()


def space_war():
    pygame.init()

    WIDTH, HEIGHT = 1200, 600
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Space War")

    # Load background image
    background_img = pygame.image.load("background1.png")

    # Load spaceship images
    spaceship_img1 = pygame.image.load("spaceship1.png")
    spaceship_img1 = pygame.transform.scale(spaceship_img1, (50, 50))

    spaceship_img2 = pygame.image.load("spaceship2.png")
    spaceship_img2 = pygame.transform.scale(spaceship_img2, (50, 50))

    # Load bullet image
    bullet_img = pygame.image.load("bullet.png")
    bullet_img = pygame.transform.scale(bullet_img, (10, 10))

    # Spaceship properties
    spaceship_width = 50
    spaceship_height = 50
    spaceship_speed = 5

    # Bullet properties
    bullet_speed = 7
    bullet_width = 10
    bullet_height = 10

    # Spaceship class
    class Spaceship:
        def __init__(self, x, y, image):
            self.x = x
            self.y = y
            self.image = image
            self.bullets = []

        def draw(self, win):
            win.blit(self.image, (self.x, self.y))
            for bullet in self.bullets:
                bullet.draw(win)

        def move_bullets(self, vel, height):
            for bullet in self.bullets:
                bullet.move(vel)
                if bullet.off_screen(height):
                    self.bullets.remove(bullet)

    # Bullet class
    class Bullet:
        def __init__(self, x, y, image):
            self.x = x
            self.y = y
            self.image = image

        def draw(self, win):
            win.blit(self.image, (self.x, self.y))

        def move(self, vel):
            self.y += vel

        def off_screen(self, height):
            return not (0 <= self.y <= height)

        def collision(self, obj):
            return collide(self, obj)

    def collide(obj1, obj2):
        offset_x = obj2.x - obj1.x
        offset_y = obj2.y - obj1.y
        return obj1.image.get_rect().colliderect(
            obj2.image.get_rect().move(offset_x, offset_y)
        )

    def draw_window(win, spaceship1, spaceship2, background_img):
        win.blit(background_img, (0, 0))
        spaceship1.draw(win)
        spaceship2.draw(win)
        pygame.display.update()

    def handle_movement(keys, spaceship1, spaceship2, width, height, speed):
        if keys[pygame.K_a] and spaceship1.x - speed > 0:
            spaceship1.x -= speed
        if (
            keys[pygame.K_d]
            and spaceship1.x + speed + spaceship1.image.get_width() < width
        ):
            spaceship1.x += speed
        if keys[pygame.K_w] and spaceship1.y - speed > 0:
            spaceship1.y -= speed
        if (
            keys[pygame.K_s]
            and spaceship1.y + speed + spaceship1.image.get_height() < height
        ):
            spaceship1.y += speed

        if keys[pygame.K_LEFT] and spaceship2.x - speed > 0:
            spaceship2.x -= speed
        if (
            keys[pygame.K_RIGHT]
            and spaceship2.x + speed + spaceship2.image.get_width() < width
        ):
            spaceship2.x += speed
        if keys[pygame.K_UP] and spaceship2.y - speed > 0:
            spaceship2.y -= speed
        if (
            keys[pygame.K_DOWN]
            and spaceship2.y + speed + spaceship2.image.get_height() < height
        ):
            spaceship2.y += speed

    def main():
        run = True
        clock = pygame.time.Clock()
        spaceship1 = Spaceship(100, 300, spaceship_img1)
        spaceship2 = Spaceship(1000, 300, spaceship_img2)

        while run:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LCTRL:
                        bullet = Bullet(
                            spaceship1.x
                            + spaceship1.image.get_width() // 2
                            - bullet_width // 2,
                            spaceship1.y,
                            bullet_img,
                        )
                        spaceship1.bullets.append(bullet)

                    if event.key == pygame.K_RCTRL:
                        bullet = Bullet(
                            spaceship2.x
                            + spaceship2.image.get_width() // 2
                            - bullet_width // 2,
                            spaceship2.y + spaceship2.image.get_height(),
                            bullet_img,
                        )
                        spaceship2.bullets.append(bullet)

            keys = pygame.key.get_pressed()
            handle_movement(
                keys, spaceship1, spaceship2, WIDTH, HEIGHT, spaceship_speed
            )

            spaceship1.move_bullets(-bullet_speed, HEIGHT)
            spaceship2.move_bullets(bullet_speed, HEIGHT)

            draw_window(win, spaceship1, spaceship2, background_img)

        pygame.quit()

    if __name__ == "__main__":
        main()


while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if option1_rect.collidepoint(mouse_pos):
                space_war()
            elif option2_rect.collidepoint(mouse_pos):
                flappy()

    screen.blit(background, (0, 0))
    pygame.draw.rect(screen, BLACK, option1_rect.inflate(10, 10), border_radius=5)
    pygame.draw.rect(screen, BLACK, option2_rect.inflate(10, 10), border_radius=5)
    screen.blit(option1_text, option1_rect)
    screen.blit(option2_text, option2_rect)
    pygame.display.update()
