import pygame
import math
import random
pygame.init()

screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Goo Mai Ru")

clock = pygame.time.Clock()

# Load images once
poison_image = pygame.image.load("dmg1.png").convert_alpha()
player_image1 = pygame.image.load("run/rr1.png").convert_alpha()
player_image2 = pygame.image.load("run/rr2.png").convert_alpha()

# Load Sounds Effect
click_sound = pygame.mixer.Sound("sounds/click.wav")
click_sound.set_volume(0.5)

# main menu
font_title = pygame.font.SysFont(None, 80)
font_button = pygame.font.SysFont(None, 40)
game_state = 'MENU'

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
        x = self.x2
        image = pygame.image.load('dmg1.png')
        image = pygame.transform.scale(image,(self.sizex,self.sizey))
        screen.blit(image,(x,self.y))
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
    def draw(self):
        x = self.x2
        image = pygame.image.load('sc1.png')
        image = pygame.transform.scale(image,(self.sizex,self.sizey))
        screen.blit(image,(x,self.y))
    def get_rect(self):
        return pygame.Rect(
            int(self.x2 + self.sizex * 0.24),
            int(self.y + self.sizey * 0.60),
            int(self.sizex * 0.54),
            int(self.sizey * 0.34)
        )


# In game black ground
class bg :
    def __init__(self):
        self.x = 800
        self.y = 800
    def draw(self) :
        image = pygame.image.load('rd1.png')
        image = pygame.transform.scale(image,(self.x,self.y))
        screen.blit(image,(0,0))
blg = bg()

# Player class
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
            image = pygame.image.load('run/rr1.png')
        elif ct == 2 :
            image = pygame.image.load('run/rr2.png')
        image = pygame.transform.scale(image,(self.sizex,self.sizey))
        screen.blit(image,(x,self.y))

    def get_rect(self):
        x = self.lane_x[self.lane]

        return pygame.Rect(
            x + 135,
            self.y + 50,
            130,
            300
        )

player = Player()

# pattern class
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
    global game_over, timer, coun
    global pattern_check, btime, tct, realtimer, tc

    game_over = False
    timer = 0
    coun = 1

    realtimer = 60
    btime = realtimer
    tct = realtimer
    pattern_check = 0
    tc = 0

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
                    game_state = 'PLAY'

            elif game_state == 'PLAY':
                if not game_over:
                    # A and D keys for player movement
                    player.handle_event(event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and game_state == 'PLAY' and game_over:
                if restart_button.collidepoint(event.pos):
                    click_sound.play()
                    restart_game()

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
        screen.blit(ti_te, (50,100))
        fi.close()

        # Draw the main menu
        title_line1 = font_title.render("Paint Color", True, (50, 50, 50))
        title_line2 = font_title.render("To This World", True, (50, 50, 50))
        screen.blit(title_line1, title_line1.get_rect(center=(400, 285)))
        screen.blit(title_line2, title_line2.get_rect(center=(400, 365)))

        # Draw the start button
        button_rect = pygame.Rect(291, 450, 220, 70)
        pygame.draw.rect(screen, (70, 150, 255), button_rect, border_radius=10)

        btn_text = font_button.render("Press E to Start", True, (255, 255, 255))
        screen.blit(btn_text, (299, 470))

    elif game_state == 'PLAY':
        if not game_over:
            blg.draw()
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
                game_over = True

            #Timer
            ti_te = ti_font.render("Time left = "+str(int(realtimer//1)), True, (0, 0, 0))
            ti_te_rect = ti_te.get_rect(center=(50, 50))
            screen.blit(ti_te, (50,50))

            ti_te = ti_font.render("Your color = "+str(int(score//1)), True, (0, 0, 0))
            ti_te_rect = ti_te.get_rect(center=(50, 50))
            screen.blit(ti_te, (50,100))

            #object pattern
            if pattern_check == 0:
                pt = pattern(2.4)
                rane = random.randint(1,2)
                if rane == 1 :
                    pt.pat1()
                elif rane == 2 :
                    pt.pat2()
                pattern_check = 1
            elif pattern_check == 1 :
                pt.draw()
                if btime-realtimer >= 0.08 :
                    pt.timer += 0.1
                    btime = realtimer
                if pt.dmo[pt.lng-1].y >= 570:
                    pattern_check = 0

            if pt :
                for oc in pt.dmo.values() :
                    if check_collision(oc,player) and tc == 0 :
                        score -= 20
                        tct = realtimer
                        tc = 1
                for oc in pt.sco.values():
                    if check_collision(oc,player) and tc == 0 :
                        score += 10
                        get_score += 10
                        tct = realtimer
                        tc = 1
            if tc == 1 :
                if tct - realtimer >= 0.5 :
                    tc = 0

            timer += 1

            if timer > 3:
                timer = 0
                if coun == 1:
                    coun = 2
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
    pygame.display.flip()

pygame.quit()