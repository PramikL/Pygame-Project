import random
import sys
import pygame
from pygame.locals import *

FPS = 40
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
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
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
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
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
            SCREEN.blit(GAME_IMAGES["numbers"][digit], (Xoffset, SCREENHEIGHT * 0.12))
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
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
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


def main():
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

    GAME_IMAGES["message"] = pygame.image.load("all/images/message.png").convert_alpha()
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
