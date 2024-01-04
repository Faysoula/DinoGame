import pygame
import random
pygame.init()

SCREEN_HEIGHT = 530
SCREEN_WIDTH = 530

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

RUNNING = [pygame.image.load('Assets/dino/dino0.png'),
    pygame.image.load('Assets/dino/dino1.png'),
    pygame.image.load('Assets/dino/dino2.png'),
    pygame.image.load('Assets/dino/dino3.png'),
    pygame.image.load('Assets/dino/dino4.png'),
    pygame.image.load('Assets/dino/dino5.png')]

JUMP = [pygame.image.load('Assets/dinojump/jump0.png'),
        pygame.image.load('Assets/dinojump/jump1.png'),
        pygame.image.load('Assets/dinojump/jump2.png'),
        pygame.image.load('Assets/dinojump/jump3.png')]

BIRD = [pygame.image.load('Assets/bird/Bird1.png'),
        pygame.image.load('Assets/bird/Bird2.png')]

CROUCH = [pygame.image.load('Assets/Crouch/crouch0.png'),
          pygame.image.load('Assets/Crouch/crouch1.png'),
          pygame.image.load('Assets/Crouch/crouch2.png'),
          pygame.image.load('Assets/Crouch/crouch3.png'),
          pygame.image.load('Assets/Crouch/crouch4.png'),
          pygame.image.load('Assets/Crouch/crouch5.png')]

SMALL_CACTUS = pygame.image.load('Assets/obs/Cactus1.png')


BIG_CACTUS = pygame.image.load('Assets/obs/Cactusbig.png')

BG = [pygame.image.load('Assets/BG.png')]


class Dinosaur:
    X_POS = 80
    Y_POS = 470
    Y_POS_CRCH = 475
    JUMP_VEL = 6

    def __init__(self):
        self.crch_img = CROUCH
        self.run_img = RUNNING
        self.jump_img = JUMP

        self.dino_crch = False
        self.dino_run = True
        self.dino_jump = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

    def update(self, userkey):
        if self.dino_jump:
            self.jump()
        elif self.dino_run:
            self.run()
        elif self.dino_crch:
            self.crouch()

        if self.step_index >= 5:
            self.step_index = 0

        if userkey[pygame.K_UP] and not self.dino_jump:
            self.dino_crch = False
            self.dino_jump = True
            self.dino_run = False
        elif userkey[pygame.K_DOWN] and not self.dino_jump:
            self.dino_crch = True
            self.dino_jump = False
            self.dino_run = False
        elif not (self.dino_jump or userkey[pygame.K_DOWN]):
            self.dino_crch = False
            self.dino_jump = False
            self.dino_run = True

    def crouch(self):
        self.image = CROUCH[self.step_index % len(CROUCH)]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_CRCH
        self.step_index += 1
        if self.step_index >= len(CROUCH) * 5:  # Assuming you want to show each frame for 5 game loops
            self.step_index = 0

    def run(self):
        self.image = RUNNING[self.step_index % len(RUNNING)]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1
        if self.step_index >= len(RUNNING) * 5:  # Assuming you want to show each frame for 5 game loops
            self.step_index = 0

    def jump(self):
        self.image = self.jump_img[0]
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < -self.JUMP_VEL:
            self.dino_jump = False
            self.dino_run = True
            self.jump_vel = self.JUMP_VEL

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))

class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image, self.rect)

class smallCac(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 425

class bigCac(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 435

class Bird(Obstacle):
    def __init__(self, images):
        self.type = 0
        super().__init__(images[self.type], self.type)
        self.image = images
        self.rect.y = 440
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index//5], self.rect)
        self.index += 1

def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles
    isrun = True
    clock = pygame.time.Clock()
    player = Dinosaur()
    game_speed = 10
    x_pos_bg = 0
    y_pos_bg = -90
    points = 0
    obstacles = []
    font = pygame.font.Font('freesansbold.ttf', 20)

    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 0.5
        text = font.render("Points: " + str(points), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (450, 20)
        SCREEN.blit(text, textRect)

    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG[0].get_width()
        SCREEN.blit(BG[0], (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG[0], (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            SCREEN.blit(BG[0], (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed

    def game_over():
        global points
        SCREEN.fill((255, 255, 255))  # Fill the screen with white
        font = pygame.font.Font('freesansbold.ttf', 30)  # Use a larger font for game over
        text = font.render(f"Game Over! Your Score: {points}", True, (255, 0, 0))  # Render the text
        text_rect = text.get_rect()
        text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        SCREEN.blit(text, text_rect)
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    isrun = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        main()

    while isrun:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
             isrun = False

        userkey = pygame.key.get_pressed()

        background()
        score()
        player.draw(SCREEN)
        player.update(userkey)

        if len(obstacles) == 0:
            if random.randint(0, 2) == 0:
                obstacles.append(smallCac(SMALL_CACTUS ))
            elif random.randint(0, 2) == 1:
                obstacles.append(bigCac(BIG_CACTUS))
            elif random.randint(0,2) == 2:
                obstacles.append(Bird(BIRD))


        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            if player.dino_rect.colliderect(obstacle.rect):
                game_over()
                return


        clock.tick(30)
        pygame.display.update()

main()




