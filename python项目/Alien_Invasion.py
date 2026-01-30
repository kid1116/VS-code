import os
import pygame

import game_functions as gf
from settings import Settings
from ship import Ship

#先清屏
os.system("cls")
print("开始游戏！")

def run_game():
    pygame.init()
    pygame.display.set_caption("Alien Invasion")

    ai_settings =Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
    
    ship = Ship(screen)

    while True:
        gf.check_events(ship)
        ship.update()
        gf.update_screen(ai_settings,screen,ship)

run_game()