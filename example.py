import pygame,math
import sys
import time
pre_time=time.time()
TEXTCOLOR = (255, 255, 255)
COOLTIME_LIMIT=5
def wait_for_key_pressed():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # When we press the "esc" key we're out of the game
                    exit_game()
                # When we press any key we leave the loop and the game continues.
                return
def draw_text(text, font, surface, x, y):
    text_obj = font.render(text, True, TEXTCOLOR)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(font.render(text, True, TEXTCOLOR), text_rect)

def exit_game(self):
    pygame.quit()
    sys.exit()

# 8번까지 구현함
pygame.init()
width,height=640,480
acc=[0,0]
arrows=[]
window = pygame.display.set_mode((width,height))
background=pygame.image.load("resources/images/background.jpg")
window.blit(background, (0, 0))
font0=pygame.font.SysFont("Agency FB",36)
font1 = pygame.font.SysFont("Liberation Serif", 24)
draw_text("MUNDO DODGEBALL",font0, window, (width / 3), (height / 3) + 100)
draw_text("press annie key to start!",font1, window, (width / 3), (height / 3) + 150)
draw_text("2019 OOP project by team MUNDO",font1, window, (width/3)*2-100, (height / 3)*2+100)
pygame.display.update()
wait_for_key_pressed()
screen=pygame.display.set_mode((width,height))
mundo=pygame.image.load("resources/images/mundo.png")
grass=pygame.image.load("resources/images/grass.png")
bush=pygame.image.load("resources/images/bush.png")
arrow=pygame.image.load("resources/images/bullet.png")
wall=pygame.image.load("resources/images/wall.png")

keys=[False,False,False,False]
playpos=[100,100]
while True:
    screen.fill((0,0,0)) # R,G,B
    for x in range(width//grass.get_width()+1):
        for y in range(height//grass.get_height()+1):
            screen.blit(grass,(x*100,y*100))
    screen.blit(bush, (0, 30))
    screen.blit(bush, (0, 135))
    screen.blit(bush, (0, 240))
    screen.blit(bush, (0, 345))
    screen.blit(bush, (540, 30))
    screen.blit(bush, (540, 135))
    screen.blit(bush, (540, 240))
    screen.blit(bush, (540, 345))
    for x in range(width//wall.get_width()+1):
        screen.blit(wall,(x*40,240))
    position=pygame.mouse.get_pos()
    angle=math.atan2(position[1]-(playpos[1]+32),position[0]-(playpos[0]+26))
    playerrot=pygame.transform.rotate(mundo, 360 - angle * 57.29)
    playerpos1=(playpos[0]-playerrot.get_rect().width//2,playpos[1]-playerrot.get_rect().height//2)
    screen.blit(playerrot,playerpos1)
    for bullet in arrows:
        index=0
        velx=math.cos(bullet[0])*10
        vely=math.sin(bullet[0])*10
        bullet[1]+=velx
        bullet[2]+=vely
        if bullet[1]<-64 or bullet[1]>640 or bullet[2]<-64 or bullet[2]>480:
            arrows.pop(index)
        index=index+1
    for projectile in arrows:
        arrow1=pygame.transform.rotate(arrow,360-projectile[0]*57.29)
        screen.blit(arrow1,(projectile[1],projectile[2]))
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            exit(0)
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_w:
                keys[0]=True
            elif event.key==pygame.K_a:
                keys[1]=True
            elif event.key==pygame.K_s:
                keys[2]=True
            elif event.key==pygame.K_d:
                keys[3]=True
            elif event.key == pygame.K_SPACE and time.time()-pre_time>=COOLTIME_LIMIT:
                position = pygame.mouse.get_pos()
                pre_time=time.time();
                acc[1] = acc[1] + 1
                arrows.append([math.atan2(position[1] - (playpos[1] + 32), position[0] - (playpos[0] + 26)), \
                playpos[0] + 26, playpos[1] + 32])
        if event.type==pygame.KEYUP:
            if event.key==pygame.K_w:
                keys[0]=False
            elif event.key==pygame.K_a:
                keys[1]=False
            elif event.key==pygame.K_s:
                keys[2]=False
            elif event.key==pygame.K_d:
                keys[3]=False
    if keys[0]:
        if 23<=playpos[1]-5<=240-23:
            playpos[1]=playpos[1]-5
    elif keys[2]:
        if 23 <= playpos[1] + 5 <= 240-23:
            playpos[1]=playpos[1]+5
    elif keys[1]:
        if 32 <= playpos[0] - 5 <= 640-32:
            playpos[0]=playpos[0]-5
    elif keys[3]:
        if 32 <= playpos[0] + 5 <= 640-32:
            playpos[0]=playpos[0]+5

