import sys
import os
import pygame
import time

from settings import Settings

#先清屏
os.system("cls")

print("开始游戏！")
def run_game():
    # 初始化游戏并创建一个屏幕对象
    pygame.init()
    pygame.display.set_caption("Alien Invasion")
    ai_settings =Settings()

    screen = pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
    screen_rect = screen.get_rect()

    image = pygame.image.load("D:\VS code\python项目\ship.bmp")
    ship_rect = image.get_rect()
    ship_rect.center = screen_rect.center

    screen.fill(ai_settings.bg_color)
    screen.blit(image, ship_rect)
    pygame.display.flip()
    
  
    # 开始游戏的主循环
    while True:
        #监视键盘和鼠标事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

run_game()
