import sys
import os
import pygame
import time

from settings import Settings
from ship import Ship

#先清屏
os.system("cls")

print("开始游戏！")
def run_game():
    # 初始化游戏并创建一个屏幕对象
    pygame.init()
    pygame.display.set_caption("Alien Invasion")

    ai_settings =Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
    screen.fill(ai_settings.bg_color)

    ship= Ship(screen)
    ship.blitme()
    pygame.display.flip()

    # 开始游戏的主循环
    while True:
        #监视键盘和鼠标事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

run_game()