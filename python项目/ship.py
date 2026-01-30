import pygame

class Ship():
    def __init__(self,screen):
        self.screen=screen 

        self.image=pygame.image.load('D:\VS code\python项目\ship.bmp')
        self.rect=self.image.get_rect()
        self.screen_rect=screen.get_rect()

        self.rect.centerx=self.screen_rect.centerx
        self.rect.bottom=self.screen_rect.bottom

        #移动标志
        self.moving_right=False

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.rect.centerx +=1

    def blitme(self):
        self.screen.blit(self.image,self.rect)