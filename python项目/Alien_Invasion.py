import os
import pygame

import game_functions as gf
from settings import Settings
from ship import Ship
from pygame.sprite import Group

#先清屏
os.system("cls")
print("开始游戏！")

def run_game():
    pygame.init()
    pygame.display.set_caption("Alien Invasion")

    ai_settings =Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
    ship = Ship(ai_settings,screen)

    bullets = Group() #创建子弹编组

    #游戏主循环
    while True:
        gf.check_events(ai_settings,screen,ship,bullets)
        ship.update()
        bullets.update()
        gf.update_screen(ai_settings,screen,ship,bullets)

run_game()