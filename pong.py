import pygame
import sys
import random

pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 800
GAME_TITLE = "PONG"



screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(GAME_TITLE)
clock = pygame.time.Clock()    


cpu_points, player_points = 0, 0

class Ball:
    def __init__(self, x, y, radius, speed_x, speed_y):
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.rect = pygame.Rect(0, 0, radius*2, radius*2)
        self.rect.center = (x, y)
    def Reset(self):
        self.rect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
        self.speed_y = 7 * random.choice([1,-1])
    def Update(self):
        global cpu_points, player_points
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.bottom >= SCREEN_HEIGHT or self.rect.top <=0:
            self.speed_y *= -1
        if self.rect.right >= SCREEN_WIDTH:
            self.speed_x *= -1
            player_points += 1
            self.Reset()        
        if self.rect.left <= 0:
            self.speed_x *= -1
            cpu_points += 1
            self.Reset()
    def Draw(self):
        pygame.draw.ellipse(screen, "white", self.rect)
        
        
        
class Paddle:
    def __init__(self, x, y, width, height, speed_y):
        self.speed_y = speed_y
        self.rect = pygame.Rect(x, y, width, height)
        self.rect.midleft = (x, y)
    def Update(self):
        self.rect.y += self.speed_y
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
    def Draw(self):
        pygame.draw.rect(screen, "white", self.rect)  


ball = Ball(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 15, 6, 6)
player_paddle = Paddle(0, SCREEN_HEIGHT/2, 20, 100, 0)
cpu = Paddle(SCREEN_WIDTH - 20, SCREEN_HEIGHT/2, 20, 100, 0)


score_font = pygame.font.Font(None, 100)




while True:
    
    
    #Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        
        if player_paddle.speed_y == 0 and event.type == pygame.KEYDOWN:    
            if event.key == pygame.K_w:
                player_paddle.speed_y = -6
            if event.key == pygame.K_s:
                player_paddle.speed_y = 6
        if player_paddle.speed_y != 0 and event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                player_paddle.speed_y = 0
            if event.key == pygame.K_s:
                player_paddle.speed_y = 0
                
                
                
    if ball.rect.y > cpu.rect.y:
        cpu.speed_y = 6
    if ball.rect.y < cpu.rect.y:
        cpu.speed_y = -6           

    if ball.rect.colliderect(cpu.rect) or ball.rect.colliderect(player_paddle.rect):
        ball.speed_x *= -1
    

    #Updating Positions
    ball.Update()
    player_paddle.Update()
    cpu.Update()
    
    
            
    #Drawing        
    screen.fill("darkgreen")
    pygame.draw.rect(screen, "forestgreen", (0, 0, SCREEN_WIDTH // 2, SCREEN_HEIGHT))
    
    
    cpu_score_surface = score_font.render(str(cpu_points), True, "white")
    player_score_surface = score_font.render(str(player_points), True, "white")
    screen.blit(cpu_score_surface, (SCREEN_WIDTH * 3/4 - cpu_score_surface.get_width() / 2, 50))
    screen.blit(player_score_surface, (SCREEN_WIDTH * 1/4 - player_score_surface.get_width() / 2, 50))
    
    pygame.draw.aaline(screen, "white", (SCREEN_WIDTH/2, 0), (SCREEN_WIDTH/2, SCREEN_HEIGHT))        
    pygame.draw.circle(screen, "white", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), 100, 5)       
    ball.Draw()           
    cpu.Draw()   
    player_paddle.Draw()       
            
    pygame.display.update()        
    clock.tick(60)





