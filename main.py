import pygame
import sys
from pygame.locals import *

# Initialize Pygame
pygame.init()
pygame.font.init()
pygame.mixer.init()

# Screen settings
WIDTH, HEIGHT = 900, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Selector")

background = pygame.image.load("back.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Fonts
FONT = pygame.font.SysFont("comicsans", 40)
TITLE_FONT = pygame.font.SysFont("comicsans", 60)


# Functions to load and run the games
def run_space_game():
    import space_game  # Assuming the space game code is in a module named space_game

    space_game.main()


def run_flappy_bird():
    import flappy_bird  # Assuming the Flappy Bird game code is in a module named flappy_bird

    flappy_bird.main()


def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


def game_selector():
    while True:
        SCREEN.fill(BLACK)
        draw_text(
            "Choose Your Game", TITLE_FONT, WHITE, SCREEN, WIDTH // 4, HEIGHT // 4
        )
        draw_text("1. Space War", FONT, WHITE, SCREEN, WIDTH // 3, HEIGHT // 2)
        draw_text("2. Flappy Bird", FONT, WHITE, SCREEN, WIDTH // 3, HEIGHT // 2 + 50)
        draw_text(
            "Press 1 or 2 to choose", FONT, WHITE, SCREEN, WIDTH // 4, HEIGHT // 2 + 100
        )

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_1:
                    run_space_game()
                elif event.key == K_2:
                    run_flappy_bird()


if __name__ == "__main__":
    game_selector()
