import pygame

pygame.init()

screen = pygame.display.set_mode((400, 600))
pygame.display.set_caption("Goo Mai Ru")

clock = pygame.time.Clock()

class obj:
    def __init__(self,speed,obj_start_point):
        self.lane = obj_start_point
        self.lane_x = [100, 200, 300]
        self.y = 25
        self.color = (70, 150, 255)
        self.speed = speed
    def draw(self):
        pass
    def move(self):
        self.y = self.y + (5*self.speed)

class obj_rect(obj):
    def __init__(self,speed,obj_start_point,sizex,sizey):
        super().__init__(speed,obj_start_point)
        self.sizex = sizex
        self.sizey = sizey
    def draw(self):
        x = self.lane_x[self.lane]

        pygame.draw.rect(
            screen,
            self.color,
            (x, self.y,self.sizex,self.sizey),
        )
#Obj 1(ตัวเทส)
obj1 = obj_rect(1,1,30,25)

class Player:
    def __init__(self):
        self.lane = 1
        self.lane_x = [100, 200, 300]
        self.y = 500
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
            25
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
    obj1.draw()
    obj1.move()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()