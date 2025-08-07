import pygame
import sys
import random

from Paddle import Paddle
from Ball import Ball


pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 800
GAME_TITLE = "PONG"



screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(GAME_TITLE)
clock = pygame.time.Clock()


points_right, points_left = 0, 0


score_font = pygame.font.Font(None, 100)
small_font = pygame.font.Font(None, 50)


class Game:
    def __init__(self):
        self.ball = Ball(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 15, 6, 6, SCREEN_WIDTH, SCREEN_HEIGHT, screen)
        self.left_paddle = Paddle(0, SCREEN_HEIGHT/2, 20, 100, 0, SCREEN_HEIGHT, screen)
        self.right_paddle = Paddle(SCREEN_WIDTH - 20, SCREEN_HEIGHT/2, 20, 100, 0, SCREEN_HEIGHT, screen)
    def Draw(self):
        self.ball.Draw()
        self.left_paddle.Draw()
        self.right_paddle.Draw()
    def Update(self):
            self.ball.Update()
            self.left_paddle.Update()
            self.right_paddle.Update()
            self.CheckCollisionWithPaddle()
            self.CheckCollisionWithSides()
    def CheckCollisionWithPaddle(self):
        if self.ball.rect.colliderect(self.right_paddle.rect) or self.ball.rect.colliderect(self.left_paddle.rect):
            self.ball.speed_x *= -1
    def CheckCollisionWithSides(self):
        global points_left, points_right
        if self.ball.rect.right >= self.ball.screen_width:
            self.ball.speed_x *= -1
            points_left += 1
            self.ball.Reset()        
        if self.ball.rect.left <= 0:
            self.ball.speed_x *= -1
            points_right += 1
            self.ball.Reset()


class Demo(Game):
    def __init__(self):
        super().__init__()
        self.running_demo = True
    def Update(self):
        return super().Update()


demo = Demo()



#demo
while demo.running_demo:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
                
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                demo.running_demo = False
                
    if demo.ball.rect.x < SCREEN_WIDTH/2:
        if demo.ball.rect.y > demo.left_paddle.rect.y:
            demo.left_paddle.speed_y = 6
        if demo.ball.rect.y < demo.left_paddle.rect.y:
            demo.left_paddle.speed_y = -6
    else:
        demo.left_paddle.speed_y = 0             
                
    if demo.ball.rect.x > SCREEN_WIDTH/2:
        if demo.ball.rect.y > demo.right_paddle.rect.y:
            demo.right_paddle.speed_y = 6
        if demo.ball.rect.y < demo.right_paddle.rect.y:
            demo.right_paddle.speed_y = -6
    else:
        demo.right_paddle.speed_y = 0                        
                              
                
    demo.Update()
                
     
    screen.fill("darkgreen")
    pygame.draw.rect(screen, "forestgreen", (0, 0, SCREEN_WIDTH // 2, SCREEN_HEIGHT))
    
    cpu_score_surface = score_font.render(str(points_right), True, "white")
    player_score_surface = score_font.render(str(points_left), True, "white")
    screen.blit(cpu_score_surface, (SCREEN_WIDTH * 3/4 - cpu_score_surface.get_width() / 2, 50))
    screen.blit(player_score_surface, (SCREEN_WIDTH * 1/4 - player_score_surface.get_width() / 2, 50))
    instructions_surface = small_font.render("[W]UP  [S]DOWN", True, "white")
    space_prompt_surface = small_font.render("Press SPACE to begin", True, "white")

    screen.blit(instructions_surface, ((SCREEN_WIDTH - instructions_surface.get_width()) // 2, SCREEN_HEIGHT - 100))
    screen.blit(space_prompt_surface, ((SCREEN_WIDTH - space_prompt_surface.get_width()) // 2, SCREEN_HEIGHT - 160))
            
    pygame.draw.aaline(screen, "white", (SCREEN_WIDTH/2, 0), (SCREEN_WIDTH/2, SCREEN_HEIGHT))        
    pygame.draw.circle(screen, "white", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), 100, 5)       
    demo.Draw()                 
            
    pygame.display.update()        
    clock.tick(60)






game = Game()
cpu_points, player_points = 0, 0

#game
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
            
            
        if game.left_paddle.speed_y == 0 and event.type == pygame.KEYDOWN:    
            if event.key == pygame.K_w:
                game.left_paddle.speed_y = -6
            if event.key == pygame.K_s:
                game.left_paddle.speed_y = 6
        if game.left_paddle.speed_y != 0 and event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                game.left_paddle.speed_y = 0
            if event.key == pygame.K_s:
                game.left_paddle.speed_y = 0    
        
    if game.ball.rect.y > game.right_paddle.rect.y:
            game.right_paddle.speed_y = 6
    if game.ball.rect.y < game.right_paddle.rect.y:
            game.right_paddle.speed_y = -6   

    #Updating Positions
    game.Update()
        
    #Drawing        
    screen.fill("darkgreen")
    pygame.draw.rect(screen, "forestgreen", (0, 0, SCREEN_WIDTH // 2, SCREEN_HEIGHT))
    
    
    cpu_score_surface = score_font.render(str(points_right), True, "white")
    player_score_surface = score_font.render(str(points_left), True, "white")
    screen.blit(cpu_score_surface, (SCREEN_WIDTH * 3/4 - cpu_score_surface.get_width() / 2, 50))
    screen.blit(player_score_surface, (SCREEN_WIDTH * 1/4 - player_score_surface.get_width() / 2, 50))
    
    pygame.draw.aaline(screen, "white", (SCREEN_WIDTH/2, 0), (SCREEN_WIDTH/2, SCREEN_HEIGHT))        
    pygame.draw.circle(screen, "white", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), 100, 5)  
        
    game.Draw()       
            
    pygame.display.update()        
    clock.tick(60)



