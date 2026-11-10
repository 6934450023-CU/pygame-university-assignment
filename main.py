import pygame
import random

pygame.init()

screen = pygame.display.set_mode((400, 600))
pygame.display.set_caption("Goo Mai Ru")

clock = pygame.time.Clock()
class FallingObject:
    def __init__(self,speed,obj_start_point):
        self.lane = obj_start_point
        self.lane_x = [100, 200, 300]
        self.y = -10
        self.color = (70, 150, 255)
        self.speed = speed
    def draw(self):
        pass
    def move(self):
        self.y = self.y + (5 * self.speed)

        if self.y > 600:
            self.y = -10
            self.lane = random.randint(0, 2)

class FallingObject_Rect(FallingObject):
    def __init__(self,speed,obj_start_point,sizex,sizey):
        super().__init__(speed,obj_start_point)
        self.sizex = sizex
        self.sizey = sizey
    def draw(self):
        x = self.lane_x[self.lane]
        pygame.draw.rect(screen,self.color,(x - self.sizex / 2,self.y,self.sizex,self.sizey))

obj1 = FallingObject_Rect(2,1,30,25)
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
game_over = False

def check_collision(obj1, player):
    if obj1.lane == player.lane:
        if obj1.y + obj1.sizey >= player.y - 25 and obj1.y <= player.y + 25:
            print("Collision detected")
            return True

    return False

font = pygame.font.Font(None, 50)

def restart_game():
    global game_over

    game_over = False

    player.lane = 1

    obj1.y = -10
    obj1.lane = random.randint(0, 2)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if not game_over:
            player.handle_event(event)

        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    restart_game()

    screen.fill((240, 240, 240))

    if not game_over:
        player.draw()
        obj1.draw()
        obj1.move()

        if check_collision(obj1, player):
            game_over = True

    else:
        text = font.render("GAME OVER", True, (255, 70, 70))
        text_rect = text.get_rect(center=(200, 270))
        screen.blit(text, text_rect)

        restart_text = pygame.font.Font(None, 30).render(
            "Press R to Restart", True, (80, 80, 80)
        )
        restart_rect = restart_text.get_rect(center=(200, 330))
        screen.blit(restart_text, restart_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()