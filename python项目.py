import sys

import pygame

def run_game():
    # Initialize the game and create a screen object
    pygame.init()
    screen = pygame.display.set_mode((1200,800))
    pygame.display.set_caption("Simple Pygame Example")

    # Main loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        # Fill the screen with a color (RGB)
        screen.fill((250,245,230))

        # Update the display
        pygame.display.flip()

run_game()