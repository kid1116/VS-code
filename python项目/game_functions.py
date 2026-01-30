import sys
import pygame
#监视键盘和鼠标事件
def check_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()