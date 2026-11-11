import pygame
import math
import random
pygame.init()

screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Goo Mai Ru")

clock = pygame.time.Clock()

class obj:
    def __init__(self,speed,obj_start_point):
        self.lane = obj_start_point
        self.sizex = 80
        self.sizey = 80
        self.lane_x = [335, 355, 375]
        self.y = -50
        self.color = (70, 150, 255)
        self.speed = speed
        self.x2 = self.lane_x[self.lane]
    def draw(self):
        pass
    def move(self):
        if self.lane == 1 :
            self.y += 5*self.speed
            self.sizex = self.sizex + 1*self.speed
            self.sizey = self.sizey + 1*self.speed
            self.x2 -= 0.4*self.speed
        elif self.lane == 0 :
            self.y += 5*self.speed
            self.sizex = self.sizex + 1*self.speed
            self.sizey = self.sizey + 1*self.speed
            self.x2 -= (0.4+1.7)*self.speed
        elif self.lane == 2 :
            self.y += 5*self.speed
            self.sizex = self.sizex + 1*self.speed
            self.sizey = self.sizey + 1*self.speed
            self.x2 -= (0.4-1.7)*self.speed

class green_poison(obj):
    def __init__(self,speed,obj_start_point):
        super().__init__(speed,obj_start_point)
    def draw(self):
        x = self.x2
        image = pygame.image.load('dmg1.png')
        image = pygame.transform.scale(image,(self.sizex,self.sizey))
        screen.blit(image,(x,self.y))

class paintb(obj):
    def __init__(self,speed,obj_start_point):
        super().__init__(speed,obj_start_point)
    def draw(self):
        x = self.x2
        image = pygame.image.load('sc1.png')
        image = pygame.transform.scale(image,(self.sizex,self.sizey))
        screen.blit(image,(x,self.y))



class bg :
    def __init__(self):
        self.x = 800
        self.y = 800
    def draw(self) :
        image = pygame.image.load('rd1.png')
        image = pygame.transform.scale(image,(self.x,self.y))
        screen.blit(image,(0,0))

blg = bg()

class Player:
    def __init__(self):
        self.lane = 1
        self.lane_x = [0, 200, 400]
        self.y = 400
        self.color = (70, 150, 255)
        self.sizex = 400
        self.sizey = 400

    def move_left(self):
        if self.lane > 0:
            self.lane -= 1

    def move_right(self):
        if self.lane < 2:
            self.lane += 1

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                self.move_left()
            elif event.key == pygame.K_d:
                self.move_right()

    def draw(self,ct):
        x = self.lane_x[self.lane]
        if ct == 1 :
            image = pygame.image.load('rr1.png')
        elif ct == 2 :
            image = pygame.image.load('rr2.png')
        image = pygame.transform.scale(image,(self.sizex,self.sizey))
        screen.blit(image,(x,self.y))

class pattern :
    def __init__(self,gspeed):
        self.dmo = {} #damage object dict
        self.sco = {}
        self.sp = gspeed
        self.dpt = [] #damage object pattern
        self.ds = [] #damage objet show out time
        self.spt = []
        self.ss = []
        self.timer = 0
        self.lng = 0
    def pat1(self) :
        self.dpt = [1,0,2,0,2,0]
        self.ds = [1,2,4,5,6,7]
        self.lng = len(self.dpt) if len(self.dpt) >= len(self.spt) else len(self.spt)
        for i in range(len(self.dpt)):
            self.dmo[i] = green_poison(self.sp,self.dpt[i])
        self.spt = [0,2,0,2,0,2]
        self.ss = [0.3,1,4,5,6,7]
        for i in range(len(self.spt)):
            self.sco[i] = paintb(self.sp,self.spt[i])
    def pat2(self) :
        self.dpt = [1,1,1,1,1]
        self.ds = [0,3,6,9,12]
        self.lng = len(self.dpt) if len(self.dpt) >= len(self.spt) else len(self.spt)
        for i in range(len(self.dpt)):
            self.dmo[i] = green_poison(self.sp,self.dpt[i])
        self.spt = [1,1,1,1]
        self.ss = [1.5,4.5,7.5,10.5]
        for i in range(len(self.spt)):
            self.sco[i] = paintb(self.sp,self.spt[i])
    def draw(self):
        for tm in range(self.lng):
            if tm in self.dmo.keys():
                if not self.dmo[tm].y >= 570 and self.timer*self.sp >= self.ds[tm]:
                        self.dmo[tm].draw()
                        self.dmo[tm].move()
                elif self.dmo[tm].y >= 570:
                    del self.dmo[tm]
            
            if tm in self.sco.keys():
                if not self.sco[tm].y >= 570 and self.timer*self.sp >= self.ss[tm]:
                        self.sco[tm].draw()
                        self.sco[tm].move()
                elif self.sco[tm].y >= 570:
                    del self.sco[tm]

pattern_check = 0

player = Player()

pytime = pygame.event.custom_type()
pygame.time.set_timer(pytime,10)
pttick = 0
realtimer = 120
btime = realtimer

ti_font = pygame.font.Font(None, 40)

running = True
Ti = 0
timer = 0
coun = 1
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        player.handle_event(event)

        if event.type == pytime:
            realtimer -= 0.01

    screen.fill((240, 240, 240))

    blg.draw()

    ti_te = ti_font.render(
        "Time left = "+str(int(realtimer//1)), True, (0, 0, 0)
    )
    ti_te_rect = ti_te.get_rect(center=(50, 50))
    screen.blit(ti_te, (50,50))

    if pattern_check == 0:
        pt = pattern(1.2)
        rane = random.randint(1,2)
        if rane == 1 :
            pt.pat1()
        elif rane == 2 :
            pt.pat2()
        pattern_check = 1
    elif pattern_check == 1 :
        pt.draw()
        if btime-realtimer >= 0.06 :
            pt.timer += 0.1
            btime = realtimer
        if pt.dmo[pt.lng-1].y >= 570:
            pattern_check = 0

    player.draw(coun)
    
    clock.tick(60)
    if timer <= 8:
        timer +=1
    else :
        timer = 0
        if coun == 1 :
            coun = 2
        else :
            coun = 1
    pygame.display.flip()

pygame.quit()