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
        self.y = 25
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
        pygame.display.set_caption("Goo Mai Ru")
        image = pygame.image.load('dmg1.png')
        image = pygame.transform.scale(image,(self.sizex,self.sizey))
        screen.blit(image,(x,self.y))


#Obj 1(ตัวเทส)
obj1 = green_poison(1,random.randint(0,2))

class Player:
    def __init__(self):
        self.lane = 1
        self.lane_x = [200, 400, 600]
        self.y = 700
        self.color = (70, 150, 255)

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

    def draw(self):
        x = self.lane_x[self.lane]

        pygame.draw.circle(
            screen,
            self.color,
            (x, self.y),
            50
        )


player = Player()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        player.handle_event(event)

    screen.fill((240, 240, 240))

    player.draw()
    #Don't forget to remove
    if not obj1.y >= 570 :
        obj1.draw()
        obj1.move()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()