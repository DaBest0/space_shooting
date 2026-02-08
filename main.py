#Create your own shooter
from pygame import *
from Sprite_class import GameSprite, player, Bullet
from random import randint
width = 700
height = 500
background = transform.scale(image.load('galaxy.jpg'), (width, height))

miss = 0
score = 0
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global miss
        if self.rect.y >= 500:
            self.rect.y = 0
            self.rect.x = randint(0,650)
            self.speed = randint(1,2)
            miss += 1
        #elif sprite.groupcollide(ufo, Bullet, True, False):
            #score += 1
            #ufo.kill()
            #Bullet.kill()
   



''' window '''
window = display.set_mode( (width, height) )

clock = time.Clock()

'''Sprite'''
Players = player(filename='rocket.png', x=100, y=410, width=75, height=90, speed=3)
#Players = player(filename='TheWorld.png', x=100, y=410, width=75, height=90, speed=3)
#UFO = Enemy(filename='ufo.png', x=100, y=0, width=60, height=60, speed=3)
enemy_group = sprite.Group()
for i in range(5):
    ufo = Enemy(filename='ufo.png', 
                  x=randint(0,640), y=0,
                  width=60,height=30, 
                  speed=randint(1,2))
    enemy_group.add(ufo)
    
ast_group = sprite.Group()
for i in range(3):
    ast = Enemy(filename='asteroid.png', 
                  x=randint(0,640), y=0,
                  width=60,height=30, 
                  speed=randint(1,2))
    ast_group.add(ast)


font.init()
style = font.Font(None, 36)
win_lose_style = font.Font(None, 100)
mixer.init()
fire = mixer.Sound('fire.ogg')



''''game loop'''

Run = True
Gaming = True
while Run:
    if Gaming == True:
        window.blit(background, (0,0))
        Players.reset(win=window)
        Players.update(width, height)
        txt_missing_ufo = style.render( "Missed: "+str(miss), 1, (255,255,255) )
        window.blit(txt_missing_ufo, (5,5) )
        txt_scoring_ufo = style.render( "Score: "+str(score), 1, (255,255,255) )
        window.blit(txt_scoring_ufo, (5,30) )
        txt_Lose = win_lose_style.render("You Lose" ,1, (255,0,0) )
        txt_Win = win_lose_style.render("You Win" ,1, (0,255,0) )
        #UFO.reset(win=window)
        #UFO.update(width, height)
        enemy_group.draw(window)
        enemy_group.update()
        ast_group.draw(window)
        ast_group.update()
    
        Players.bullet_group.draw(window)
        Players.bullet_group.update()

        sprites_lists = sprite.groupcollide(
        enemy_group, Players.bullet_group, True, True
        )
        Player_ufo = sprite.spritecollide(
        Players, enemy_group, False
        )
        ast_bullet = sprite.groupcollide(
        ast_group, Players.bullet_group, False, True
        )
        ast_player = sprite.spritecollide(
        Players, ast_group, False
        )
        if sprites_lists:
            score += 1
            ufo = Enemy(filename='ufo.png', 
                          x=randint(0,640), y=0,
                          width=60,height=30, 
                          speed=randint(1,2))
            enemy_group.add(ufo)
        if Player_ufo:
            window.blit(txt_Lose, (200,250))
            Gaming = False
        elif ast_player:
            window.blit(txt_Lose, (200,250))
            Gaming = False
        elif miss >= 10:
            window.blit(txt_Lose, (200,250))
            Gaming = False
        elif score >= 10:
            window.blit(txt_Win, (230,250))
            Gaming = False

    else:
        time.delay(3000)
        for ufo in enemy_group:
            ufo.kill()
        for ast in ast_group:
            ast.kill()
        for bullet in Players.bullet_group:
            bullet.kill()
        
        for i in range(5):
            ufo = Enemy(filename='ufo.png', 
                          x=randint(0,640), y=0,
                          width=60,height=30, 
                          speed=randint(1,2))
            enemy_group.add(ufo)
        
        for i in range(3):
            ast = Enemy(filename='asteroid.png', 
                          x=randint(0,640), y=0,
                          width=60,height=60, 
                          speed=randint(1,2))
            ast_group.add(ast)
        
        Players.kill()
        Players = player(filename='rocket.png', x=100, y=410, width=75, height=90, speed=3)
        
        score = 0
        miss = 0


        Gaming = True
    
        
    for e in event.get():
        if e.type == QUIT:
            Run = False
        
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                Players.shoot()
                fire.play()
    
    display.update()
    clock.tick(60)
