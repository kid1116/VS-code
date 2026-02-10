import sys
import pygame
from bullet import Bullet
from alien import Alien

#按下键盘
def check_keydown_events(event,ai_settings,screen,ship,bullets):
    if event.key == pygame.K_RIGHT:
         ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left =True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings,screen,ship,bullets)
    elif event.key == pygame.K_q:
        sys.exit()

#松开键盘
def check_keyup_events(event,ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
           
#响应键盘和鼠标事件
def check_events(ai_settings,screen,ship,bullets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT :
            sys.exit()
        elif event.type == pygame.KEYDOWN: #按下键盘
            check_keydown_events(event,ai_settings,screen,ship,bullets)
        elif event.type == pygame.KEYUP: #松开键盘
            check_keyup_events(event,ship)

#更新屏幕
def update_screen(ai_settings,screen,ship,bullets,aliens):
    screen.fill(ai_settings.bg_color)

    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)

    #让最近绘制的屏幕可见
    pygame.display.flip()

#删除已消失的子弹
def update_bullets(bullets):
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <=0:
            bullets.remove(bullet)

#发射子弹检查
def fire_bullet(ai_settings,screen,ship,bullets):
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings,screen,ship)
        bullets.add(new_bullet)

#创建外星人群
def create_fleet(ai_settings,screen,ship,aliens):
    alien = Alien(ai_settings,screen)
    number_aliens_x = get_number_aliens_x(ai_settings,alien.rect.width)
    number_rows = get_number_rows(ai_settings,ship.rect.height,alien.rect.height)
    #创建第一行外星人
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings,screen,aliens,alien_number,row_number)

#创建单个外星人并加入群组
def create_alien(ai_settings,screen,aliens,alien_number,row_number):
    alien = Alien(ai_settings,screen)
    alien_width = alien.rect.width
    alien.rect.x = alien_width + 2 * alien_width * alien_number
    alien.rect.y = alien.rect.height + 2*alien.rect.height*row_number
    aliens.add(alien)

#计算每行可容纳的外星人数量
def get_number_aliens_x(ai_settings,alien_width):
    available_space_x = ai_settings.screen_width - (2 * alien_width)
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

#计算可以容纳多少行外星人
def get_number_rows(ai_settings,ship_height,alien_height):
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows
<<<<<<< HEAD

#外星人移动
def update_aliens(aliens):
    aliens.update()
=======
    
>>>>>>> 57bcecc858ffb1f1e4577bf232890b180e48df71
