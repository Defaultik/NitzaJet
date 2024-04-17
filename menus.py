import pygame
import constants as Constants
import random

class Menu:
    def __init__(self, screen, surface, active):
        self.screen = screen
        self.surface = surface
        self.active = active


    def draw(self):
        pass


class MainMenu(Menu):
    def __init__(self, screen, surface, active):
        super().__init__(screen, surface, active)
    

    def draw(self):
        self.screen.blit(Constants.BACKGROUND_IMAGE, (0, 0))
        self.surface.fill((10, 10, 10, 190))
        self.screen.blit(self.surface, (0, 0))
        
        text_surface = Constants.FONT_LOGO.render("NITZAJET", True, "white")
        text_rect = text_surface.get_rect(center=(Constants.WIDTH / 2.05, Constants.HEIGHT / 3))
        self.screen.blit(text_surface, text_rect)
        
        start_btn = pygame.Rect(Constants.WIDTH / 2.5, (text_rect.y + text_rect.height) + 15, 270, 45)
        pygame.draw.rect(self.screen, "white", start_btn, 0, 100)
        text_surface = Constants.FONT_MAIN.render("Play", True, "black")
        text_rect = text_surface.get_rect(center=start_btn.center)
        self.screen.blit(text_surface, text_rect)
        
        quit_btn = pygame.Rect(Constants.WIDTH / 2.5, start_btn.y + 60, 270, 45)
        pygame.draw.rect(self.screen, "white", quit_btn, 0, 100)
        text_surface = Constants.FONT_MAIN.render("Quit", True, "black")
        text_rect = text_surface.get_rect(center=quit_btn.center)
        self.screen.blit(text_surface, text_rect)

        random_fact = Constants.FONT_MAIN.render(f'"{Constants.RANDOM_QUESTION}"', True, (100, 100, 100, 60))
        random_fact_rect = random_fact.get_rect(center=(quit_btn.center[0], 25))
        self.screen.blit(random_fact, random_fact_rect)

        return start_btn, quit_btn


class PauseMenu(Menu):
    def __init__(self, screen, surface, active):
        super().__init__(screen, surface, active)

    
    def draw(self):
        self.surface.fill((10, 10, 10, 190))
        self.screen.blit(self.surface, (0, 0))
        
        text_surface = Constants.FONT_LOGO.render("Pause", True, "white")
        text_rect = text_surface.get_rect(center=(Constants.WIDTH / 2.05, Constants.HEIGHT / 3))
        self.screen.blit(text_surface, text_rect)
        
        continue_btn = pygame.Rect(Constants.WIDTH / 2.5, (text_rect.y + text_rect.height) + 20, 270, 45)
        pygame.draw.rect(self.screen, "white", continue_btn, 0, 100)
        text_surface = Constants.FONT_MAIN.render("Play", True, "black")
        text_rect = text_surface.get_rect(center=continue_btn.center)
        self.screen.blit(text_surface, text_rect)
        
        restart_btn = pygame.Rect(Constants.WIDTH / 2.5, continue_btn.y + 60, 270, 45)
        pygame.draw.rect(self.screen, "white", restart_btn, 0, 100)
        text_surface = Constants.FONT_MAIN.render("Restart", True, "black")
        text_rect = text_surface.get_rect(center=restart_btn.center)
        self.screen.blit(text_surface, text_rect)
        
        quit_btn = pygame.Rect(Constants.WIDTH / 2.5, restart_btn.y + 60, 270, 45)
        pygame.draw.rect(self.screen, "white", quit_btn, 0, 100)
        text_surface = Constants.FONT_MAIN.render("Quit", True, "black")
        text_rect = text_surface.get_rect(center=quit_btn.center)
        self.screen.blit(text_surface, text_rect)

        return continue_btn, restart_btn, quit_btn


class GameOverMenu(Menu):
    def __init__(self, screen, surface, active):
        super().__init__(screen, surface, active)
    
    
    def draw(self):
        self.surface.fill((10, 10, 10, 190))
        self.screen.blit(self.surface, (0, 0))
        
        text_surface = Constants.FONT_LOGO.render("Game Over", True, "white")
        text_rect = text_surface.get_rect(center=(Constants.WIDTH / 2.05, Constants.HEIGHT / 3))
        self.screen.blit(text_surface, text_rect)
        
        restart_btn = pygame.Rect(Constants.WIDTH / 2.5, (text_rect.y + text_rect.height) + 20, 270, 45)
        pygame.draw.rect(self.screen, "white", restart_btn, 0, 100)
        text_surface = Constants.FONT_MAIN.render("Restart", True, "black")
        text_rect = text_surface.get_rect(center=restart_btn.center)
        self.screen.blit(text_surface, text_rect)
        
        quit_btn = pygame.Rect(Constants.WIDTH / 2.5, restart_btn.y + 60, 270, 45)
        pygame.draw.rect(self.screen, "white", quit_btn, 0, 100)
        text_surface = Constants.FONT_MAIN.render("Quit", True, "black")
        text_rect = text_surface.get_rect(center=quit_btn.center)
        self.screen.blit(text_surface, text_rect)

        return restart_btn, quit_btn