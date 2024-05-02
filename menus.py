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
        
        continue_btn = pygame.Rect(Constants.WIDTH / 2.5, (text_rect.y + text_rect.height) + 15, 270, 45)
        pygame.draw.rect(self.screen, "white", continue_btn, 0, 100)
        text_surface = Constants.FONT_MAIN.render("Continue", True, "black")
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
    

class QuestionMenu(Menu):
    def __init__(self, screen, surface, active):
        self.screen = screen
        self.surface = surface
        self.active = active


    def draw(self):
        self.surface.fill((10, 10, 10, 190))

        question = pygame.Rect(Constants.WIDTH / 3, Constants.HEIGHT / 4, 500, 270)
        pygame.draw.rect(self.surface, (0, 0, 0, 200), question, 0, 10)
        text_surface = Constants.FONT_QUESTION.render(Constants.RANDOM_QUESTION, True, "white")
        text_rect = text_surface.get_rect(center=(question.center[0], question.center[1] - 75))
        self.surface.blit(text_surface, text_rect)

        yes = pygame.Rect(question.x + 15, (question.y + question.height) - 60, 150, 50)
        pygame.draw.rect(self.surface, (50, 250, 50, 255), yes, 0, 100)
        text_surface = Constants.FONT_MAIN.render("True", True, "white")
        text_rect = text_surface.get_rect(center=yes.center)
        self.surface.blit(text_surface, text_rect)

        no = pygame.Rect((question.x + question.width) - 15 - 150, (question.y + question.height) - 60, 150, 50)
        pygame.draw.rect(self.surface, (250, 50, 50, 255), no, 0, 100)
        text_surface = Constants.FONT_MAIN.render("False", True, "white")
        text_rect = text_surface.get_rect(center=no.center)
        self.surface.blit(text_surface, text_rect)

        self.screen.blit(self.surface, (0, 0))

        return yes, no