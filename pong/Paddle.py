import pygame
import sys



class Paddle:
    def __init__(self, x, y, width, height, speed_y, screen_height, game_window):
        self.speed_y = speed_y
        self.rect = pygame.Rect(x, y, width, height)
        self.rect.midleft = (x, y)
        self.screen_height = screen_height
        self.game_window = game_window
    def Update(self):
        self.rect.y += self.speed_y
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= self.screen_height:
            self.rect.bottom = self.screen_height
    def Draw(self):
        pygame.draw.rect(self.game_window, "white", self.rect)  
        
        
        
        
        
