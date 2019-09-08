import pygame as pg, random, math, time
from os import path
from settings import *
from sprites import *

class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()

        self.screen = pg.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        pg.display.set_caption(TITLE)
        
        self.clock = pg.time.Clock()
        self.running = True
        self.playing = False

        self.img_dir = path.join(path.dirname(__file__), 'img')
        self.snd_dir = path.join(path.dirname(__file__), 'snd')

        self.soundhit = pg.mixer.Sound(path.join(self.snd_dir, "Clang_and_wobble.wav"))  #碰到磚塊音效
        self.soundpad = pg.mixer.Sound(path.join(self.snd_dir,"Stones_and_Water_On_Cement.wav"))  #碰到滑板音效
        self.score = 0  #得分

    def draw_text(self, text, size, color, x, y):
        font = pg.font.SysFont('SimHei', size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quitgame()

    def update(self):
        self.allsprite.update() 

        if self.score == 54:  #得分為54，亦即打到的磚塊數為54(所有磚塊)。
            self.draw_text("Congratulations!!", 60, RED, DISPLAY_WIDTH/2, DISPLAY_HEIGHT/2 - 100)
            pg.display.update()  #更新畫面
            time.sleep(2)        #暫停2秒
            self.game_intro()    #回到game_intro畫面

    def quitgame(self):
        pg.quit()
        quit()

    def draw(self):
        self.screen.fill(WHITE)
        self.allsprite.draw(self.screen)
        pg.display.update() #pg.display.flip()

    def new(self):
        self.intro = False
        self.playing = True

        self.allsprite = pg.sprite.Group()  #建立全部角色群組
        self.bricks = pg.sprite.Group()     #建立磚塊角色群組

        self.ball = Ball(self)         #建立綠球
        self.pad = Pad(self)           #建立滑板
        self.allsprite.add(self.ball)  #加入全部角色群組
        self.allsprite.add(self.pad)   #加入全部角色群組

        #(初始)建立磚塊
        cur_x = 8 
        cur_y = 8
        BLOCK_X_GAP = 18
        BLOCK_Y_GAP = 15
        for row in range(0, 6):          #6列方塊
            cur_x = 8
            for column in range(0, 9):   #每列9磚塊
                brick = Brick(self, column * 70 + cur_x, row * 28 + cur_y)   #位置 
                self.bricks.add(brick)     #加入磚塊角色群組
                self.allsprite.add(brick)  #加入全部角色群組
                cur_x += BLOCK_X_GAP
            cur_y += BLOCK_Y_GAP    

    #結束程式
    def gameover(self): 
        self.playing = False
        #顯示gg_img
        self.gg_img = pg.image.load(path.join(self.img_dir, 'expressionless-emoji.png')).convert()
        self.gg_img = pg.transform.scale(self.gg_img, (100, 100))
        self.gg_img.set_colorkey(WHITE)
        self.gg_img_rect = self.gg_img.get_rect()
        self.gg_img_rect.x = 350
        self.gg_img_rect.y = 400
        self.screen.blit(self.gg_img, self.gg_img_rect)
        #顯示訊息
        self.draw_text("You failed !", 35, BLACK, DISPLAY_WIDTH/2, DISPLAY_HEIGHT/2)
        self.draw_text("你打爆 {} 個磚塊！還剩下 {} 個磚塊。".format(str(self.score), str(54 - self.score)), 20, BLACK, DISPLAY_WIDTH/2, DISPLAY_HEIGHT-30)
        pg.display.update()  #更新畫面
        time.sleep(2)        #暫停2秒
        self.game_intro()
           
    def run(self):
        while self.playing:
            self.events()
            self.update()
            self.collision_check()
            self.draw()
            self.clock.tick(FPS)

    def collision_check(self):        
        #檢查球和磚塊碰撞
        self.ball_hit_brick = pg.sprite.spritecollide(self.ball, self.bricks, True)
        if len(self.ball_hit_brick) > 0:            #球和磚塊發生碰撞
            self.score += len(self.ball_hit_brick)  #計算分數
            self.soundhit.play()    #球撞磚塊聲
            self.ball.rect.y += 20  #球向下移
            self.ball.bounceup()    #球反彈
            
        #檢查球和滑板碰撞
        self.ball_hit_pad = pg.sprite.collide_rect(self.ball, self.pad)  
        if self.ball_hit_pad:       #球和滑板發生碰撞
            self.soundpad.play()    #球撞滑板聲
            self.ball.bounceup()    #球反彈

        if(self.ball.rect.bottom >= DISPLAY_HEIGHT - 10):  #球到達下邊界出界
            self.gameover()

    def game_intro(self):
        self.intro = True
        self.intro_background = pg.image.load(path.join(self.img_dir, 'bg.jpg')).convert()
        self.intro_background_rect = self.intro_background.get_rect()
        
        while self.intro:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.quitgame()
            self.screen.blit(self.intro_background, self.intro_background_rect)
            self.draw_text("打磚塊遊戲!", 80, BLUE, 400, 200)
            self.button("Start", 200, 450, 150, 50, RED, LIGHT_RED, action=self.new)
            self.button("Quit", 450, 450, 150, 50, GREEN, LIGHT_GREEN, action=self.quitgame)
            pg.display.update()
            self.clock.tick(FPS)

    def button(self, text, posX, posY, width, height, inActiveColor, activeColor, action=None):
        mouse = pg.mouse.get_pos()
        click = pg.mouse.get_pressed() 
        if (mouse[0] > posX and mouse[0] < posX+width) and (mouse[1] > posY and mouse[1] < posY+height):
            pg.draw.rect(self.screen, activeColor, (posX, posY, width, height))
            if click[0] == 1 and action != None:
                action()
        else:
            pg.draw.rect(self.screen, inActiveColor, (posX, posY, width, height))
        self.draw_text(text, 25, YELLOW, posX+(width/2), posY+(height/2)-15)

game = Game()
game.game_intro()
while game.running:
    game.run()
    game.game_intro()