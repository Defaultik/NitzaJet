import pygame
import random
import constants as Constants

from menus import MainMenu, PauseMenu, GameOverMenu, QuestionMenu
from map import Map
from player import Player
from dangers import Rocket, Laser
from coin import Coin


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
        self.question_menu = QuestionMenu(self.screen, self.surface, False)

        self.map = Map(self.screen)
        self.player = Player(self)
        self.rocket = Rocket(self, self.player)
        self.laser = Laser(self, self.player)

        self.rockets = []
        self.lasers = []
        self.coins = []

        # Initialize coin spawn time and interval
        self.coin_spawn_time = 0
        self.coin_spawn_interval = random.randint(300, 600)

        self.distance = 0
        self.distance_interval = 0

        self.collected_coins = 0
        self.best_distance = 0

        self.load_data()
        

    def load_data(self):
        try:
            with open("data.txt", "r") as file:
                data = file.readlines()
                if data:
                    self.best_distance = int(data[0].strip())
                    self.collected_coins = int(data[1].strip())
                else:
                    self.best_distance = 0
                    self.collected_coins = 0
        except FileNotFoundError:
            self.best_distance = 0
            self.collected_coins = 0


    def save_data(self):
        with open("data.txt", "w") as file:
            file.write(f"{self.best_distance}\n")
            file.write(f"{self.collected_coins}\n")


    def dangers_generator(self):
        if (not self.game_over_menu.active) and (not self.pause_menu.active) and (not self.main_menu.active) and (not self.question_menu.active):
            if self.rocket.spawn_time >= self.rocket.spawn_interval:
                self.rockets.append({"x": Constants.WIDTH - 60, "y": Constants.HEIGHT / 2, "warning": True})
                self.rocket.spawn_time = 0
                self.rocket.spawn_interval = random.randint(60, 300)  # Generate new time
            else:
                self.rocket.spawn_time += 1

            if self.laser.spawn_time >= self.laser.spawn_interval:
                self.lasers.append({"x": self.WIDTH, "y": random.randint(80, self.HEIGHT - 80), "size": random.randint(90, 120)})
                self.laser.spawn_time = 0
                self.laser.spawn_interval = random.randint(160, 550)  # Generate new time
            else:
                self.laser.spawn_time += 1


    def coin_generator(self):
        if (not self.game_over_menu.active) and (not self.pause_menu.active) and (not self.main_menu.active) and (not self.question_menu.active):
            if self.coin_spawn_time >= self.coin_spawn_interval:
                new_coin = Coin(self, self.player, self.WIDTH, random.randint(80, self.HEIGHT - 80))
                self.coins.append(new_coin)

                self.coin_spawn_time = 0
                self.coin_spawn_interval = random.randint(400, 800)  # Generate new interval for next spawn
            else:
                self.coin_spawn_time += 1


    def run(self):
        while not self.quit:
            pygame.time.Clock().tick(self.fps)

            self.dangers_generator()
            self.coin_generator()

            self.map.draw()
            self.player.draw()
            self.rocket.draw()
            self.laser.draw()

            if (not self.pause_menu.active) and (not self.game_over_menu.active) and (not self.main_menu.active) and (not self.question_menu.active):
                for coin in self.coins:
                    coin.update()

            for coin in self.coins[:]:
                coin.draw()

            # Update distance
            if (not self.pause_menu.active) and (not self.game_over_menu.active) and (not self.main_menu.active) and (not self.question_menu.active):
                self.distance += 1

            # Display distance and collected coins in the top-left corner
            distance_text = Constants.FONT_MAIN.render(f"Distance: {self.distance}", True, (255, 255, 255))
            coins_text = Constants.FONT_MAIN.render(f"Coins: {self.collected_coins}", True, (255, 255, 255))
            best_distance_text = Constants.FONT_MAIN.render(f"Best Distance: {self.best_distance}", True, (255, 255, 255))

            self.screen.blit(distance_text, (10, 10))
            self.screen.blit(coins_text, (10, 50))
            self.screen.blit(best_distance_text, (10, 90))

            if self.main_menu.active:
                start_btn, quit_btn = self.main_menu.draw()
            elif self.pause_menu.active:
                continue_btn, restart_btn, quit_btn = self.pause_menu.draw()
            elif self.game_over_menu.active:
                restart_btn, quit_btn = self.game_over_menu.draw()
            elif self.question_menu.active:
                true_btn, false_btn = self.question_menu.draw()

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_ESCAPE) and (not self.main_menu.active) and (not self.game_over_menu.active) and (not self.question_menu.active):
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
                            self.restart = True
                        elif quit_btn.collidepoint(event.pos):
                            self.quit = True

                    elif self.game_over_menu.active:
                        if restart_btn.collidepoint(event.pos):
                            self.restart = True
                        elif quit_btn.collidepoint(event.pos):
                            self.quit = True

                    elif self.question_menu.active:
                        if true_btn.collidepoint(event.pos):
                            if Constants.QUESTIONS[Constants.RANDOM_QUESTION] == True:
                                self.collected_coins += 1
                        elif false_btn.collidepoint(event.pos):
                            if Constants.QUESTIONS[Constants.RANDOM_QUESTION] == False:
                                self.collected_coins += 1
                        
                        self.question_menu.active = False
                        Constants.RANDOM_QUESTION = list(Constants.QUESTIONS.keys())[random.randint(0, 1)]
                            
                if self.restart:
                    self.restart = False
                    self.pause_menu.active = False
                    self.game_over_menu.active = False
                    self.question_menu.active = False

                    self.distance = 0
                    if self.distance > self.best_distance:
                        self.best_distance = self.distance

                    self.player.sprite.rect.x = 350
                    self.player.sprite.rect.y = Constants.HEIGHT / 1.1 - Constants.FLOOR_IMAGE.get_height()

                    self.rocket.warning_sound = False
                    self.rocket.fly_sound = False
                    self.rocket.sprite.image = Constants.ROCKET_IMAGE
                    self.rocket.sprite.rect = self.rocket.sprite.image.get_rect()

                    self.rockets.clear()
                    self.lasers.clear()

                if event.type == pygame.QUIT:
                    self.quit = True

        if self.distance > self.best_distance:
            self.best_distance = self.distance

        self.save_data()
        pygame.quit()

if __name__ == "__main__":
    Game().run()
