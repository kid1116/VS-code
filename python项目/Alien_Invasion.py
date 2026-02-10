import os
import pygame
from pygame.sprite import Group

import game_functions as gf
from settings import Settings
from ship import Ship
from alien import Alien

#先清屏
os.system("cls")
print("开始游戏！(按Q键退出)")

def run_game():
    pygame.init()
    pygame.display.set_caption("Alien Invasion")

    ai_settings =Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
<<<<<<< HEAD
    ship = Ship(ai_settings,screen)     
=======
    ship = Ship(ai_settings,screen)
>>>>>>> 57bcecc858ffb1f1e4577bf232890b180e48df71
    bullets = Group() #创建子弹编组

    alien = Alien(ai_settings,screen)
    aliens =Group() #创建外星人编组
    gf.create_fleet(ai_settings,screen,ship,aliens)

    #游戏主循环
    while True:
        gf.check_events(ai_settings,screen,ship,bullets) 
        ship.update()
        gf.update_bullets(bullets)
<<<<<<< HEAD
        gf.update_aliens(aliens)
        gf.update_screen(ai_settings,screen,ship,bullets,aliens)
        
=======
        gf.update_screen(ai_settings,screen,ship,bullets,aliens)
>>>>>>> 57bcecc858ffb1f1e4577bf232890b180e48df71
        
run_game()