import pygame
import random
import constants as Constants

from menus import MainMenu, PauseMenu, GameOverMenu
from map import Map
from player import Player
from dangers import Rocket, Laser


class Game:
    def __init__(self):
        self.WIDTH = Constants.WIDTH
        self.HEIGHT = Constants.HEIGHT

        self.fps = Constants.FPS
        self.game_speed = Constants.INIT_GAME_SPEED
        self.quit = False
        self.restart = False

        self.screen = pygame.display.set_mode([self.WIDTH, self.HEIGHT])
        self.surface = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        pygame.display.set_caption("NitzaJet | by David's team")

        self.main_menu = MainMenu(self.screen, self.surface, True)
        self.pause_menu = PauseMenu(self.screen, self.surface, False)
        self.game_over_menu = GameOverMenu(self.screen, self.surface, False)

        self.map = Map(self.screen)
        self.player = Player(self)
        self.rocket = Rocket(self, self.player)
        self.laser = Laser(self, self.player)

        self.rockets = []
        self.lasers = []

    
    def dangers_generator(self):
        if (not self.game_over_menu.active) and (not self.pause_menu.active) and (not self.main_menu.active):
            if self.rocket.spawn_time >= self.rocket.spawn_interval:
                self.rockets.append({"x": Constants.WIDTH - 60, "y": Constants.HEIGHT / 2, "warning": True})
                self.rocket.spawn_time = 0
                self.rocket.spawn_interval = random.randint(60, 220)  # Generate new time
            else:
                self.rocket.spawn_time += 1
        
            if self.laser.spawn_time >= self.laser.spawn_interval:
                self.lasers.append({"x": self.WIDTH, "y": random.randint(80, self.HEIGHT - 80), "size": random.randint(90, 120)})
                self.laser.spawn_time = 0
                self.laser.spawn_interval = random.randint(120, 360)  # Generate new time
            else:
                self.laser.spawn_time += 1

    
    def run(self):
        while not self.quit:
            pygame.time.Clock().tick(self.fps)

            self.dangers_generator()

            self.map.draw()
            self.player.draw()
            self.rocket.draw()
            self.laser.draw()

            if self.main_menu.active:
                start_btn, quit_btn = self.main_menu.draw()
            elif self.pause_menu.active:
                continue_btn, restart_btn, quit_btn = self.pause_menu.draw()
            elif self.game_over_menu.active:
                restart_btn, quit_btn = self.game_over_menu.draw()

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_ESCAPE) and (not self.main_menu.active) and (not self.game_over_menu.active):
                        if self.pause_menu.active:
                            self.pause_menu.active = False
                        else:
                            self.pause_menu.active = True

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.main_menu.active:
                        if start_btn.collidepoint(event.pos):
                            self.main_menu.active = False
                        elif quit_btn.collidepoint(event.pos):
                            self.quit = True

                    elif self.pause_menu.active:
                        if continue_btn.collidepoint(event.pos):
                            self.pause_menu.active = False
                        elif restart_btn.collidepoint(event.pos):
                            self.pause_menu.active = False
                            self.restart = True
                        elif quit_btn.collidepoint(event.pos):
                            self.quit = True

                    elif self.game_over_menu.active:
                        if restart_btn.collidepoint(event.pos):
                            self.restart = True
                        elif quit_btn.collidepoint(event.pos):
                            self.quit = True

                if self.restart:
                    self.restart = False
                    self.pause_menu.active = False
                    self.game_over_menu.active = False

                    self.rocket.warning_sound = False
                    self.rocket.fly_sound = False
                    self.rocket.sprite.image = Constants.ROCKET_IMAGE

                    self.rockets.clear()
                    self.lasers.clear()

                if event.type == pygame.QUIT:
                    self.quit = True
                    
        pygame.mixer.Sound.play(pygame.mixer.Sound("assets/sounds/ui/quit.ogg"))

        pygame.time.delay(650)
        pygame.quit()


if __name__ == "__main__":
    Game().run()