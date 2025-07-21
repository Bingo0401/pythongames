import pygame
import sys

pygame.init()

window = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("Pong")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLUE = (30, 144, 255)
RED = (220, 20, 60)
BGREEN = (34, 139, 34)

# Ball class
class ball:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed_x = 10
        self.speed_y = 10
    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        if self.y > 600 - self.radius or self.y < self.radius:
            self.speed_y = -self.speed_y
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

# Paddle class
class paddle:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.speed_y = 10
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

# CPU Paddle class
class cpu_paddle(paddle):
    def __init__(self, x, y, width, height, color):
        super().__init__(x, y, width, height, color)
        self.speed_y = 10
    def update(self, ball):
        # Move towards the ball's y position
        if self.y + self.height // 2 < ball.y:
            self.y += self.speed_y
        elif self.y + self.height // 2 > ball.y:
            self.y -= self.speed_y
        # Clamp to screen
        if self.y < 0:
            self.y = 0
        if self.y > 600 - self.height:
            self.y = 600 - self.height

# Game class
class Game:
    def __init__(self):
        self.ball = ball(500, 300, 15, WHITE)
        self.player_paddle = paddle(30, 250, 20, 100, BLUE)
        self.cpu_paddle = cpu_paddle(1000 - 40, 250, 20, 100, RED)
        self.player_score = 0
        self.cpu_score = 0
        self.font = pygame.font.SysFont(None, 72)
    def update(self):
        self.ball.update()
        self.cpu_paddle.update(self.ball)
    def draw(self, screen):
        screen.fill(BGREEN)
        # Center dashed line
        dash_height = 30
        gap = 20
        for y in range(0, 600, dash_height + gap):
            pygame.draw.rect(screen, WHITE, (1000//2 - 2, y, 4, dash_height))
        self.ball.draw(screen)
        self.player_paddle.draw(screen)
        self.cpu_paddle.draw(screen)
        # Draw scores
        player_text = self.font.render(str(self.player_score), True, WHITE)
        cpu_text = self.font.render(str(self.cpu_score), True, WHITE)
        screen.blit(player_text, (1000//4, 20))
        screen.blit(cpu_text, (1000*3//4, 20))
    def check_collision(self):
        # Player paddle collision
        if (self.ball.x - self.ball.radius < self.player_paddle.x + self.player_paddle.width and
            self.player_paddle.y < self.ball.y < self.player_paddle.y + self.player_paddle.height):
            self.ball.speed_x = abs(self.ball.speed_x)
        # CPU paddle collision
        if (self.ball.x + self.ball.radius > self.cpu_paddle.x and
            self.cpu_paddle.y < self.ball.y < self.cpu_paddle.y + self.cpu_paddle.height):
            self.ball.speed_x = -abs(self.ball.speed_x)
        # Scoring
        if self.ball.x < 0:
            self.cpu_score += 1
            self.draw(window)
            pygame.display.update()
            pygame.time.delay(1000)
            self.respawn_ball(direction=1)
        elif self.ball.x > 1000:
            self.player_score += 1
            self.draw(window)
            pygame.display.update()
            pygame.time.delay(1000)
            self.respawn_ball(direction=-1)
    def respawn_ball(self, direction):
        self.ball.x = 500
        self.ball.y = 300
        self.ball.speed_x = 12 * direction
        self.ball.speed_y = 12

game = Game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()
    # Player input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        game.player_paddle.y -= game.player_paddle.speed_y
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        game.player_paddle.y += game.player_paddle.speed_y
    # Clamp to screen
    if game.player_paddle.y < 0:
        game.player_paddle.y = 0
    if game.player_paddle.y > 600 - game.player_paddle.height:
        game.player_paddle.y = 600 - game.player_paddle.height

    game.update()
    game.check_collision()
    game.draw(window)
    pygame.display.update()
    clock.tick(60)
