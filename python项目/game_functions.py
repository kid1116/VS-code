import sys
import pygame

#更新屏幕
def update_screen(ai_settings,screen,ship):
    screen.fill(ai_settings.bg_color)
    ship.blitme()
    pygame.display.flip()

#响应键盘和鼠标事件
def check_events(ship):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        
        elif event.type == pygame.KEYDOWN: #按下键盘
            if event.key == pygame.K_RIGHT:
                ship.moving_right = True

        elif event.type == pygame.KEYUP: #松开键盘
            if event.key == pygame.K_RIGHT:
                ship.moving_right = False
           


