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

        GAME_SOUNDS["die"] = pygame.mixer.Sound("all/audio/die.wav")
        GAME_SOUNDS["hit"] = pygame.mixer.Sound("all/audio/hit.wav")
        GAME_SOUNDS["point"] = pygame.mixer.Sound("all/audio/point.mp3")
        GAME_SOUNDS["swoosh"] = pygame.mixer.Sound("all/audio/swoosh.mp3")
        GAME_SOUNDS["wing"] = pygame.mixer.Sound("all/audio/wing.mp3")

        GAME_IMAGES["background"] = pygame.image.load(BACKGROUND).convert()
        GAME_IMAGES["player"] = pygame.image.load(PLAYER).convert_alpha()

        while True:
            welcomeScreen()
            mainGame()


def space_war():
    import random
    import pygame
    from pygame import mixer

    pygame.init()

    screen = pygame.display.set_mode((800, 600))

    pygame.display.set_caption("Space War")
    icon = pygame.image.load("game/img/ufo.png")
    pygame.display.set_icon(icon)

    playerImg = pygame.image.load("game/img/player.png")
    playerX = 370
    playerY = 480
    playerX_change = 0

    enemyImg = []
    enemyX = []
    enemyY = []
    enemyX_change = []
    enemyY_change = []
    num_of_enemies = 6

    for i in range(num_of_enemies):
        enemyImg.append(pygame.image.load("game/img/enemy.png"))
        enemyX.append(random.randint(0, 735))
        enemyY.append(random.randint(50, 150))
        enemyX_change.append(4)
        enemyY_change.append(40)

    bulletImg = pygame.image.load("game/img/bullet.png")
    bulletX = 0
    bulletY = 480
    bulletX_change = 0
    bulletY_change = 10
    bullet_state = "ready"

    score_value = 0
    font = pygame.font.Font("freesansbold.ttf", 32)

    textX = 10
    textY = 10

    over_font = pygame.font.Font("freesansbold.ttf", 64)

    def show_score(x, y):
        score = font.render("Score : " + str(score_value), True, (255, 255, 255))
        screen.blit(score, (x, y))

    def game_over_text():
        over_text = over_font.render("GAME OVER", True, (255, 255, 255))
        screen.blit(over_text, (200, 250))

    def player(x, y):
        screen.blit(playerImg, (x, y))

    def enemy(x, y, i):
        screen.blit(enemyImg[i], (x, y))

    def fire_bullet(x, y):
        global bullet_state
        bullet_state = "fire"
        screen.blit(bulletImg, (x + 16, y + 10))

    def isCollision(enemyX, enemyY, bulletX, bulletY):
        distance = ((enemyX - bulletX) ** 2 + (enemyY - bulletY) ** 2) ** 0.5
        if distance < 27:
            return True
        else:
            return False

    running = True
    while running:
        screen.fill((0, 0, 0))
        background = pygame.image.load("game/img/background.png")
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_change = -5
                if event.key == pygame.K_RIGHT:
                    playerX_change = 5
                if event.key == pygame.K_SPACE:
                    if bullet_state == "ready":
                        bulletX = playerX
                        fire_bullet(bulletX, bulletY)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0

        playerX += playerX_change
        if playerX <= 0:
            playerX = 0
        elif playerX >= 736:
            playerX = 736

        for i in range(num_of_enemies):

            if enemyY[i] > 440:
                for j in range(num_of_enemies):
                    enemyY[j] = 2000
                game_over_text()
                break

            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = 4
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 736:
                enemyX_change[i] = -4
                enemyY[i] += enemyY_change[i]

            collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
            if collision:
                bulletY = 480
                bullet_state = "ready"
                score_value += 1
                enemyX[i] = random.randint(0, 735)
                enemyY[i] = random.randint(50, 150)

            enemy(enemyX[i], enemyY[i], i)

        if bulletY <= 0:
            bulletY = 480
            bullet_state = "ready"

        if bullet_state == "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change

        player(playerX, playerY)
        show_score(textX, textY)
        pygame.display.update()


def main():
    while True:
        screen.blit(background, (0, 0))
        screen.blit(option1_text, option1_rect)
        screen.blit(option2_text, option2_rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if option1_rect.collidepoint(event.pos):
                    space_war()
                elif option2_rect.collidepoint(event.pos):
                    flappy()


if __name__ == "__main__":
    main()
