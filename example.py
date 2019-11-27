import pygame, math
import sys
import time

pre_time = time.time()
pree_time = time.time()
pre2_time=time.time()
pre3_time=time.time()
pre4_time=time.time()
TEXTCOLOR = (255, 255, 255)


class Mundo:
    def __init__(self, x, y):
        self.health = 100
        self.strength = 100
        self.armor = 100
        self.healthregen = 0.02
        self.cooltime_limit = 0.2
        self.arrows = []
        self.spell1type = 1
        self.spell1cool = 3
        self.spell2type = 2
        self.spell2cool = 3
        self.spelllist=[0,"heal","flash", "ignite", "exhaust", "ghost"]
        self.speed=5
        self.x = x
        self.y = y

    def move(self, k0, k1, k2, k3,ty):  # wasd로 움직임
        if ty==1:
            if k0:
                if 23 <= self.y - self.speed <= 240 - 23:
                    self.y = self.y - self.speed
            elif k2:
                if 23 <= self.y + self.speed <= 240 - 23:
                    self.y = self.y + self.speed
        elif ty==2:
            if k0:
                if 240+23<=self.y-self.speed<=480-23:
                    self.y=self.y-self.speed
            elif k2:
                if 240+23<=self.y+self.speed<=480-23:
                    self.y=self.y+self.speed
        if k1:
            if 32 <= self.x - self.speed <= 640 - 32:
                self.x = self.x - self.speed
        elif k3:
            if 32 <= self.x + self.speed <= 640 - 32:
                self.x = self.x + self.speed

    def attack(self):  # 스킬을 사용
        position = pygame.mouse.get_pos()
        tmptime = time.time();
        self.arrows.append([math.atan2(position[1] - (self.y + 32), position[0] - (self.x + 26)), \
                            self.x + 26, self.y + 32])
        pygame.mixer.music.load('resources/audio/throw.mp3')
        pygame.mixer.music.play(0)
        return tmptime

    def spelluse(self,type): # 스펠을 사용
        returnlist=[]
        tmtime=time.time()
        if type=='r':
            returnlist=spelluses(self.x,self.y,self.spelllist[self.spell1type])
        if type=='f':
            returnlist=spelluses(self.x,self.y,self.spelllist[self.spell2type])
        self.x = returnlist[0]
        self.y = returnlist[1]
        if returnlist[2]=='heal':
            self.health+=20
        if returnlist[2]=='exhaust':
            pass
        if returnlist[2]=='ghost':
            self.speed=7

        return tmtime

    def injured(self, oppomundo):  # 공격받았을 때 체력이 깎임
        global pre2_time
        index1=0
        for bullet in oppomundo.arrows:
            bullrect = pygame.Rect(arrow.get_rect())
            bullrect.left = bullet[1]
            bullrect.top = bullet[2]
            tmpmundo = pygame.Rect(mundo.get_rect())
            tmpmundo.center=(self.x,self.y)
            if tmpmundo.colliderect(bullrect):
                self.health -= oppomundo.strength / self.armor * 100
                oppomundo.arrows.pop(index1)
                pygame.mixer.music.load('resources/audio/injured.mp3')
                pygame.mixer.music.play(0)
                pre2_time=time.time()
                self.speed=3
            if time.time()-pre2_time>=2:
                self.speed=5
            index1+=1
def spelluses(mx,my,spelltype)->list:
    list = []
    if spelltype == "flash":
        posi = pygame.mouse.get_pos()
        angle = math.atan2(posi[1] - (my + 32), posi[0] - (mx + 26))
        list.append(mx+math.cos(angle)*100)
        list.append(my+math.sin(angle)*100)
        list.append("flash")
    elif spelltype == "heal":
        list.append(mx)
        list.append(my)
        list.append("heal")
    elif spelltype == "ignite":
        list.append(mx)
        list.append(my)
        list.append("ignite")
    elif spelltype == "exhaust":
        list.append(mx)
        list.append(my)
        list.append("exhaust")
    elif spelltype == "ghost":
        list.append(mx)
        list.append(my)
        list.append("ghost")
    return list


def basicscreenblit():
    screen.fill((0, 0, 0))  # R,G,B
    for x in range(width // grass.get_width() + 1):
        for y in range(height // grass.get_height() + 1):
            screen.blit(grass, (x * 100, y * 100))
    screen.blit(bush, (0, 30))
    screen.blit(bush, (0, 135))
    screen.blit(bush, (0, 240))
    screen.blit(bush, (0, 345))
    screen.blit(bush, (540, 30))
    screen.blit(bush, (540, 135))
    screen.blit(bush, (540, 240))
    screen.blit(bush, (540, 345))
    for x in range(width // wall.get_width() + 1):
        screen.blit(wall, (x * 40, 240))


def mundoblit(tmpmundo, pos):  # 문도의 상태 갱신
    angle = math.atan2(pos[1] - (tmpmundo.y + 32), pos[0] - (tmpmundo.x + 26))
    playerrot = pygame.transform.rotate(mundo, 360 - angle * 57.29)
    playerpos1 = (tmpmundo.x - playerrot.get_rect().width // 2, tmpmundo.y - playerrot.get_rect().height // 2)
    screen.blit(playerrot, playerpos1)


def arrowblit(tmpmundo):  # 칼의 상태 갱신
    for bullet in tmpmundo.arrows:
        index = 0
        velx = math.cos(bullet[0]) * 7.5
        vely = math.sin(bullet[0]) * 7.5
        bullet[1] += velx
        bullet[2] += vely
        if bullet[1] < -64 or bullet[1] > 640 or bullet[2] < -64 or bullet[2] > 480:
            tmpmundo.arrows.pop(index)
        index = index + 1
    for projectile in tmpmundo.arrows:
        arrow1 = pygame.transform.rotate(arrow, 360 - projectile[0] * 57.29)
        screen.blit(arrow1, (projectile[1], projectile[2]))


def wait_for_key_pressed():  # 초기 화면 전환
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # When we press the "esc" key we're out of the game
                    exit_game()
                # When we press any key we leave the loop and the game continues.
                return


def draw_text(text, font, surface, x, y):  # 화면에 텍스트 입력
    text_obj = font.render(text, True, TEXTCOLOR)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(font.render(text, True, TEXTCOLOR), text_rect)


def exit_game(self):  # 게임 종료
    pygame.quit()
    sys.exit()


# 8번까지 구현함
pygame.init()
Mundo1 = Mundo(320.0, 100.0)
Mundo2 = Mundo(320.0, 400.0)
width, height = 640, 480
window = pygame.display.set_mode((width, height))
background = pygame.image.load("resources/images/background.jpg")
window.blit(background, (0, 0))
font0 = pygame.font.SysFont("Agency FB", 36)
font1 = pygame.font.SysFont("Liberation Serif", 24)
draw_text("MUNDO DODGEBALL", font0, window, (width / 3), (height / 3) + 100)
draw_text("press annie key to start!", font1, window, (width / 3), (height / 3) + 150)
draw_text("2019 OOP project by team MUNDO", font1, window, (width / 3) * 2 - 100, (height / 3) * 2 + 100)
pygame.display.update()
wait_for_key_pressed()
screen = pygame.display.set_mode((width, height))
mundo = pygame.image.load("resources/images/mundo.png")
grass = pygame.image.load("resources/images/grass.png")
bush = pygame.image.load("resources/images/bush.png")
arrow = pygame.image.load("resources/images/bullet.png")
wall = pygame.image.load("resources/images/wall.png")

keys = [False, False, False, False]
while True:
    basicscreenblit()
    position = pygame.mouse.get_pos()
    mundoblit(Mundo1, position)
    mundoblit(Mundo2, position)
    arrowblit(Mundo1)
    arrowblit(Mundo2)
    Mundo1.injured(Mundo2)
    Mundo2.injured(Mundo1)
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                keys[0] = True
            elif event.key == pygame.K_a:
                keys[1] = True
            elif event.key == pygame.K_s:
                keys[2] = True
            elif event.key == pygame.K_d:
                keys[3] = True
            elif event.key == pygame.K_q and time.time() - pre_time >= Mundo1.cooltime_limit:
                pre_time = Mundo1.attack()
            elif event.key==pygame.K_r and time.time()-pre3_time>=Mundo1.spell1cool:
                pre3_time=Mundo1.spelluse('r')
            elif event.key==pygame.K_f and time.time()-pre4_time>=Mundo1.spell2cool:
                pre4_time=Mundo1.spelluse('f')
            if time.time() - pree_time >= 1:
                Mundo1.health += Mundo1.healthregen
                Mundo2.health += Mundo2.healthregen
                pree_time = time.time()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                keys[0] = False
            elif event.key == pygame.K_a:
                keys[1] = False
            elif event.key == pygame.K_s:
                keys[2] = False
            elif event.key == pygame.K_d:
                keys[3] = False
    Mundo1.move(keys[0], keys[1], keys[2], keys[3],1)
