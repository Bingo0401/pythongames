import pygame
import random
import sys


class Ball:
    def __init__(self, x, y, radius, speed_x, speed_y, screen_width, screen_height, game_window):
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.rect = pygame.Rect(0, 0, radius*2, radius*2)
        self.rect.center = (x, y)
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.game_window = game_window
    def Reset(self):
        self.rect.center = (self.screen_width/2, self.screen_height/2)
        self.speed_y = 7 * random.choice([1,-1])
    def Update(self):
        global cpu_points, player_points
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.bottom >= self.screen_height or self.rect.top <=0:
            self.speed_y *= -1
            
        if self.rect.right >= self.screen_width or self.rect.left <= 0:
            self.speed_x *= -1        
    def Draw(self):
        pygame.draw.ellipse(self.game_window, "white", self.rect)
        
        
        
        
if __name__ == "__main__":        
    pygame.init()

    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 800
    GAME_TITLE = "PONG"

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(GAME_TITLE)
    clock = pygame.time.Clock()
    
    ball = Ball(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 15, 6, 6, SCREEN_WIDTH, SCREEN_HEIGHT, screen)
    
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
       
       
        ball.Update()
       
        screen.fill("black") 
        
        ball.Draw()      

        pygame.display.update()        
        clock.tick(60)         
            
            
#coded by Bingo