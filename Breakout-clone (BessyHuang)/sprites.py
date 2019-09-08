import pygame as pg
from settings import *
import random, math

#球體
class Ball(pg.sprite.Sprite): 
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.speed = 5   #球移動速度
        self.x = 300     #初始x座標
        self.y = 350     #初始y座標
        self.color = GREEN
        self.image = pg.Surface([16, 16])   #繪製球體
        self.image.fill(WHITE)
        pg.draw.circle(self.image, self.color, (8,8), 8, 0)
        self.rect = self.image.get_rect()       #取得球體區域
        self.direction = random.randint(40,70)  #移動角度 #球移動方向

    #球體移動
    def update(self):         
        radian = math.radians(self.direction)    #角度轉為弳度
        self.dx = self.speed * math.cos(radian)  #球水平運動速度
        self.dy = -self.speed * math.sin(radian) #球垂直運動速度
        self.x += self.dx     #計算球新坐標
        self.y += self.dy
        self.rect.x = self.x  #移動球圖形
        self.rect.y = self.y
        
        if (self.rect.left <= 0 or self.rect.right >= DISPLAY_WIDTH - 10):  #到達左右邊界
            self.bouncelr()
        elif (self.rect.top <= 10):  #到達上邊界
            self.rect.top = 10
            self.bounceup()

    def bounceup(self):  #上邊界反彈
        self.direction = 360 - self.direction

    def bouncelr(self):  #左右邊界反彈
        self.direction = (180 - self.direction) % 360

    def draw(self):
        self.game.screen.blit(self.image, (self.x, self.y))

#磚塊
class Brick(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.Surface([80, 32])  #磚塊長寬
        self.brick_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.image.fill(self.brick_color)
        self.rect = self.image.get_rect()
        self.rect.x = x    #磚塊位置
        self.rect.y = y

    def draw(self):
        self.game.screen.blit(self.image, (self.rect.x, self.rect.y))

#滑板
class Pad(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.Surface([60, 15])  #滑板長寬
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = int((DISPLAY_WIDTH - self.rect.width)/2)  #滑板位置
        self.rect.y = DISPLAY_HEIGHT - self.rect.height - 30
    
    #滑板位置隨滑鼠移動 
    def update(self):  
        pos = pg.mouse.get_pos()  
        self.rect.x = pos[0]       #滑鼠x坐標
        #不要移出右邊界
        if self.rect.x > DISPLAY_WIDTH - self.rect.width:
            self.rect.x = DISPLAY_WIDTH - self.rect.width

    def draw(self):
        self.game.screen.blit(self.image, (self.rect.x, self.rect.y))