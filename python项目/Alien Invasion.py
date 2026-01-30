import sys
import os
import pygame

from settings import Settings

#先清屏
os.system("cls")

print("开始游戏！")
def run_game():
    # 初始化游戏并创建一个屏幕对象
    pygame.init()
    ai_settings =Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    #设置背景色(RGB)
    bg_color = ai_settings.bg_color
  
    # 开始游戏的主循环
    while True:
        #监视键盘和鼠标事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        #绘制屏幕颜色
        screen.fill(bg_color)

        #更新屏幕显示
        pygame.display.flip()
       
run_game()
