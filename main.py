import pygame
import math
import random
pygame.init()

screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Paint Color to This World")

paint_images = {
    "sc1.png": pygame.image.load("sc1.png").convert_alpha(),
    "color/green.png": pygame.image.load("color/green.png").convert_alpha(),
    "color/red.png": pygame.image.load("color/red.png").convert_alpha(),
    "color/blue.png": pygame.image.load("color/blue.png").convert_alpha()
}

clock = pygame.time.Clock()

def load_scaled_image(path, size):
    image = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(image, size)


# Player animation: frame 1-4
run_images = {
    1: load_scaled_image("run/r4.png", (500, 500)),
    2: load_scaled_image("run/r3.png", (500, 500)),
    3: load_scaled_image("run/r2.png", (500, 500)),
    4: load_scaled_image("run/r1.png", (500, 500))
}

# Background images
background_images = {
    "no": load_scaled_image("rd1.png", (800, 800)),
    "r": load_scaled_image("red/rd.png", (800, 800)),
    "g": load_scaled_image("green/gr.png", (800, 800)),
    "b": load_scaled_image("blue/bl.png", (800, 800))
}

# Load images once
poison_image = pygame.image.load("dmg1.png").convert_alpha()
player_image1 = pygame.image.load("run/r1.png").convert_alpha()
player_image2 = pygame.image.load("run/r2.png").convert_alpha()
player_image1 = pygame.image.load("run/r3.png").convert_alpha()
player_image2 = pygame.image.load("run/r4.png").convert_alpha()
paint_image = pygame.image.load("sc1.png").convert_alpha()

# Load Sounds Effect
click_sound = pygame.mixer.Sound("sounds/click.wav")
click_sound.set_volume(0.5)

# main menu
font_title = pygame.font.SysFont(None, 80)
font_button = pygame.font.SysFont(None, 40)
game_state = 'MENU'

#color check :
red = 0
gre = 0
blu = 0

#difficult control
df = 0
spdt = 0
timep = 0

# Parent object class
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
    def reset(self):
        self.sizex = 80
        self.sizey = 80
        self.y = -50
        self.x2 = self.lane_x[self.lane]

#Child class (Damage_object)
class green_poison(obj):
    def __init__(self,speed,obj_start_point):
        super().__init__(speed,obj_start_point)
    def draw(self):
        image = pygame.transform.scale(
            poison_image,
            (int(self.sizex), int(self.sizey))
        )
        screen.blit(image, (self.x2, self.y))
    def get_rect(self):
        return pygame.Rect(
            int(self.x2 + self.sizex * 0.24),
            int(self.y + self.sizey * 0.60),
            int(self.sizex * 0.54),
            int(self.sizey * 0.34)
        )

#Child class (Score_object)
class paintb(obj):
    def __init__(self,speed,obj_start_point):
        super().__init__(speed,obj_start_point)
        self.im = 'sc1.png'
    def draw(self):
        image = pygame.transform.scale(
            paint_images[self.im],
            (int(self.sizex), int(self.sizey))
        )
        screen.blit(image, (self.x2, self.y))
    def get_rect(self):
        return pygame.Rect(
            int(self.x2 + self.sizex * 0.24),
            int(self.y + self.sizey * 0.60),
            int(self.sizex * 0.54),
            int(self.sizey * 0.34)
        )
    def point(self) :
        pass

class greenp(paintb):
    def __init__(self,speed,obj_start_point):
        super().__init__(speed,obj_start_point)
        self.im = 'color/green.png'
    def point(self) :
        global gre
        gre += 1


class redp(paintb):
    def __init__(self,speed,obj_start_point):
        super().__init__(speed,obj_start_point)
        self.im = 'color/red.png'
    def point(self) :
        global red
        red += 1


class bluep(paintb):
    def __init__(self,speed,obj_start_point):
        super().__init__(speed,obj_start_point)
        self.im = 'color/blue.png'
    def point(self) :
        global blu
        blu += 1

# In game black ground
class bg :
    def __init__(self,bgcc):
        self.x = 800
        self.y = 800
        self.bgcc = bgcc
    def draw(self) :
        if self.bgcc == "b" :
            image = pygame.image.load("blue/bl.png")
            image = pygame.transform.scale(image,(self.x,self.y))
            screen.blit(image,(0,0))
        elif self.bgcc == "r" :
            image = pygame.image.load("red/rd.png")
            image = pygame.transform.scale(image,(self.x,self.y))
            screen.blit(image,(0,0))
        elif self.bgcc == "g" :
            image = pygame.image.load("green/gr.png")
            image = pygame.transform.scale(image,(self.x,self.y))
            screen.blit(image,(0,0))
        else :
            image = pygame.image.load('rd1.png')
            image = pygame.transform.scale(image,(self.x,self.y))
            screen.blit(image,(0,0))
    def change(self,nbg):
        self.bgcc = nbg
blg = bg('no')

# black ground change
class bgc :
    def __init__(self):
        self.x = 800
        self.y = 800
    def bch(self):
        global bcetim,red,gre,blu,stp,blg
        if stp == 0 :
            stp += 1
        if red > gre and red > blu :
            if stp < 5 :
                image = pygame.image.load("red/r"+str(stp)+'.png')
                image = pygame.transform.scale(image,(self.x,self.y))
                screen.blit(image,(0,0))
            elif stp >= 5 :
                image = pygame.image.load("red/r4.png")
                image = pygame.transform.scale(image,(self.x,self.y))
                screen.blit(image,(0,0))
                blg.change('r')
        elif gre > red and gre> blu :
            if stp < 5 :
                image = pygame.image.load("green/g"+str(stp)+'.png')
                image = pygame.transform.scale(image,(self.x,self.y))
                screen.blit(image,(0,0))
            elif stp >= 5 :
                image = pygame.image.load("green/g4.png")
                image = pygame.transform.scale(image,(self.x,self.y))
                screen.blit(image,(0,0))
                blg.change('g')
        elif blu > red and blu > gre :
            if stp < 5 :
                image = pygame.image.load("blue/b"+str(stp)+'.png')
                image = pygame.transform.scale(image,(self.x,self.y))
                screen.blit(image,(0,0))
            elif stp >= 5 :
                image = pygame.image.load("blue/b4.png")
                image = pygame.transform.scale(image,(self.x,self.y))
                screen.blit(image,(0,0))
                blg.change('b')
        if bcetim >= 5 :
            stp += 1
            bcetim = 0
        else :
            bcetim +=1
bcetim = 0
stp = 0
cbg = bgc()

# Player class
class Player:
    def __init__(self):
        self.lane = 1
        self.lane_x = [-60, 140, 340]
        self.y = 300
        self.color = (70, 150, 255)
        self.sizex = 500
        self.sizey = 500

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

    def draw(self, ct):
        x = self.lane_x[self.lane]
        screen.blit(run_images[ct], (x, self.y))

    def get_rect(self):
        x = self.lane_x[self.lane]

        return pygame.Rect(
            x + 195,
            self.y + 110,
            130,
            300
        )

player = Player()

# pattern class
class pattern :
    def __init__(self,gspeed):
        global spdt
        self.dmo = {} #damage object dict
        self.sco = {}
        self.sp = gspeed*spdt
        self.dpt = [] #damage object pattern
        self.ds = [] #damage objet show out time
        self.spt = []
        self.ss = []
        self.timer = 0
        self.lng = 0
        self.clr = []
    def pat1(self) :
        self.dpt = [1,0,2,0,2,0]
        self.ds = [1,2,4,5,6,7]
        self.spt = [0,2,0,2,0,2]
        self.ss = [0.3,1,4,5,6,7]
        self.clr = ['b','0','g','b','r','g']
        self.lng = len(self.dpt) if len(self.dpt) >= len(self.spt) else len(self.spt)
        for i in range(len(self.dpt)):
            self.dmo[i] = green_poison(self.sp,self.dpt[i])
        for i in range(len(self.spt)):
            if self.clr[i] == '0' :
                self.sco[i] = paintb(self.sp,self.spt[i])
            elif self.clr[i] == 'r':
                self.sco[i] = redp(self.sp,self.spt[i])
            elif self.clr[i] == 'g':
                self.sco[i] = greenp(self.sp,self.spt[i])
            elif self.clr[i] == 'b':
                self.sco[i] = bluep(self.sp,self.spt[i])
    def pat2(self) :
        self.dpt = [1,1,1,1,1]
        self.ds = [0,3,6,9,12]
        self.spt = [1,1,1,1]
        self.ss = [1.5,4.5,7.5,10.5]
        self.clr = ['g','r','g','r']
        self.lng = len(self.dpt) if len(self.dpt) >= len(self.spt) else len(self.spt)
        for i in range(len(self.dpt)):
            self.dmo[i] = green_poison(self.sp,self.dpt[i])
        for i in range(len(self.spt)):
            if self.clr[i] == '0' :
                self.sco[i] = paintb(self.sp,self.spt[i])
            elif self.clr[i] == 'r':
                self.sco[i] = redp(self.sp,self.spt[i])
            elif self.clr[i] == 'g':
                self.sco[i] = greenp(self.sp,self.spt[i])
            elif self.clr[i] == 'b':
                self.sco[i] = bluep(self.sp,self.spt[i])
    def pat3(self) :
        self.dpt = [2]
        self.ds = [3]
        self.spt = [1,2,1,1,2]
        self.ss = [0,1,2,4,5]
        self.clr = ['r','g','b','r','b']
        self.lng = len(self.dpt) if len(self.dpt) >= len(self.spt) else len(self.spt)
        for i in range(len(self.dpt)):
            self.dmo[i] = green_poison(self.sp,self.dpt[i])
        for i in range(len(self.spt)):
            if self.clr[i] == '0' :
                self.sco[i] = paintb(self.sp,self.spt[i])
            elif self.clr[i] == 'r':
                self.sco[i] = redp(self.sp,self.spt[i])
            elif self.clr[i] == 'g':
                self.sco[i] = greenp(self.sp,self.spt[i])
            elif self.clr[i] == 'b':
                self.sco[i] = bluep(self.sp,self.spt[i])
    def pat4(self) :
        self.dpt = [0,2,0,2,0,2]
        self.ds = [0,0,2,2,4,4]
        self.spt = [1,2,0,1,2,0]
        self.ss = [1,1,1,3,3,3]
        self.clr = ['0','r','g','0','b','g']
        self.lng = len(self.dpt) if len(self.dpt) >= len(self.spt) else len(self.spt)
        for i in range(len(self.dpt)):
            self.dmo[i] = green_poison(self.sp,self.dpt[i])
        for i in range(len(self.spt)):
            if self.clr[i] == '0' :
                self.sco[i] = paintb(self.sp,self.spt[i])
            elif self.clr[i] == 'r':
                self.sco[i] = redp(self.sp,self.spt[i])
            elif self.clr[i] == 'g':
                self.sco[i] = greenp(self.sp,self.spt[i])
            elif self.clr[i] == 'b':
                self.sco[i] = bluep(self.sp,self.spt[i])
    def draw(self):
        for tm in range(self.lng):
            if tm in self.sco.keys():
                if not self.sco[tm].y >= 900 and self.timer*self.sp >= self.ss[tm]:
                    self.sco[tm].draw()
                    self.sco[tm].move()
                elif self.sco[tm].y >= 900:
                    del self.sco[tm]
            if tm in self.dmo.keys():
                if not self.dmo[tm].y >= 900 and self.timer*self.sp >= self.ds[tm]:
                    self.dmo[tm].draw()
                    self.dmo[tm].move()
                elif self.dmo[tm].y >= 900:
                    del self.dmo[tm]
            
    def collis_check(self,pla) :
        global score,get_score,df,stp
        self.ky = list(self.dmo.keys())
        for oc in self.ky :
            if check_collision(self.dmo[oc],pla) :
                score -= 20*df
                del self.dmo[oc]

        self.ky2 = list(self.sco.keys())
        for oc in self.ky2:
            if check_collision(self.sco[oc],pla) :
                score += 10
                get_score += 10
                if stp == 0 :
                    self.sco[oc].point()
                del self.sco[oc]

    def remove(self,ty,loc):
        if ty == "sco" :
            del self.sco[loc]
        if ty == "dmo" :
            del self.dmo[loc]

pattern_check = 0

# Collision function
def check_collision(obj1, player):
    if obj1.lane != player.lane:
        return False

    if obj1.y < 480:
        return False

    return obj1.get_rect().colliderect(
        player.get_rect()
    )

# Restart function
def restart_game():
    global game_over, timer, coun, timep
    global pattern_check, btime, tct, realtimer, tc
    global bcetim, stp
    global red, gre, blu, score, get_score

    game_over = False
    timer = 0
    coun = 1

    # Reset score
    score = 100
    get_score = 0

    # Reset collected colors
    red = 0
    gre = 0
    blu = 0

    # Reset background and animation
    blg.change('no')
    bcetim = 0
    stp = 0

    # Reset timer
    realtimer = 60 + timep
    btime = realtimer
    tct = realtimer

    pattern_check = 0
    tc = 0

    # Reset player
    player.lane = 1

#timer
pytime = pygame.event.custom_type()
pygame.time.set_timer(pytime,10)
realtimer = 60
btime = realtimer

#timer font
ti_font = pygame.font.Font(None, 40)

font = pygame.font.Font(None, 80)
small_font = pygame.font.Font(None, 36)
restart_button = pygame.Rect(300, 380, 200, 60)
menu_button = pygame.Rect(300, 460, 200, 60)
diff_ez_button = pygame.Rect(200, 100, 400, 100)
diff_normal_button = pygame.Rect(200, 270, 400, 100)
diff_hard_button = pygame.Rect(200, 440, 400, 100)
running = True
game_over = False
show_hitbox = False
timer = 0
coun = 1
score = 100
get_score = 0

tc = 0
tct = realtimer
escore = 0
get_score_o = 0
hgsore = 0
hg_te = 0
rng = 0

#fps check
fp = 0
ftim = realtimer
fc = 0

# Main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            # hitbox toggle
            if event.key == pygame.K_h:
                show_hitbox = not show_hitbox
            # start game from menu
            if game_state == 'MENU':
                if event.key == pygame.K_e:
                    restart_game()
                    game_state = 'Diff'
            # A and D keys for player movement
            if game_state == 'PLAY' and not game_over:
                player.handle_event(event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and game_state == 'MENU':
                if 291 <= event.pos[0] <= 511 and 450 <= event.pos[1] <= 520:
                    click_sound.play()
                    game_state = 'Diff'

            elif event.button == 1 and game_state == 'Diff':  ##########difficulty selection
                if diff_ez_button.collidepoint(event.pos):
                    # Set game difficulty to easy
                    click_sound.play()
                    df = 0.5
                    spdt = 0.75
                    timep = 30
                    rng = +0.04
                    restart_game()
                    game_state = 'PLAY'
                elif diff_normal_button.collidepoint(event.pos):
                    # Set game difficulty to normal
                    click_sound.play()
                    df = 2
                    spdt = 1
                    timep = 0
                    rng = +0.02
                    restart_game()
                    game_state = 'PLAY'
                elif diff_hard_button.collidepoint(event.pos):
                    # Set game difficulty to hard
                    click_sound.play()
                    df = 100
                    spdt = 1.5
                    timep = -15
                    rng = 0.05
                    restart_game()
                    game_state = 'PLAY'

            elif event.button == 1 and game_state == 'PLAY' and game_over:
                if restart_button.collidepoint(event.pos):
                    click_sound.play()
                    game_state = 'Diff'
                    game_over = False

                elif menu_button.collidepoint(event.pos):
                    click_sound.play()
                    game_state = 'MENU'
                    game_over = False

        #Timer event
        if event.type == pytime:
            realtimer -= 0.01

    #white screen
    screen.fill((240, 240, 240))

    if game_state == 'MENU':
        #Total color
        fi = open("TotalPaint.txt","r")
        ti_te = ti_font.render("Total color point = "+fi.read(), True, (0, 0, 0))
        screen.blit(ti_te, (10,10))
        fi.close()

        #high color
        fi = open("highest.txt","r")
        hg_te = ti_font.render("Highest color = "+fi.read(), True, (0, 0, 0))
        screen.blit(hg_te, (10,35))
        fi.close()

        # Draw the main menu
        title_line1 = font_title.render("Paint Color", True, (50, 50, 50))
        title_line2 = font_title.render("To This World", True, (50, 50, 50))
        screen.blit(title_line1, title_line1.get_rect(center=(400, 285)))
        screen.blit(title_line2, title_line2.get_rect(center=(400, 365)))

        # Draw the start button
        button_rect = pygame.Rect(291, 450, 220, 70)
        pygame.draw.rect(screen, (70, 150, 255), button_rect, border_radius=10)

        btn_text = font_button.render("Press to Start", True, (255, 255, 255))
        screen.blit(btn_text, (310, 470))

    elif game_state == 'Diff':

        # Draw difficulty selection buttons
        pygame.draw.rect(screen, (70, 200, 70), diff_ez_button, border_radius=10)
        pygame.draw.rect(screen, (200, 200, 70), diff_normal_button, border_radius=10)
        pygame.draw.rect(screen, (200, 70, 70), diff_hard_button, border_radius=10)

        ez_text = font_button.render("Easy", True, (255, 255, 255))
        normal_text = font_button.render("Normal", True, (255, 255, 255))
        hard_text = font_button.render("Hard", True, (255, 255, 255))

        screen.blit(ez_text, (365, 140))
        screen.blit(normal_text, (350, 310))
        screen.blit(hard_text, (365, 480))

    elif game_state == 'PLAY':
        if not game_over:
            blg.draw()
            
            if blu >= 3 and blu>red and blu>gre and blg.bgcc != "b" :
                cbg.bch()
            elif red >= 3 and red>blu and red>gre and blg.bgcc != "r" :
                cbg.bch()
            elif gre >= 3 and gre>blu and gre>red and blg.bgcc != "g" :
                cbg.bch()
            else :
                stp = 0
                bcetim = 0

            if score <= 0 or realtimer <= 0:
                get_score_o = get_score
                fi = open("TotalPaint.txt","r")
                get_score += int(fi.read().strip())
                fi.close()
                fi = open("TotalPaint.txt","w")
                fi.write(str(get_score))
                fi.close()
                get_score = 0
                escore = score
                fi = open("highest.txt","r")
                hgsore = int(fi.read().strip())
                fi.close()
                if score >= hgsore :
                    hgsore = score
                fi = open("highest.txt","w")
                fi.write(str(hgsore))
                fi.close()
                game_over = True

            #Timer
            ti_te = ti_font.render("Time left = "+str(int(realtimer//1)), True, (0, 0, 0))
            ti_te_rect = ti_te.get_rect(center=(50, 50))
            screen.blit(ti_te, (50,50))

            #color
            ti_te = ti_font.render("Your color = "+str(int(score//1)), True, (0, 0, 0))
            ti_te_rect = ti_te.get_rect(center=(50, 50))
            screen.blit(ti_te, (50,100))

            #FPS
            #if not ftim-realtimer >= 1:
            #    fc+=1
            #else :
            #    fp = fc
            #    fc = 0
            #    ftim = realtimer
            #ti_te = ti_font.render("FPS:"+str(int(fp)), True, (0, 0, 0))
            #ti_te_rect = ti_te.get_rect(center=(50, 50))
            #screen.blit(ti_te, (50,130))

            #object pattern
            if pattern_check == 0:
                pt = pattern(2.4)
                rane = random.randint(1,4) 
                if rane == 1 :
                    pt.pat1()
                elif rane == 2 :
                    pt.pat2()
                elif rane == 3 :
                    pt.pat3()
                elif rane == 4 :
                    pt.pat4()
                pattern_check = 1
            elif pattern_check == 1 :
                pt.draw()
                if btime-realtimer >= 0.08+rng :
                    pt.timer += 0.1
                    btime = realtimer
                if len(pt.dmo) == 0 and len(pt.sco) == 0 :
                    pattern_check = 0
                pt.collis_check(player)

            #if pt :
            #    for oc in pt.dmo.values() :
            #        if check_collision(oc,player) and tc == 0 :
            #            score -= 20
            #            tct = realtimer
            #            tc = 1
            #    for oc in pt.sco.values():
            #        if check_collision(oc,player) and tc == 0 :
            #            score += 10
            #            get_score += 10
            #            tct = realtimer
            #            tc = 1
            #if tc == 1 :
            #    if tct - realtimer >= 0.5 :
            #        tc = 0

            timer += 1

            if timer > 1:
                timer = 0
                if coun < 4:
                    coun += 1
                else:
                    coun = 1
            #player
            player.draw(coun)

            #show hitbox
            if show_hitbox:
                pygame.draw.rect(
                    screen, (255, 0, 0),
                    player.get_rect(), 2
                )
                for oj in pt.dmo.values():
                    pygame.draw.rect(
                        screen, (255, 0, 0),
                        oj.get_rect(), 2
                )
                for oj2 in pt.sco.values():
                    pygame.draw.rect(
                        screen, (255, 0, 0),
                        oj2.get_rect(), 2
                )

        else:
            score = 100 
            if escore <= 0 :
                text = font.render(
                    "GAME OVER", True, (255, 70, 70)
                )
                text_rect = text.get_rect(center=(400, 330))
                screen.blit(text, text_rect)
            else :
                text = font.render(
                    "Your color = " + str(escore), True, (255, 70, 70)
                )
                text_rect = text.get_rect(center=(400, 330))
                screen.blit(text, text_rect)

            mouse_pos = pygame.mouse.get_pos()
            is_hovered = restart_button.collidepoint(mouse_pos)

            mouse_pressed = pygame.mouse.get_pressed()[0]
            is_pressed = is_hovered and mouse_pressed

            if is_pressed:
                button_color = (45, 125, 80)
                offset_y = 4
            elif is_hovered:
                button_color = (105, 205, 145)
                offset_y = 0
            else:
                button_color = (80, 170, 120)
                offset_y = 0

            # Shadow
            shadow_rect = restart_button.move(0, 5)
            pygame.draw.rect(
                screen, (35, 90, 60),
                shadow_rect, border_radius=12
            )

            # Button
            draw_rect = restart_button.move(0, offset_y)
            pygame.draw.rect(
                screen, button_color,
                draw_rect, border_radius=12
            )

            # Text
            restart_text = small_font.render(
                "RESTART", True, (255, 255, 255)
            )

            restart_text_rect = restart_text.get_rect(
                center=draw_rect.center
            )

            screen.blit(restart_text, restart_text_rect)

            # Main Menu button
            menu_hovered = menu_button.collidepoint(
                pygame.mouse.get_pos()
            )

            if menu_hovered:
                menu_color = (110, 155, 210)
            else:
                menu_color = (80, 120, 170)

            pygame.draw.rect(
                screen,
                menu_color,
                menu_button,
                border_radius=12
            )

            menu_text = small_font.render(
                "MAIN MENU", True, (255, 255, 255)
            )

            menu_text_rect = menu_text.get_rect(
                center=menu_button.center
            )

            screen.blit(menu_text, menu_text_rect)
    
    clock.tick(30)

    pygame.display.set_caption(
        f"Goo Mai Ru | FPS: {clock.get_fps():.1f}"
    )

    pygame.display.flip()

pygame.quit()
