import pygame
import random

pygame.init()

screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Paint Color To This World")
clock = pygame.time.Clock()

# Load images once
poison_image = pygame.image.load("dmg1.png").convert_alpha()
player_image1 = pygame.image.load("rr1.png").convert_alpha()
player_image2 = pygame.image.load("rr2.png").convert_alpha()

# main menu
font_title = pygame.font.SysFont(None, 80)
font_button = pygame.font.SysFont(None, 40)
game_state = 'MENU'


# Parent class from teammate
class obj:
    def __init__(self, speed, obj_start_point):
        self.lane = obj_start_point
        self.lane_x = [335, 355, 375]
        self.speed = speed
        self.reset()

    def reset(self):
        self.sizex = 80
        self.sizey = 80
        self.y = 25
        self.x2 = self.lane_x[self.lane]

    def draw(self):
        pass

    def move(self):
        self.y += 5 * self.speed
        self.sizex += 1 * self.speed
        self.sizey += 1 * self.speed

        if self.lane == 1:
            self.x2 -= 0.4 * self.speed
        elif self.lane == 0:
            self.x2 -= 2.1 * self.speed
        elif self.lane == 2:
            self.x2 += 1.3 * self.speed


# Child class from teammate
class green_poison(obj):
    def __init__(self, speed, obj_start_point):
        super().__init__(speed, obj_start_point)

    def draw(self):
        image = pygame.transform.scale(
            poison_image,
            (int(self.sizex), int(self.sizey))
        )
        screen.blit(image, (int(self.x2), int(self.y)))

    def get_rect(self):
        return pygame.Rect(
            int(self.x2 + self.sizex * 0.24),
            int(self.y + self.sizey * 0.60),
            int(self.sizex * 0.54),
            int(self.sizey * 0.34)
        )


# Player class
class Player:
    def __init__(self):
        self.lane = 1
        self.lane_x = [0, 200, 400]
        self.y = 400
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

    def draw(self, ct):
        x = self.lane_x[self.lane]

        if ct == 1:
            image = player_image1
        else:
            image = player_image2

        image = pygame.transform.scale(
            image,
            (self.sizex, self.sizey)
        )
        screen.blit(image, (x, self.y))

    def get_rect(self):
        x = self.lane_x[self.lane]

        return pygame.Rect(
            x + 135,
            self.y + 50,
            130,
            300
        )


# Create objects
player = Player()
obj1 = green_poison(1, random.randint(0, 2))

running = True
game_over = False
show_hitbox = False

timer = 0
coun = 1

font = pygame.font.Font(None, 80)
small_font = pygame.font.Font(None, 36)


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

    game_over = False
    timer = 0
    coun = 1

    player.lane = 1

    obj1.lane = random.randint(0, 2)
    obj1.reset()


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
                if game_over:
                    # restart game or go to main menu when game over
                    if event.key == pygame.K_r:
                        restart_game()
                    elif event.key == pygame.K_q:
                        game_state = 'MENU'
                        game_over = False
                else:
                    # A and D keys for player movement
                    player.handle_event(event)

    screen.fill((240, 240, 240))

    if game_state == 'MENU':
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
            obj1.move()

            if check_collision(obj1, player):
                game_over = True

            elif obj1.y >= 570:
                obj1.lane = random.randint(0, 2)
                obj1.reset()

            player.draw(coun)
            obj1.draw()

            if show_hitbox:
                pygame.draw.rect(
                    screen, (255, 0, 0),
                    player.get_rect(), 2
                )
                pygame.draw.rect(
                    screen, (255, 0, 0),
                    obj1.get_rect(), 2
                )

            timer += 1

            if timer > 8:
                timer = 0
                if coun == 1:
                    coun = 2
                else:
                    coun = 1

        else:
            text = font.render(
                "GAME OVER", True, (255, 70, 70)
            )
            text_rect = text.get_rect(center=(400, 330))
            screen.blit(text, text_rect)

            restart_text = small_font.render(
                "Press R to Restart", True, (80, 80, 80)
            )
            restart_rect = restart_text.get_rect(
                center=(400, 410)
            )
            screen.blit(restart_text, restart_rect)

            menu_text = small_font.render(
                "Press Q to Main Menu", True, (80, 80, 80)
            )
            menu_rect = menu_text.get_rect(
                center=(400, 460)
            )
            screen.blit(menu_text, menu_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()